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

def solveeqs(equations, sympyvars, startval = None, numericsolve = True, fsolvemethod = 'hybr'):
    """
    Solve set of nonlinear equations.
    If numericsolve is True, use numeric methods via scipy.

    This isn't meant to extend the methods in scipy or sympy in any way. It's just meant as a quick summary to help me remember how they work and also a quick and dirty application method.

    fsolve method 'hybr' requires that equations and sympyvars have same length. 'lm' does not.
    """
    import sympy
    
    # ensure vars list is a list
    sympyvars = list(sympyvars)

    if startval is None:
        startval = [0.0] * len(sympyvars)

    if numericsolve is True:
        import scipy.optimize

        # ensure equations is a list
        # if it is a matrix, scipy.optimize does not work.
        try:
            equations[0, 0]

            # if no error then matrix.
            equations = list(equations)
        except:
            None

        # make it a function like f([1,2,3]) rather than f(1,2,3) by adding [] around sympyvars
        func = sympy.lambdify([sympyvars], equations)

        try:
            func([0.1] * len(sympyvars))
        except Exception:
            print('ERROR: Basic function does not work')
            print('\nEquations:')
            print(equations)
            print('\nVariables that are supposed to be in equations:')
            print(sympyvars)
            asdfjkl;

        # ssvars = scipy.optimize.root(func, [0.1] * len(solvevars), method = 'lm')
        output = scipy.optimize.root(func, startval, method = fsolvemethod)
        if output['success'] is True:
            ssvars = output['x']
        else:
            print('ERROR: steadystatesolve failed')
            print(output)
            asdfjkl;

        varssdict = {}
        for i in range(len(sympyvars)):
            var = sympyvars[i]
            # need float otherwise given in strange format i.e. mpf()
            varssdict[var] = float(ssvars[i])
    else:
        varssdict = sympy.solve(equations, sympyvars)

        # if equations are sympy matrix, this returns [(0, 0.96, 0.07)].
        # if equations are sympy vector, this returns {'a': 0, 'k': 0.96, 'c': 0.07}.
        # need to account for this:
        try:
            if isinstance(varssdict[0], tuple):
                temp = varssdict[0]
                varssdict = {}
                for i in range(len(sympyvars)):
                    var = sympyvars[i]
                    # need float otherwise given in strange format i.e. mpf()
                    varssdict[var] = float(temp[i])
        except:
            None


    return(varssdict)
