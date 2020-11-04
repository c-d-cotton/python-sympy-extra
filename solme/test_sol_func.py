#!/usr/bin/env python3
# PYTHON_PREAMBLE_START_STANDARD:{{{

# Christopher David Cotton (c)
# http://www.cdcotton.com

# modules needed for preamble
import importlib
import os
from pathlib import Path
import sys

# Get full real filename
__fullrealfile__ = os.path.abspath(__file__)

# Function to get git directory containing this file
def getprojectdir(filename):
    curlevel = filename
    while curlevel is not '/':
        curlevel = os.path.dirname(curlevel)
        if os.path.exists(curlevel + '/.git/'):
            return(curlevel + '/')
    return(None)

# Directory of project
__projectdir__ = Path(getprojectdir(__fullrealfile__))

# Function to call functions from files by their absolute path.
# Imports modules if they've not already been imported
# First argument is filename, second is function name, third is dictionary containing loaded modules.
modulesdict = {}
def importattr(modulefilename, func, modulesdict = modulesdict):
    # get modulefilename as string to prevent problems in <= python3.5 with pathlib -> os
    modulefilename = str(modulefilename)
    # if function in this file
    if modulefilename == __fullrealfile__:
        return(eval(func))
    else:
        # add file to moduledict if not there already
        if modulefilename not in modulesdict:
            # check filename exists
            if not os.path.isfile(modulefilename):
                raise Exception('Module not exists: ' + modulefilename + '. Function: ' + func + '. Filename called from: ' + __fullrealfile__ + '.')
            # add directory to path
            sys.path.append(os.path.dirname(modulefilename))
            # actually add module to moduledict
            modulesdict[modulefilename] = importlib.import_module(''.join(os.path.basename(modulefilename).split('.')[: -1]))

        # get the actual function from the file and return it
        return(getattr(modulesdict[modulefilename], func))

# PYTHON_PREAMBLE_END:}}}

# Test 1:{{{1
def test1():
    import sympy

    eqs_string = [
    'x1 + log(x1) - x2',
    'x2 - x3',
    'x3 - x4',
    'x4**0.2 - x5',
    'x5 - x6 - 0.1',
    'x6 - 1'
    ]

    eqs = sympy.zeros(len(eqs_string),1)

    for i in range(len(eqs_string)):
        eqs[i,0] = sympy.sympify(eqs_string[i])

    sympyvars = list(eqs.atoms(sympy.Symbol))

    ssvars = sympy.nsolve(eqs, sympyvars, [0.1] * len(eqs))
    print('Sol by attempt using standard numerical methods')
    # not sure why x6 and x2 appear to be reversed
    print(ssvars)

    # try and solve by other method
    print('\nSol by simplification first solution.')
    eqs2, solvar, solsol = importattr(__projectdir__ / Path('solme/solme_func.py'), 'simplifyfunc')(eqs.copy())
    
    soldict = {}

    soldict = importattr(__projectdir__ / Path('solme/solme_func.py'), 'simplifysolutionlists')(soldict, solvar, solsol)
    print(soldict)

    # verifying this is a solution
    eqs2 = eqs.copy()
    for var in soldict:
        eqs2 = eqs2.subs(sympy.Symbol(var), soldict[var])
    print(eqs2)

