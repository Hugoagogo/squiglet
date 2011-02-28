from __future__ import division
from sys import stdout
from math import pi
import random
import vector

## Pyglet Imports
from pyglet import app, clock, graphics, gl
from pyglet.window import key, Window, mouse
from pyglet.window.key import symbol_string

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
        
        pts = []
        col = []
        print self.vector
        for link in self.vector.links:
            pts.append(link.points[0].pos)
            pts.append(link.points[1].pos)
            if link.highlight:
                col.append(self.vector.colour)
                col.append(self.vector.colour)
            else:
                col.append((255,255,255))
                col.append((255,255,255))
        print col
        gl.glBegin(gl.GL_LINES)
        for position, color in zip(pts, col):
            gl.glColor3ub(*color)
            gl.glVertex2f((position[0]*self.view_scale)+self.width/2,(position[1]*self.view_scale)+self.height/2)
            print position
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
win = GameWindow((20,20))
app.run()