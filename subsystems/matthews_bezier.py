"""THIS IS NOT A COMMAND GROUP.
THIS DOES NOT CHANGE ANYTHING ABOUT ANY ROBOT.
This module contains a group of bezier curve related functions to make the bezier curve drive train work better or something."""

import math
from typing import Tuple

def nDegreeBezierCurve(
    t: float,
    *points: Tuple[float]
    ) -> float:
    finalOutput = 0
    for i in range(len(points)):
        finalOutput += bniu(len(points)-1, i, t) * points[i]
    return finalOutput

def bniu(n, i, u):
    return (math.factorial(n)/(math.factorial(i) * math.factorial(n-i))) * (u ** i) * ((1 - u) ** (n - i))

def nDegreeBezierCurveDerivative(
    t: float,
    *points: Tuple[float]
    ) -> float:
    finalOutput = 0
    for i in range(len(points) - 1):
        print(i)
        finalOutput += bniu(len(points)-2, i, t) * (len(points) - 1) * (points[i + 1] - points[i])
    return finalOutput
