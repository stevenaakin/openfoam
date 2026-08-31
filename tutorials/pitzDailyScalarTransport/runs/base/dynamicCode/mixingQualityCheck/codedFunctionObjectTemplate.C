/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) YEAR OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "codedFunctionObjectTemplate.H"
#include "volFields.H"
#include "read.H"
#include "addToRunTimeSelectionTable.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

defineTypeNameAndDebug(mixingQualityCheckFunctionObject, 0);

addRemovableToRunTimeSelectionTable
(
    functionObject,
    mixingQualityCheckFunctionObject,
    dictionary
);


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    // dynamicCode:
    // SHA1 = 13204e8ce69fe389c7f209808338402d752f1a3c
    //
    // unique function name that can be checked if the correct library version
    // has been loaded
    void mixingQualityCheck_13204e8ce69fe389c7f209808338402d752f1a3c(bool load)
    {
        if (load)
        {
            // code that can be explicitly executed after loading
        }
        else
        {
            // code that can be explicitly executed before unloading
        }
    }
}


// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * Private Member Functions  * * * * * * * * * * * //

const fvMesh& mixingQualityCheckFunctionObject::mesh() const
{
    return refCast<const fvMesh>(obr_);
}


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

mixingQualityCheckFunctionObject::mixingQualityCheckFunctionObject
(
    const word& name,
    const Time& runTime,
    const dictionary& dict
)
:
    functionObjects::regionFunctionObject(name, runTime, dict)
{
    read(dict);
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

mixingQualityCheckFunctionObject::~mixingQualityCheckFunctionObject()
{}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

bool mixingQualityCheckFunctionObject::read(const dictionary& dict)
{
    if (false)
    {
        Info<<"read mixingQualityCheck sha1: 13204e8ce69fe389c7f209808338402d752f1a3c\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


Foam::wordList mixingQualityCheckFunctionObject::fields() const
{
    if (false)
    {
        Info<<"fields mixingQualityCheck sha1: 13204e8ce69fe389c7f209808338402d752f1a3c\n";
    }

    wordList fields;
//{{{ begin code
    
//}}} end code

    return fields;
}


bool mixingQualityCheckFunctionObject::execute()
{
    if (false)
    {
        Info<<"execute mixingQualityCheck sha1: 13204e8ce69fe389c7f209808338402d752f1a3c\n";
    }

//{{{ begin code
    #line 32 "/home/sakin/openfoam/tutorials/pitzDailyScalarTransport/runs/base/system/functions/mixingQualityCheck"

        const volScalarField& T
        (
            mesh().lookupObject<volScalarField>("T")
        );

        const scalar maxT = max(T).value();
        const scalar meanT = T.weightedAverage(mesh().V()).value();

        const scalar mixingQuality = meanT/maxT;
        Info << "mixingQuality = " << mixingQuality << endl;

        if (mixingQuality > 0.9)
        {
            const_cast<Time&>(mesh().time()).writeAndEnd();
        }
    
//}}} end code

    return true;
}


bool mixingQualityCheckFunctionObject::write()
{
    if (false)
    {
        Info<<"write mixingQualityCheck sha1: 13204e8ce69fe389c7f209808338402d752f1a3c\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


bool mixingQualityCheckFunctionObject::end()
{
    if (false)
    {
        Info<<"end mixingQualityCheck sha1: 13204e8ce69fe389c7f209808338402d752f1a3c\n";
    }

//{{{ begin code
    
//}}} end code

    return true;
}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// ************************************************************************* //

