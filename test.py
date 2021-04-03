import math

def getHigherBezierSlope(p: list, t: float):
    dxDt = 0
    dyDt = 0 
    
    # The for loop will act as our summation again.
    for i in range(len(p) - 1):
        x = p[i][0]
        y = p[i][1]
        
        nextX = p[i+1][0]
        nextY = p[i+1][1]
            
        # View the position method for binomial coefficient info.
        n = len(p) - 2
        binomialCoefficient = math.factorial(n) / (
            math.factorial(i) * math.factorial(n - i)
        )
        
        # (n + 1) restores 'n's original value, the length of p.
        qX = (n + 1) * (nextX - x)
        qY = (n + 1) * (nextY - y)

        dxDt += binomialCoefficient * (1 - t) ** (n - i) * t ** i * qX
        dyDt += binomialCoefficient * (1 - t) ** (n - i) * t ** i * qY
    
    # According to parametric differentiation, we can do the following:
    dyDx = dyDt / dxDt
        
    return (dyDt, dxDt) # NOTE: make this two variables. Prolly can just use dyDt and dxDt.


points = [[10, 0], [0, 5], [5, 8], [20, 3], [25, 5], [15, 10]]
t = 0.25

v = getHigherBezierSlope(points, t)

a = math.atan2(v[0], v[1]) * 180 / math.pi + 90

if a > 180: a -= 360

print(a)