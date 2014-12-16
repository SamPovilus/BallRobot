import math

def TransformXYRotZToMotor(x,y,rotZ,d=1):
    m1 = (-math.sin(math.pi/3)*x+math.cos(math.pi/3)*y+d*rotZ)/3
    m2 = (                                      -1.0*y+     d)/3
    m3 = ( math.sin(math.pi/3)*x+math.cos(math.pi/3)*y+d*rotZ)/3
    return [m1,m2,m3]

