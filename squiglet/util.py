import math
import operator

def point_dist(p1,p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
    
def generate_circle(radius,pos=(0,0),segments=10):
    positions = []
    for seg in range(segments):
        angle = seg*2*math.pi/segments
        x = math.sin(angle)*radius
        y = math.cos(angle)*radius
        positions.append((x+pos[0],y+pos[1]))
    return positions
        
    
def add_tup(t1,t2):
    return tuple(map(operator.add, t1,t2))
    
def multiply_tup(t1,t2):
    return tuple(map(operator.mul, t1,t2))

def scale_tup(t,scale):
    return (t[0]*scale,t[1]*scale)
    
def eq_tup(t1,t2): ## because floating point numbers dont equal each other often
    for f1,f2 in zip(t1,t2):
        if not round(f1,6) == round(f2,6):
            return False
    return True