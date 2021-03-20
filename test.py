import math

nextDistance = 80
lastDistance = 100
offsetDistance = 4

nextAngle = 15

triangleHeight = nextDistance * math.cos(nextAngle * math.pi / 180)

print(triangleHeight)

# Awful variable name I know, hard to explain.
mainTriangleAngle = math.asin(triangleHeight / lastDistance) * 180 / math.pi

finalTriangleAngle = 180 - ((90 - mainTriangleAngle) + nextAngle)

desiredDistance=offsetDistance**2+nextDistance**2-2*offsetDistance*nextDistance*math.cos(finalTriangleAngle * math.pi / 180)
desiredDistance = math.sqrt(desiredDistance)
desiredAngle = math.asin((nextDistance * (math.sin(finalTriangleAngle * math.pi / 180))) / desiredDistance) * 180 / math.pi

print('dd ' + str(desiredDistance))
print('da ' + str(desiredAngle))
