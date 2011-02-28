import math
def point_dist(p1,p2):
    return ((p1[0]**2 + p2[0]**2)+(p1[1]**2 + p2[1]**2))*0.5
    
def generate_circle(radius,pos=(0,0),segments=10):
    positions = []
    for seg in range(segments):
        angle = seg*2*math.pi/segments
        x = math.sin(angle)*radius
        y = math.cos(angle)*radius
        positions.append((x+pos[0],y+pos[1]))
    return positions
        
    
