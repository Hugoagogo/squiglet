## Standard Imports
from __future__ import division
from sys import stdout
from math import pi
import random
import Tkinter, tkFileDialog, tkMessageBox

## Custom Imports
import __init__ as squiglet
import util

## Pyglet Imports
from pyglet import app, clock, graphics, gl
from pyglet.window import key, Window, mouse
from pyglet.window.key import symbol_string

help = """
Create a point\tLeft Click
Clear active point\tRight Click
Close loop\tMiddle Click
Delete active point\tDelete
Clear all points\tCTRL-D
Move a point\tClick and drag

Save using\tCTRL-S
Load using\tCTRL-L

Open this help file\tF1 or CTRL-H
"""

SQUARE_SIZE = 3

SNAP_DIST = .4

AA_SAMPLES = 4

POINT_DELTAS = [
    (+SQUARE_SIZE,+SQUARE_SIZE),
    (+SQUARE_SIZE,-SQUARE_SIZE),
    (-SQUARE_SIZE,-SQUARE_SIZE),
    (-SQUARE_SIZE,+SQUARE_SIZE)
    ]

LINE_COLOUR = (255,255,255)
LINE_HIGHLIGHT_COLOUR = (255,0,0)

POINT_COLOUR = (255,255,255)
POINT_ACTIVE_COLOUR = (255,255,0)
POINT_HOVER_COLOUR = (0,255,255)

GRID_ON = True
GRID_SIZE = 1
GRID_COLOUR = (75,75,75)
GRID_SNAP = True
GRID_SNAP_DIST = .15

CENTER_ON = True
CENTER_COLOUR = GRID_COLOUR

def SaveAs():
    root = Tkinter.Tk()
    root.withdraw()
    filename = tkFileDialog.asksaveasfilename(title="Save vector as",filetypes = [ ('squiglet files', '.sgl'),('all files', '.*')])
    root.quit()
    return filename
    
def LoadAs():
    root = Tkinter.Tk()
    root.withdraw()
    filename = tkFileDialog.askopenfilename(title="Load vector",filetypes = [ ('squiglet files', '.sgl'),('all files', '.*')])
    root.quit()
    return filename

def OkBox():
    root = Tkinter.Tk()
    root.withdraw()
    status = tkMessageBox.askokcancel(title="Clear all?", message="Are you sure you want to clear all points")
    root.quit()
    return status

def HelpBox():
    root = Tkinter.Tk()
    root.withdraw()
    status = tkMessageBox.showinfo(title="Help", message=help)
    root.quit()

class GameWindow(Window):
    def __init__(self, view_size=(10,10),scale=(10),*args, **kwargs):
        Window.__init__(self, *args, **kwargs)
        self.set_mouse_visible(True)
        
        self.view_scale = scale#min(self.width/view_size[0],self.height/view_size[1])
        self.view_size = view_size
        
        self.width = self.view_scale*self.view_size[0]
        self.height = self.view_scale*self.view_size[1]
        
        self.setup()
    
    def setup(self,filename=False):
        self.active_point = None
        self.first_point = None
        self.hover_point = None
        self.dragging_point = None
        
        self.vector = squiglet.Vector(LINE_HIGHLIGHT_COLOUR,filename)
    
    def on_update(self):
        pass
        
    def on_draw(self):
        self.clear()
        if CENTER_ON:
            gl.glBegin(gl.GL_POLYGON)
            for delta in POINT_DELTAS:
                gl.glColor3ub(*CENTER_COLOUR)
                gl.glVertex2f(*util.add_tup(self.vector_to_screen(0,0),delta))
                
            gl.glEnd()
        
        if GRID_ON:
            gl.glBegin(gl.GL_LINES)
            for x in range(-int(self.view_size[0]/GRID_SIZE),int(self.view_size[0]/GRID_SIZE)):
                gl.glColor3ub(*GRID_COLOUR)
                gl.glColor3ub(*GRID_COLOUR)
                gl.glVertex2f(*self.vector_to_screen(x*GRID_SIZE,-self.view_size[1]/2))
                gl.glVertex2f(*self.vector_to_screen(x*GRID_SIZE,+self.view_size[1]/2))
                
            for y in range(-int(self.view_size[1]/GRID_SIZE),int(self.view_size[1]/GRID_SIZE)):
                gl.glColor3ub(*GRID_COLOUR)
                gl.glColor3ub(*GRID_COLOUR)
                gl.glVertex2f(*self.vector_to_screen(-self.view_size[0]/2,y*GRID_SIZE))
                gl.glVertex2f(*self.vector_to_screen(+self.view_size[0]/2,y*GRID_SIZE))
            gl.glEnd()
            
            
        gl.glBegin(gl.GL_LINES)
        for link in self.vector.links:
            if link.highlight:
                gl.glColor3ub(*self.vector.colour)
                gl.glColor3ub(*self.vector.colour)
            else:
                gl.glColor3ub(*LINE_COLOUR)
                gl.glColor3ub(*LINE_COLOUR)
                
            gl.glVertex2f(*self.vector_to_screen(*link.points[0].pos))
            gl.glVertex2f(*self.vector_to_screen(*link.points[1].pos))
        gl.glEnd()
        
        for point in self.vector.points:
            gl.glBegin(gl.GL_POLYGON)
            if point == self.hover_point:
                for x in range(4): gl.glColor3ub(*POINT_HOVER_COLOUR)
            elif point == self.active_point:
                for x in range(4): gl.glColor3ub(*POINT_ACTIVE_COLOUR)
            else:
                for x in range(4): gl.glColor3ub(*POINT_COLOUR)
            for delta in POINT_DELTAS:
                gl.glVertex2f(*util.add_tup(self.vector_to_screen(*point.pos),delta))
                
            gl.glEnd()
        
    def on_mouse_motion(self, x, y, dx, dy):
        nearest, nearest_dist = self.vector.nearest_point(*self.screen_to_vector(x,y))
        if nearest_dist < SNAP_DIST:
            self.hover_point = nearest
        else:
            self.hover_point = None
            
    def on_mouse_release(self,x,y,button,modifiers):
        ## Deal in vector coords
        print (x,y),
        x,y = self.screen_to_vector(x,y)
        print (x,y)
        ## Drgging action
        if self.dragging_point:
            snap = self.snap_candidate(x,y,[self.dragging_point])
            print "SNAP",snap,
            if type(snap) == squiglet.Point:
                print "DRAGGING",self.dragging_point
                for link in self.dragging_point.links:
                    snap.link(link.other(self.dragging_point))
                self.vector.remove_point(self.dragging_point)
            else:
                if type(snap) == tuple:
                    x,y = snap
                self.dragging_point.pos = (x,y)
            self.dragging_point = None
            
        ## Normal Actions
        else:
            highlight = modifiers & key.MOD_SHIFT
            if button == mouse.LEFT:
                snap = self.snap_candidate(x,y)
                if type(snap) == squiglet.Point:
                    print "SNAP_POINT"
                    if self.active_point:
                        if modifiers & key.MOD_CTRL:
                            self.active_point.link(snap,highlight)
                        else:
                            self.active_point.unlink(snap)
                    self.active_point = snap
                    
                else:
                    print snap
                    if type(snap) == tuple:
                        print "ARG"
                        x,y = snap
                    new_point = self.vector.add_point(x,y)
                    if self.active_point:
                        new_point.link(self.active_point,highlight)
                    else:
                        self.first_point = new_point
                    self.active_point = new_point
                
            elif button == mouse.RIGHT and self.active_point:
                if not len(self.active_point.links):
                    self.vector.points.remove(self.active_point)
                self.active_point = None
                
            elif button == mouse.MIDDLE and self.active_point and self.first_point:
                self.first_point.link(self.active_point,highlight)
                self.active_point = self.first_point = None
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        x,y = self.screen_to_vector(x,y)
        if not self.dragging_point:
            nearest, nearest_dist = self.vector.nearest_point(x,y)
            if nearest_dist < SNAP_DIST:
                self.dragging_point = nearest
        else:
            snap = self.snap_candidate(x,y,[self.dragging_point])
            if type(snap) == squiglet.Point:
                print "A",snap
                self.dragging_point.pos = snap.pos
            elif type(snap) == tuple:
                print "B"
                self.dragging_point.pos = snap
            else:
                self.dragging_point.pos = (x,y)
            
    def on_key_press(self,pressed,modifiers):
        if pressed == key.S and modifiers & key.MOD_CTRL:
            path = SaveAs()
            if path:
                self.vector.save(path)
                print "Saved: %s"%(path)
            self.activate()
        elif pressed == key.L and modifiers & key.MOD_CTRL:
            path = LoadAs()
            if path:
                self.setup(path)
                print "Loaded: %s"%(path)
            self.activate()
        elif pressed == key.D and modifiers & key.MOD_CTRL:
            if OkBox():
                self.setup()
        elif (pressed == key.H and modifiers & key.MOD_CTRL) or pressed==key.F1:
            HelpBox()
        elif pressed == key.DELETE or pressed == key.BACKSPACE:
            self.vector.remove_point(self.active_point)
            self.active_point = None
            self.first_point = None

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        print "ARG"
    
    def vector_to_screen(self,x,y):
        return (
            (x*self.view_scale)+(self.width/2),
            (y*self.view_scale)+(self.height/2)
        )
        
    def screen_to_vector(self,x,y):
        return (
            (x-(self.width/2))/self.view_scale,
            (y-(self.height/2))/self.view_scale
        )
    
    def snap_candidate(self,x,y,exclude=[]):
        """ Test if there are any candidates of snap points, takes x,y in VECTOR oordinates not screen"""
        nearest, nearest_dist = self.vector.nearest_point(x,y,exclude)
        if nearest_dist < SNAP_DIST:
            return nearest
        elif (x%GRID_SIZE < GRID_SNAP_DIST or GRID_SIZE-x%GRID_SIZE < GRID_SNAP_DIST) and (y%GRID_SIZE < GRID_SNAP_DIST or GRID_SIZE-y%GRID_SIZE < GRID_SNAP_DIST):
            return int(round(x/GRID_SIZE))*GRID_SIZE, int(round(y/GRID_SIZE))*GRID_SIZE
        else:
            return None

if __name__ == '__main__':
    stdout.flush()
    win = GameWindow((20,20),scale = 25,config = gl.Config(sample_buffers=1,samples=AA_SAMPLES))
    app.run()