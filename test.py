import math

def getHigherBezierPosition(p: list, t: float):
    """
    Ok this math is going to kill the robot. Look here:
    https://en.wikipedia.org/wiki/B%C3%A9zier_curve#Robotics
    for the math behind what I'm about to write. 
    """
    
    # The for loop will act as our summation.        
    # Start at one, end at our given number. 
    xSum = 0
    ySum = 0
    
    # Don't subtrct one here so we can iterate through each point. 
    for i in range(len(p)):
        x = p[i][0]
        y = p[i][1]
        
        # Binomial coefficient stuff here ('n' is the 'w'):
        # https://math.stackexchange.com/questions/1713706/what-does-2-values-vertically-arranged-in-parenthesis-in-an-equation-mean
        # Remember, 'n' is NOT number of points; instead, it's the degree. This means an 'n' of five has six points.
        n = len(p) - 1
        binomialCoefficient = math.factorial(n) / (math.factorial(i) * math.factorial(n - i))
        
        xSum += binomialCoefficient * (1 - t)**(n-i) * t**i * x
        ySum += binomialCoefficient * (1 - t)**(n-i) * t**i * y
        
    return (xSum, ySum)

points = [[10,0],[0,5],[5,8],[20,3],[25,5],[15,10]]
t = 1

point = points = getHigherBezierPosition(points, t)
