#!/usr/bin/env python3
"""
Inject small zero-mean random velocity perturbations into an OpenFOAM ascii
0/U field, to break horizontal symmetry so LES can develop 3-D turbulence.

Pure standard library (no numpy) so it runs under any python3, including the
WSL base env that lacks numpy.

Usage:
  python3 perturb_U.py --field 0/U [--sigma 1e-3] [--seed 42]
                       [--ncells N]              # required only if internalField is 'uniform'
                       [--centres 0/C --ztaper 60 --zscale 15]  # optional depth taper (z positive DOWN)
                       [--no-w]                  # do not perturb vertical (z) component

Writes <field>.bak once, then overwrites <field> in place.
"""
import argparse, os, random, re, sys, math


def read(path):
    with open(path, "r") as f:
        return f.read()


def parse_internal_vectors(txt):
    """Return (kind, prefix, vectors, suffix) where kind in {uniform,nonuniform}.
    prefix/suffix are the file text before/after the numeric payload so we can
    rewrite losslessly."""
    m = re.search(r"internalField\s+", txt)
    if not m:
        raise ValueError("no internalField found")
    # uniform case: internalField   uniform (x y z);
    prefix = txt[:m.start()]
    mu = re.match(r"internalField\s+uniform\s*\(([^()]*)\)\s*;", txt[m.start():])
    if mu:
        comps = [float(x) for x in mu.group(1).split()]
        return ("uniform", prefix, comps, txt[m.start()+mu.end():])
    # nonuniform case
    mn = re.match(r"internalField\s+nonuniform\s+List<vector>\s*", txt[m.start():])
    if not mn:
        raise ValueError("internalField is neither uniform nor nonuniform List<vector>")
    rest = txt[m.start() + mn.end():]
    # optional leading count, then ( ... ) ;
    mc = re.match(r"(\d+)\s*", rest)
    count = int(mc.group(1)) if mc else None
    paren_start = rest.index("(", mc.end() if mc else 0)
    # find matching close paren for the outer list
    depth = 0
    for i in range(paren_start, len(rest)):
        if rest[i] == "(":
            depth += 1
        elif rest[i] == ")":
            depth -= 1
            if depth == 0:
                paren_end = i
                break
    else:
        raise ValueError("unterminated list")
    body = rest[paren_start+1:paren_end]
    vecs = re.findall(r"\(([^()]*)\)", body)
    vectors = [[float(x) for x in v.split()] for v in vecs]
    if count is not None and count != len(vectors):
        raise ValueError(f"count {count} != parsed {len(vectors)}")
    # advance past the terminating ';' so suffix starts cleanly
    j = paren_end + 1
    while j < len(rest) and rest[j] in " \t\r\n":
        j += 1
    if j < len(rest) and rest[j] == ";":
        j += 1
    suffix = rest[j:]
    return ("nonuniform", prefix, vectors, suffix)


def parse_centres_z(path):
    txt = read(path)
    kind, _, vectors, _ = parse_internal_vectors(txt)
    if kind != "nonuniform":
        raise ValueError("centres field must be nonuniform")
    return [v[2] for v in vectors]


def amp(sigma, z, ztaper, zscale):
    if ztaper is None:
        return sigma
    if z <= ztaper:
        return sigma
    return sigma * math.exp(-(z - ztaper) / zscale)


def fmt(v):
    return "(" + " ".join(repr(c) if False else ("%.10g" % c) for c in v) + ")"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--field", required=True)
    ap.add_argument("--sigma", type=float, default=1e-3)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ncells", type=int, default=None)
    ap.add_argument("--centres", default=None)
    ap.add_argument("--ztaper", type=float, default=None)
    ap.add_argument("--zscale", type=float, default=15.0)
    ap.add_argument("--no-w", action="store_true")
    a = ap.parse_args()

    random.seed(a.seed)
    txt = read(a.field)
    kind, prefix, payload, suffix = parse_internal_vectors(txt)

    if kind == "uniform":
        if a.ncells is None:
            print("ERROR: internalField is uniform; pass --ncells N to expand", file=sys.stderr)
            sys.exit(2)
        base = payload
        vectors = [list(base) for _ in range(a.ncells)]
    else:
        vectors = payload

    zs = None
    if a.centres:
        zs = parse_centres_z(a.centres)
        if len(zs) != len(vectors):
            print(f"ERROR: centres {len(zs)} != cells {len(vectors)}", file=sys.stderr)
            sys.exit(2)

    n = len(vectors)
    # zero-mean: subtract the mean perturbation afterwards per component
    dvs = []
    for i in range(n):
        z = zs[i] if zs is not None else 0.0
        s = amp(a.sigma, z, a.ztaper, a.zscale)
        dx = random.gauss(0.0, s)
        dy = random.gauss(0.0, s)
        dz = 0.0 if a.no_w else random.gauss(0.0, s)
        dvs.append((dx, dy, dz))
    mx = sum(d[0] for d in dvs) / n
    my = sum(d[1] for d in dvs) / n
    mz = sum(d[2] for d in dvs) / n
    for i in range(n):
        vectors[i][0] += dvs[i][0] - mx
        vectors[i][1] += dvs[i][1] - my
        vectors[i][2] += dvs[i][2] - mz

    body = "\n".join(fmt(v) for v in vectors)
    newtxt = prefix + "internalField   nonuniform List<vector> \n%d\n(\n%s\n)\n;" % (n, body) + suffix
    if not os.path.exists(a.field + ".bak"):
        with open(a.field + ".bak", "w") as f:
            f.write(txt)
    with open(a.field, "w") as f:
        f.write(newtxt)
    print(f"OK: perturbed {n} cells, sigma={a.sigma}, taper={a.ztaper}, no_w={a.no_w}")


if __name__ == "__main__":
    main()
