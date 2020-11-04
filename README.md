# Introduction
Functions that work with Python's sympy module.

Includes:
- solme: Functions to solve sets of equations by replacing simple constraints first. Intended to solve for steady state quickly. Currently not working properly.
- solgeneral: Functions to apply standard solution methods to functions quickly.
- subs: Alternative function for substituting variables since I find sympy.subs and sympy.evalf are sometimes a little slow.

# Solme
Nonlinear solvers solve for large sets of equations and variables at the same time. However, with a large number of variables, this doesn't work well. If the variables only appear a couple of times, we can solve out for these variables in the equations and reduce the equations down. This is what these functions do. The simplification can subsitute out variables that appear once, twice or three times. We can then try and apply the nonlinear solvers and hope they will work better.
