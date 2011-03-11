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
            return ## why link to yourself
        for link in self.links:
            if point in link:
                link.highlight = highlight
                return ## Already linked so dont bother
            
        new_link = Link(self,point,highlight)
        self.links.add(new_link)
        point.links.add(new_link)
        return new_link
    
    def unlink(self,point=None):
        """ Remove links, always should be called before deleting a point """
        if point:
            for link in self.links:
                if link.other(self) == point:
                    link.kill()
                    break
        else:
            for link in self.links:
                link.other(self).links.remove(link)
            self.links.clear()

    def draw(self):
        """ Not actually Used """
        pass

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
        if self.points[0] == point:
            return self.points[1]
        elif self.points[1] == point:
            return self.points[0]
        else:
            raise ValueError("Point not in link")
    
    def kill(self):
        self.points[0].links.discard(self)
        self.points[1].links.discard(self)

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
            print "LOADING", filename

    def add_point(self, x, y):
        new_point = Point(x,y)
        self.points.add(new_point)
        return new_point
    
    def remove_point(self,point):
        point.unlink()
        self.points.discard(point)
        print self.points
        del point
    
    def nearest_point(self,*pos,**other):
        """ Return the point in vector closest to position """
        if len(pos) == 1:
            pos = pos[0]
        if "exclude" in other:
            exclude = other['exclude']
        else:
            exclude = []
        min = None
        min_dist = 1000000 ## not a great soultion but the simplest
        for point in self.points:
            if not point in exclude:
                dist = util.point_dist(point.pos,pos)
                if dist < min_dist:
                    min = point
                    min_dist = dist
            
        return min, min_dist
            
    def draw(self,scale,pos):
        LINE_COLOUR = (255,255,255)
        gl.glEnable(gl.GL_DEPTH_TEST);
        gl.glEnable(gl.GL_BLEND);
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA);

        
        gl.glEnable(gl.GL_LINE_SMOOTH);
        gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_DONT_CARE);

        gl.glBegin(gl.GL_LINES)
        for link in self.links:
            if link.highlight:
                gl.glColor3ub(*self.colour)
                gl.glColor3ub(*self.colour)
            else:
                gl.glColor3ub(*LINE_COLOUR)
                gl.glColor3ub(*LINE_COLOUR)
                
            gl.glVertex2f(*util.add_tup(pos,util.scale_tup(link.points[0].pos,scale)))
            gl.glVertex2f(*util.add_tup(pos,util.scale_tup(link.points[1].pos,scale)))
            print util.add_tup(pos,util.scale_tup(link.points[0].pos,scale))
        gl.glEnd()

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
        self.points = set()
        for point in data['pout']:
            data['pout'][point] = self.add_point(*data['pout'][point])
        for link in data['lout']:
            data['pout'][link[0][0]].link(data['pout'][link[0][1]],link[1])

    def __repr__(self):
        return "<Vector instance with %d points >" % len(self.points)