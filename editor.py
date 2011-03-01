from __future__ import division
from sys import stdout
from math import pi
import random
import vector

## Pyglet Imports
from pyglet import app, clock, graphics, gl
from pyglet.window import key, Window, mouse
from pyglet.window.key import symbol_string

POINT_DELTAS = [
    (+3,+3),
    (+3,-3),
    (-3,-3),
    (-3,+3)
    ]

class GameWindow(Window):
    def __init__(self, view_size=(10,10),*args, **kwargs):
        Window.__init__(self, *args, **kwargs)
        self.set_mouse_visible(True)
        self.vector = vector.Vector((255,0,0),"test")
        self.active_point = None
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
                gl.glColor3ub(*(255,255,255))
                gl.glColor3ub(*(255,255,255))
                
            gl.glVertex2f((link.points[0].x*self.view_scale)+self.width/2,(link.points[0].y*self.view_scale)+self.height/2)
            gl.glVertex2f((link.points[1].x*self.view_scale)+self.width/2,(link.points[1].y*self.view_scale)+self.height/2)
            print (link.points[0].x*self.view_scale)+self.width/2,(link.points[0].y*self.view_scale)+self.height/2
        gl.glEnd()
        
        for point in self.vector.points:
            gl.glBegin(gl.GL_POLYGON)
            if point == self.active_point:
                for x in range(4): gl.glColor3ub(*(255,125,100))
            else:
                for x in range(4): gl.glColor3ub(*(255,255,255))
            print point
            for delta in POINT_DELTAS:
                #print point.x*self.view_scale+delta[0],point.y*self.view_scale+delta[1]
                gl.glVertex2f(point.x*self.view_scale+delta[0]+self.width/2,point.y*self.view_scale+delta[1]+self.height/2)
                
            
                
            gl.glEnd()
        
    def on_mouse_motion(self, x, y, dx, dy):
        pass
    
    def on_mouse_press(self,x,y,button,modifier):
        new_point = self.vector.add_point(x,y)
        if self.active_point:
            new_point.link(active)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass
stdout.flush()
win = GameWindow((21,21))
app.run()