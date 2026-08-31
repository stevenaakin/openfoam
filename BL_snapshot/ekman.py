import re, sys, math

def parse_vectors(path):
    txt = open(path).read()
    m = re.search(r'internalField\s+nonuniform\s+List<vector>\s*', txt)
    rest = txt[m.end():]
    mc = re.match(r'\s*(\d+)\s*', rest)
    ps = rest.index('(', mc.end())
    depth = 0
    for i in range(ps, len(rest)):
        if rest[i] == '(':
            depth += 1
        elif rest[i] == ')':
            depth -= 1
            if depth == 0:
                pe = i
                break
    body = rest[ps+1:pe]
    vecs = re.findall(r'\(([^()]*)\)', body)
    return [[float(x) for x in v.split()] for v in vecs]

def depths(L, n, R):
    r = R**(1.0/(n-1))
    d1 = L*(r-1)/(r**n - 1) if abs(r-1) > 1e-12 else L/n
    centers, edge = [], 0.0
    for i in range(n):
        w = d1*r**i
        centers.append(edge + w/2.0)
        edge += w
    return centers

def main():
    path = sys.argv[1]
    nx, ny, nz = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    L = float(sys.argv[5]) if len(sys.argv) > 5 else 200.0
    R = float(sys.argv[6]) if len(sys.argv) > 6 else 10.0
    vs = parse_vectors(path)
    assert len(vs) == nx*ny*nz, (len(vs), nx*ny*nz)
    per = nx*ny
    zc = depths(L, nz, R)
    print('  z(m)    mean_u     mean_v     speed    dir(deg)   rms_u    rms_v    rms_w')
    for k in range(nz):
        cells = vs[k*per:(k+1)*per]
        mu = sum(c[0] for c in cells)/per
        mv = sum(c[1] for c in cells)/per
        su = (sum((c[0]-mu)**2 for c in cells)/per)**0.5
        sv = (sum((c[1]-mv)**2 for c in cells)/per)**0.5
        sw = (sum((c[2])**2 for c in cells)/per)**0.5
        speed = (mu*mu + mv*mv)**0.5
        d = math.degrees(math.atan2(mv, mu))
        print('%6.2f %10.6f %10.6f %9.6f %9.2f %8.6f %8.6f %8.6f' % (zc[k], mu, mv, speed, d, su, sv, sw))

main()
