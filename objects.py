class Point(object):
    def __init__(self):
        self.links = []
        self.active = False
        
    def link(self,point,highlight = False):
        """ Create the link on both sides """
        new_link = Link(self,other,highlight)
        self.links.append(new_link)
        other.links.append(new_link)

    def __del__(self):
        """ Do some cleanup """
        for link in links:
            del link

class Link(object):
    def __init__(self,point1,point2,highlight):
        self.points = [point1,point2]
        self.highlight = highlight
