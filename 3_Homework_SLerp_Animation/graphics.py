from OpenGL.GL import *

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