## Standard Imports
from __future__ import division
from sys import stdout
from math import pi
import random

## Custom Imports
import vector
import util

## Pyglet Imports
from pyglet import app, clock, graphics, gl
from pyglet.window import key, Window, mouse
from pyglet.window.key import symbol_string

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


class GameWindow(Window):
    def __init__(self, view_size=(10,10),*args, **kwargs):
        Window.__init__(self, *args, **kwargs)
        self.set_mouse_visible(True)
        
        self.vector = vector.Vector(LINE_HIGHLIGHT_COLOUR,"test")
        self.active_point = None
        self.first_point = None
        self.hover_point = None
        
        self.view_scale = min(self.width/view_size[0],self.height/view_size[1])
        self.view_size = view_size

    def on_update(self):
        pass
        
    def on_draw(self):
        self.clear()
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
        nearest, nearest_dist = self.vector.nearest_point(self.screen_to_vector(x,y))
        if nearest_dist < SNAP_DIST:
            self.hover_point = nearest
        else:
            self.hover_point = None
    
    def on_mouse_press(self,x,y,button,modifier):
        highlight = modifier & key.MOD_SHIFT
        if button == mouse.LEFT:
            nearest, nearest_dist = self.vector.nearest_point(self.screen_to_vector(x,y))
            if nearest_dist > SNAP_DIST: 
                new_point = self.vector.add_point(*self.screen_to_vector(x,y))
                if self.active_point:
                    new_point.link(self.active_point,highlight)
                else:
                    self.first_point = new_point
                self.active_point = new_point
            else:
                if self.active_point:
                    self.active_point.link(nearest)
                self.active_point = nearest
            
        elif button == mouse.RIGHT and self.active_point:
            if not len(self.active_point.links):
                self.vector.points.remove(self.active_point)
            self.active_point = None
            
        elif button == mouse.MIDDLE and self.active_point and self.first_point:
            self.first_point.link(self.active_point,highlight)
            self.active_point = self.first_point = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass
    
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
stdout.flush()
win = GameWindow((21,21),config = gl.Config(sample_buffers=1,samples=AA_SAMPLES))
app.run()