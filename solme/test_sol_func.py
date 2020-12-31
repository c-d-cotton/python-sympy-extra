#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/../')

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
    from solme_func import simplifyfunc
    eqs2, solvar, solsol = simplifyfunc(eqs.copy())
    
    soldict = {}

    from solme_func import simplifysolutionlists
    soldict = simplifysolutionlists(soldict, solvar, solsol)
    print(soldict)

    # verifying this is a solution
    eqs2 = eqs.copy()
    for var in soldict:
        eqs2 = eqs2.subs(sympy.Symbol(var), soldict[var])
    print(eqs2)

