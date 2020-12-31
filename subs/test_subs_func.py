#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/../')

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
    from subs_func import matrixsubsquick
    matrix2 = matrixsubsquick(matrix, replacedict)
    print(str(datetime.datetime.now() - now))

    print('My method2 - subsympymatrix_string:')
    now = datetime.datetime.now()
    from subs_func import subsympymatrix_string
    matrix2 = subsympymatrix_string(matrix, replacedict)
    print(str(datetime.datetime.now() - now))

    print('My method3 - matrixofelements:')
    print('First part:')
    now = datetime.datetime.now()
    from subs_func import getmatrixofsympyelements
    matrixofelements = getmatrixofsympyelements(matrix)
    print(str(datetime.datetime.now() - now))
    print('Second part:')
    now = datetime.datetime.now()
    from subs_func import submatrixfrommatrixofelements
    matrix2 = submatrixfrommatrixofelements(matrix, replacedict, matrixofelements)
    print(str(datetime.datetime.now() - now))

    print('lambdifysubs method:')
    now = datetime.datetime.now()
    from subs_func import lambdifysubs
    matrix2= lambdifysubs(matrix, replacedict)
    print(str(datetime.datetime.now() - now))

    print('lambdifysubs split method:')
    print('First part:')
    now = datetime.datetime.now()
    from subs_func import lambdifysubs_lambdifyonly
    matrix_f, sortedvars = lambdifysubs_lambdifyonly(matrix, replacedict)
    print(str(datetime.datetime.now() - now))
    print('Second part:')
    now = datetime.datetime.now()
    from subs_func import lambdifysubs_subsonly
    matrix2 = lambdifysubs_subsonly(matrix_f, sortedvars, replacedict)
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
