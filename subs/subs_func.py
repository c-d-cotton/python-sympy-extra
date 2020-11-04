#!/usr/bin/env python3
"""
Includes 3 methods for substituting sympy variables from matrix
Intended as replacements for sympy.matrix.evalf(subs=dict) and sympy.matrix.subs(dict)
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

import copy
import numpy as np
import re
import sympy

# Substitute large sympy matrix quickly:{{{1
def matrixsubsquick(matrix, replacedict):
    """
    SLOWER THAN subsympymatrix_string.

    Works by first analysing which elements need to be replaced and only applying the substitution for those elements.
    Not sure why it's quicker than the sympy replace method

    """
    import sympy

    shape = matrix.shape
    lenl = shape[0] * shape[1]
    matrix = matrix.reshape(lenl, 1)

    symbols = []
    for i in range(0, lenl):
        symbols.append(matrix[i, 0].atoms(sympy.Symbol))

    allsymbols = set([sympy.Symbol(var) for var in replacedict])

    # print(replacedict)
    for i in range(0, lenl):
        for var in allsymbols:
            if var in symbols[i]:
                matrix[i, 0] = matrix[i, 0].subs(var, replacedict[str(var)])

    # for i in range(0, lenl):
    #     replacedict2 = {}
    #     for var in replacedict:
    #         if var in symbols[i]:
    #             replacedict2[var] = replacedict[var]
    #     l[i] = l[i].evalf(subs = replacedict2)

    matrix = matrix.reshape(shape[0], shape[1])


    return(matrix)


# Lambdify then apply function:{{{1
def lambdifysubs(matrix, replacedict):
    sortedvars = sorted(replacedict)
    matrix_f = sympy.lambdify(sortedvars, matrix)
    inputvalues = [replacedict[var] for var in sortedvars]
    nmatrix = matrix_f(*inputvalues)

    return(nmatrix)


def lambdifysubs_lambdifyonly(matrix, replacedict = None):

    if replacedict is None:
        # convert to sympy matrix before doing atoms
        if isinstance(matrix, np.ndarray):
            matrix = sympy.Matrix(matrix)
        elements = matrix.atoms(sympy.Symbol)
        # sortedvars = sorted([element for element in list(replacedict) if element in elements])
        sortedvars = sorted([str(element) for element in elements])
    else:
        sortedvars = sorted(replacedict)

    matrix_f = sympy.lambdify(sortedvars, matrix)

    return(matrix_f, sortedvars)


def lambdifysubs_subsonly(matrix_f, sortedvars, replacedict):
    inputvalues = [replacedict[var] for var in sortedvars]
    nmatrix = matrix_f(*inputvalues)

    return(nmatrix)

# Replace string with replacedict (auxilliary for subsympymatrix_string):{{{1
def stringsubsvars(string, replacedict):
    """
    Replace variables in a string using replacedict.
    """
    for var in replacedict:
        string = re.sub('(?<![a-zA-Z0-9_])' + var + '(?![a-zA-Z0-9_])', '' + str(replacedict[var]), string)

    return(string)


def evalstring(string):
    from numpy import exp
    from numpy import log

    num = eval(string)

    return(num)


# Substitute large sympy quickly:{{{1
def subsympymatrix_string(inputarray, replacedict, inputtype = 'sympymatrix'):
    """
    Convert sympy matrix into a string, do replace using regex and then eval result.

    Warning: I'm not sure whether the substitute will always work perfectly.
    Maybe stick with matrixsubsquick to be safe.
    """
    if inputtype == 'sympymatrix':
        string = str(inputarray)
        # Want to ignore Matrix( ... )
        string = string[7: -1]
    elif inputtype == 'listofstrings':
        # input = ['a', 'b']
        string = '[' + ', '.join(inputarray) + ']'

    string2 = stringsubsvars(string, replacedict)
    num = evalstring(string2)
    num = np.array(num)

    return(num)


def subsympymatrix_string_test():
    replacedict = {'a': 1}
    sympymatrix = sympy.Matrix([['a', '2'], ['3', '4']])
    print(subsympymatrix_string(sympymatrix, replacedict))

    listofstrings = ['a', '2', '3', '4']
    print(subsympymatrix_string(listofstrings, replacedict, inputtype = 'listofstrings'))
    

# Matrixofelements method:{{{1
def getmatrixofsympyelements(matrix):
    """
    I don't really need to convert matrix to numpy
    I do so to make reshaping easier
    """
    # convert to numpy matrix for simplicity
    matrix = np.array(matrix)
    shape = matrix.shape
    vector = np.reshape(matrix, (-1))

    vectorofelements = []
    for i in range(0, len(vector)):
        vectorofelements.append( set(str(element) for element in vector[i].atoms(sympy.Symbol)) )

    # vectorofelements.reshape(matrix, shape)
    matrixofelements = np.reshape(vectorofelements, shape)


    return(matrixofelements)


def submatrixfrommatrixofelements(matrix, replacedict, matrixofelements):
    """
    Use matrixofelements to speed up substituting out replacedict for matrix
    Should work with both numpy and sympy matrix input
    """
    matrix = copy.deepcopy(matrix)
    for i in range(len(matrix[:, 0])):
        for j in range(len(matrix[0, :])):
            if len(matrixofelements[i, j]) > 0:
                matrix[i, j] = eval( stringsubsvars(str(matrix[i, j]), {var: replacedict[var] for var in matrixofelements[i, j]}) )

    return(matrix)


def matrixofsympyelements_test():
    matrix = sympy.sympify([['a', 'b'], [3, 4]])
    matrix = np.array(matrix)
    matrixofelements = getmatrixofsympyelements(matrix)
    print(matrixofelements)
    matrixsubbed = submatrixfrommatrixofelements(matrix, {'a': 1, 'b': 2}, matrixofelements)
    print(matrixsubbed)


