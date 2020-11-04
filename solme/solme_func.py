#!/usr/bin/env python3
"""
3 steps:
1. Simplify by removing varialbes that only appear sparsely.
2. Solve the remaining equations (if any).
3. Simplify the equations.
"""
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

# Main Functions:{{{1
def simplifyfunc(eqs, occurrences = 2):
    import sympy

    variables = eqs.atoms(sympy.Symbol)

    # the number of time the variable occurs in the equations
    occurrences = 1

    solvar = []
    solsol = []
    while True:

        # the variables in each eq of eqs
        eqs_vars = []
        # the number of variables in each eq of eqs
        eqs_vars_freq = []
        for i in range(0, len(eqs)):
            symbols = eqs[i,0].atoms(sympy.Symbol)
            eqs_vars.append(symbols)
            eqs_vars_freq.append(len(symbols))
            

        varstar = None
        for var in variables:
            # I compute the number of times the variable occurs in the equations.
            # I then find whether equations exist with only one occurrence of that form of variable i.e. K - L has only one form of K but K + K^2 - L has two forms
            numoc = 0
            besteq = None
            for i in range(len(eqs)):
                # number of occurrences
                if var in eqs_vars[i]:
                    numoc = numoc + 1

                    # check number of times occurs
                    eq = eqs[i]
                    # replacing K + K**2 - L with K + K**2 - 1.
                    # ISSUE: what if constants cancel i.e. K + K**2 - L + T? Then get wrong number.
                    for var2 in variables:
                        if var2 != var:
                            eq = eq.subs(var2, 1)
                    # ignore integer
                    numterms = sympy.count_ops(eq) - 1

                    # set the best equation for this term
                    if besteq is None:
                        besteq = i
                    elif besteqnumterms > numterms:
                        besteq = i
                    elif besteqnumterms == numterms and eqs_vars_freq[besteq] > eqs_vars_freq[i]:
                        besteq = i

                    if besteq == i:
                        besteqnumterms = numterms
            if numoc <= occurrences:
                if varstar is None or numocstar < numoc or (numocstar == numoc and besteqnumterms < numtermsstar):
                    if besteqnumterms == 1 or numoc == 1:
                        varstar = var
                        numocstar = numoc
                        besteqstar = besteq
                        numtermsstar = besteqnumterms

                        # make replacements for single eq immediately.
                        # if numocstar == 1:
                        #     break
                            
        # if no sol:
        if varstar is None:
            break
        sol = sympy.solve(eqs[besteqstar], varstar)
        # remove row
        eqs.row_del(besteqstar)
        # substitute out other instances of variable
        for i in range(len(eqs)):
            eqs[i, 0] = eqs[i, 0].subs(varstar, sol)

        variables.remove(varstar)

        solvar.append(str(varstar))
        if len(sol) == 1:
            sol = sol[0]
        solsol.append(sol)


    return(eqs, solvar, solsol)



def simplifyfunc(eqs, othervars = 1, bounddict = {}, printiterations = False):
    """
    Look for lines of eqs with just no other variables, 1 other variable etc.
    """
    import numpy as np
    import scipy.optimize
    import sympy
    import sys

    variables = eqs.atoms(sympy.Symbol)

    solvar = []
    solsol = []
    # while look through eqs
    while True:
        # make copy of eqs so that can delete lines that don't work
        eqs2 = eqs.copy()
        # the variables in each eq of eqs
        eqs_vars = []
        # the number of variables in each eq of eqs
        eqs_vars_freq = []
        for i in range(0, len(eqs)):
            symbols = eqs[i,0].atoms(sympy.Symbol)
            eqs_vars.append(symbols)
            eqs_vars_freq.append(len(symbols))

        foundvar = False
        # while over individual eq within eqs.
        while foundvar is False and len(eqs2) > 0:
            import datetime
            argmin = np.argmin(eqs_vars_freq)
            numothervars = eqs_vars_freq[argmin] - 1
            if numothervars <= othervars:
                varseq = eqs_vars[argmin]

                for var in varseq:
                    try:
                        sol = sympy.solve(eqs2[argmin], var)
                        if len(sol) == 1:
                            sol = sol[0]
                            # found goodvar so break for chain and set foundvar to True so break search over other eqs.
                            foundvar = True
                    except Exception:
                        # doesn't work well sometimes with single variable functions.
                        # for example if have sth like x1 + log(x1) - 1.61051.
                        # Then use scipy and make note of what did.
                        if len(varseq) == 1:
                            print('Used scipy for var: ' + str(var) + ' starting from 0.1.')
                            # sympy.nsolve(eqs2[argmin], var, 0.1)

                            func = sympy.lambdify([var], eqs2[argmin])

                            output = scipy.optimize.root(func, [0.1])
                            if output['success'] is True:
                                # weird expression needed to get sympy number - otherwise get exception when try to do subs later
                                # must be better way to do this
                                sol = (output['x'][0] + sympy.Symbol('a')).subs(sympy.Symbol('a'), 0)
                                foundvar = True
                            else:
                                None
                                # just carry on and try next var
                    if foundvar is True:
                        if str(var) in bounddict:
                            if (bounddict[var][0] is None or sol > bounddict[var][0]) and (bounddict[var][1] is None or sol < bounddict[var][1]) and (bounddict[var][2] is None or sol >= bounddict[var][2]) and (bounddict[var][3] is None and sol <= bounddict[var][3]):
                                # this stops iterating over variables
                                break
                            else:
                                foundvar = False
                
                if foundvar is True:
                    # this stops iterating over equations
                    break
                else:
                    # delete this line so don't consider again
                    eqs2.row_del(argmin)
                    del eqs_vars[argmin]
                    del eqs_vars_freq[argmin]
            else:
                # if too many vars
                break
                        
        # if no sol then break chain over looking through equations:
        if foundvar is False:
            break
        eqs.row_del(argmin)
        # substitute out other instances of variable
        print(var)
        print(sol)
        eqs = eqs.subs(var, sol)
        # for i in range(len(eqs)):
        #     eqs[i, 0] = eqs[i, 0].subs(var, sol)

        variables.remove(var)

        solvar.append(str(var))
        solsol.append(sol)

        if printiterations is True:
            print('')
            print(eqs)
            print(solvar)
            print(solsol)


    return(eqs, solvar, solsol)



def solveeqs(eqs, initval = None):
    """
    This function is really given for expositional purposes (to show the second of the third steps of solving by first simplifying). It doesn't really add anything.
    """
    import scipy.optimize
    import sys

    solveeqs = [eqs[i, 0] for i in range(len(eqs))]

    sympyvars = list(solveeqs.atoms(sympy.Symbol))

    func = sympy.lambdify([sympyvars], solveeqs)

    try:
        func([0.1] * len(sympyvars))
    except Exception:
        print('ERROR: Basic function does not work')
        sys.exit(1)

    output = scipy.optimize.root(func, [0.1] * len(sympyvars))
    if output['success'] is True:
        ssvars = output['x']
    else:
        print('ERROR: steadystatesolve failed')
        print(output)
        sys.exit(1)
    

def simplifysolutionlists(soldict, partsolvar, partsolsol):
    """
    I have a dictionary of values for soldict.
    Solve these variables into partsolvar and partsolsol (what I got from simplifyfunc) to simplify the functions.
    """
    import sympy

    # first input actual solutions
    for var in soldict:
        for i in reversed(range(len(partsolvar))):
            partsolsol[i].subs(sympy.Symbol(var), soldict[var])

    # now go back through partially solved equations
    for j in reversed(range(len(partsolvar))):
        for i in reversed(range(len(partsolvar))):
            soldict[partsolvar[j]] = partsolsol[j]
            partsolsol[i] = partsolsol[i].subs(sympy.Symbol(partsolvar[j]), partsolsol[j])

    return(soldict)
