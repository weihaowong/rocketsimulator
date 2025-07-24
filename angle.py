#to get the angle for the rocket, we want to start from 0 to a high angle before going back to 0.
#we can use y = -cos x + 1, 0<x<pi
import sympy as sy
import numpy as np
import matplotlib.pyplot as plt
import math 

class Angle:
    def __init__(self):
        pass
    def angle_function(self, x_value):
        x = sy.symbols("x")
        y = 1.05**(x-400)
        gf = sy.diff(y, x)
        m = gf.subs(x, x_value)
        return(np.degrees(np.arctan(float(m))))


