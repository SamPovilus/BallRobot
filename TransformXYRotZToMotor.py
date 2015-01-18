import math

#from http://cdn.intechopen.com/pdfs-wm/8875.pdf pg 211
def TransformXYRotZToMotor(x,y,rotZ,d=1,debug = False):
    m1 = (-math.sin(math.pi/3)*x+math.cos(math.pi/3)*y+d*rotZ)/3
    m2 = (                                      -1.0*y+d*rotZ)/3
    m3 = ( math.sin(math.pi/3)*x+math.cos(math.pi/3)*y+d*rotZ)/3
    if(debug):
        print "TransformXYRotZ x: " + '%+6f' %(x) + " y: " + '%+6f' % (y) + " rotZ:" + '%+6f' % (rotZ) + " m1: " + '%+5f' % (m1) + " m2: " + '%+5f' % (m2) + " m3: " + '%+5f' % m3 
    return [m1,m2,m3]

