from OpenGL.GL import *
import numpy as np

MILS_PER_SEC = 1000

def draw_cartesian():
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor(1, 0, 0, 0)
    glVertex(0, 0, 0)
    glVertex(0, 1, 0)
    glColor(0, 1, 0, 0)
    glVertex(0, 0, 0)
    glVertex(0, 0, 1)
    glColor(0, 0, 1, 0)
    glVertex(0, 0, 0)
    glVertex(1, 0, 0)
    glEnd()

def draw_mesh(max_z, min_z):
    glColor3f(1,1,1)
    glBegin(GL_LINES)
    for i in np.arange(-4,4,0.5):
        glVertex3f(i,0, max_z)
        glVertex3f(i,0, min_z)

    for i in np.arange(min_z, max_z, 0.5):
        glVertex3f(-4,0,i)
        glVertex3f(4,0,i)
    glEnd()

def draw_arrow(point):
    glBegin(GL_LINES)
    glVertex3f(point[0], point[1], point[2])
    if point[0] != 0:
        glVertex3f(point[0] - 0.2, point[1] - 0.05, point[2])
    else:
        glVertex3f(point[0] - 0.08, point[1], point[2] + 1)
    glVertex3f(point[0], point[1], point[2])
    if point[0] != 0:
        glVertex3f(point[0] - 0.2, point[1] + 0.05, point[2])
    else:
        glVertex3f(point[0] + 0.08, point[1], point[2] + 1)
    glEnd()

def draw_global_cartesian():
    glColor3f(26/255, 144/255, 255/255)
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex3f(0,0,-7)
    glVertex3f(0,0,7)
    glVertex3f(-4.2,0,0)
    glVertex3f(4.2,0,0)
    #glVertex3f(0,-2,0)
    #glVertex3f(0,2,0)
    glEnd()
    draw_arrow(point=(0, 0, -7))
    draw_arrow(point=(4.2, 0, 0))
