#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/../')

def trysolve():
    import sympy

    equations = sympy.sympify([
    'a + b + c - 1',
    '2*a + b - 2',
    '3*c - 3',
    ])

    sympyvars = ['a', 'b', 'c']

    print('Numeric solve:')
    from solgeneral_func import solveeqs
    varssdict = solveeqs(equations, sympyvars)
    print(varssdict)

    print('\nSympy solve:')
    from solgeneral_func import solveeqs
    varssdict2 = solveeqs(equations, sympyvars, numericsolve = False)
    print(varssdict2)

# Run:{{{1
trysolve()
