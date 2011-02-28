import pickle
import pyglet
from pyglet import gl
import util

class Point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.links = set()
        self.active = False
        
    def link(self,point,highlight = False):
        """ Create the link on both sides """
        if point == self:
            return
        for link in self.links:
            if point in link:
                return ## Already linked so dont bother
            
        new_link = Link(self,point,highlight)
        self.links.add(new_link)
        point.links.add(new_link)

    def draw(self):
        pass

    def __del__(self):
        """ Do some cleanup """
        for link in self.links:
            del link

    def pos_get(self):
        return self.x,self.y
    def pos_set(self,pos):
        self.x, self.y = pos
    pos = property(pos_get,pos_set)

    def __repr__(self):
        return "<Point instance at (%f,%f)>"%self.pos
        

class Link(object):
    def __init__(self,point1,point2,highlight):
        self.points = [point1,point2]
        self.highlight = highlight
        
    def other(self,point):
        return self.points.difference((point,)).pop()

    def __contains__(self,value):
        return value in self.points

    def __repr__(self):
        return "<Link instance between %s, %s, Higlight = %s>"%tuple((map(lambda x:str(x.pos),self.points)+[str(self.highlight)]))

class Vector(object):
    def __init__(self,colour = (255,0,0),filename=False):
        self.points = set()
        self.colour = colour

        if filename:
            self.load(filename)

    def add_point(self, x,y):
        new_point = Point(x,y)
        self.points.add(new_point)
        return new_point
    
    def nearest_point(self,pos):
        """ Return the point in vector closest to position """
        min = None
        min_dist = 1000000 ## not a great soultion but the simplest
        for point in set:
            dist = util.point_dist(point.pos,pos)
            
    def draw(self):
        ## ALL OUT OF DATE AND UNUSED AS OF YET
        #pts = []
        #col = []
        #for link in self.links:
        #    pts.append(link.points[0].pos)
        #    pts.append(link.points[1].pos)
        #    if link.highlight:
        #        col.append(self.colour)
        #        col.append(self.colour)
        #    else:
        #        col.append((255,255,255))
        #        col.append((255,255,255))
        #print col
        #gl.glBegin(gl.GL_LINES)
        #for position,color in zip(pts, col):
        #    print color
        #    gl.glColor3ub(*color)
        #    gl.glVertex2f(position[0]*20,position[1]*20)
        #    print position
        #gl.glEnd()
        pass

    @property
    def links(self):
        """ all of the links (lines to be drawn) of all the vectors's points """
        links = set()
        for point in self.points:
            links |= point.links
        return links
        
    def save(self,filename):
        """ A basic wrapper of save_d to write to a file """
        f = open(filename,"wb")
        pickle.dump(self.save_d(),f)
        f.close()

    def load(self,filename):
        """ A basic wrapper of load_d to write to a file """
        f = open(filename,"rb")
        self.load_d(pickle.load(f))
        f.close()

    def save_d(self):
        """ Converts the vector to a standard python data struture """
        data = {"pout": dict((hash(x),x.pos) for x in self.points),
                "lout": [(map(hash,x.points),x.highlight) for x in self.links]
                }
        return data

    def load_d(self,data):
        """ Loads a vetor from a python datastructure NOTE wipes current Vector if called """
        for point in data['pout']:
            data['pout'][point] = self.add_point(*data['pout'][point])
        for link in data['lout']:
            data['pout'][link[0][0]].link(data['pout'][link[0][1]],link[1])

    def __repr__(self):
        return "<Vector instance with %d points >"%len(self.points)

 ##A few little Tests
v = Vector()

a = v.add_point(+10,+10)
b = v.add_point(+10,-10)
c = v.add_point(-10,-10)
d = v.add_point(-10,+10)

a.link(b)
b.link(c,True)
c.link(d,True)
d.link(a)

v.save("test")
print Vector("test")

