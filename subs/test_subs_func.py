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

def eqs():
    """
    This is actually slower than the standard case.
    """
    import datetime
    import sympy

    n = 50
    symbols = [sympy.Symbol('x' + str(i)) for i in range(0, n)]

    # different matrices to try
    # matrix = [[symbols[i]] + [0] * (n - 1) for i in range(0, n)]
    # matrix = [[symbols[i]] * n for i in range(0, n)]
    matrix = [[1] + [0] * (n - 1) for i in range(0, n)]

    matrix = sympy.Matrix(matrix)

    replacedict = {}
    for i in range(0, n):
        replacedict[str(symbols[i])] = i


    print('My method - matrixsubsquick:')
    now = datetime.datetime.now()
    matrix2 = importattr(__projectdir__ / Path('subs/subs_func.py'), 'matrixsubsquick')(matrix, replacedict)
    print(str(datetime.datetime.now() - now))

    print('My method2 - subsympymatrix_string:')
    now = datetime.datetime.now()
    matrix2 = importattr(__projectdir__ / Path('subs/subs_func.py'), 'subsympymatrix_string')(matrix, replacedict)
    print(str(datetime.datetime.now() - now))

    print('My method3 - matrixofelements:')
    print('First part:')
    now = datetime.datetime.now()
    matrixofelements = importattr(__projectdir__ / Path('subs/subs_func.py'), 'getmatrixofsympyelements')(matrix)
    print(str(datetime.datetime.now() - now))
    print('Second part:')
    now = datetime.datetime.now()
    matrix2 = importattr(__projectdir__ / Path('subs/subs_func.py'), 'submatrixfrommatrixofelements')(matrix, replacedict, matrixofelements)
    print(str(datetime.datetime.now() - now))

    print('lambdifysubs method:')
    now = datetime.datetime.now()
    matrix2= importattr(__projectdir__ / Path('subs/subs_func.py'), 'lambdifysubs')(matrix, replacedict)
    print(str(datetime.datetime.now() - now))

    print('lambdifysubs split method:')
    print('First part:')
    now = datetime.datetime.now()
    matrix_f, sortedvars = importattr(__projectdir__ / Path('subs/subs_func.py'), 'lambdifysubs_lambdifyonly')(matrix, replacedict)
    print(str(datetime.datetime.now() - now))
    print('Second part:')
    now = datetime.datetime.now()
    matrix2 = importattr(__projectdir__ / Path('subs/subs_func.py'), 'lambdifysubs_subsonly')(matrix_f, sortedvars, replacedict)
    print(str(datetime.datetime.now() - now))

    print('sympy evalf method:')    
    now = datetime.datetime.now()
    matrix2= matrix.evalf(subs=replacedict)
    print(str(datetime.datetime.now() - now))

    print('sympy subs method:')    
    now = datetime.datetime.now()
    matrix2= matrix.subs(replacedict)
    print(str(datetime.datetime.now() - now))


# Run:{{{1
eqs()
