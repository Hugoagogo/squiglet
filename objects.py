import pickle

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

    def edit_draw(self):
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
        self.points = set((point1,point2))
        self.highlight = highlight

    def __contains__(self,value):
        return value in self.points

    def __repr__(self):
        return "<Link instance between %s, %s, Higlight = %s>"%tuple((map(lambda x:str(x.pos),self.points)+[str(self.highlight)]))

class Vector(object):
    def __init__(self,filename=False):
        self.points = []

        if filename:
            self.load(filename)

    def add_point(self, x,y):
        new_point = Point(x,y)
        self.points.append(new_point)
        return new_point

    @property
    def links(self):
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

## A few little Tests
##v = Vector()
##
##a = v.add_point(1,1)
##b = v.add_point(1,2)
##c = v.add_point(2,2)
##
##a.link(b)
##b.link(c)
##c.link(a)
##
##v.save("test")
##print Vector("test")

