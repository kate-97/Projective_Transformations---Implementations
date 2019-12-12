import pygame

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import math
import numpy as np
from Quaternions_Functions import *
from read_off import *
from SLerp_Functions import *
from graphics import *

name = 'seashell.off'


def graphic_animation(e2b,e2e,tm):
    pygame.init()

    display = (1000,1000)

    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(120,1.0,1,11)

    verts = None
    faces = None
    try:
        with open(name, 'r') as f:
            verts, faces = read_off(f)
    except:
        quit('Greska pri citanju fajla')

    draw_shell = glGenLists(1)
    glNewList(draw_shell, GL_COMPILE)
    Read(verts,faces)
    glEndList()

    t = 0
    tm = math.ceil((tm * MILS_PER_SEC) / 20)
    animationEnd = False

    e = e2b
    A_begin = conversionFromEulersToMatrix(e2b)
    Aa_begin = A2AngleAxis(A_begin)
    A_end = conversionFromEulersToMatrix(e2e)
    Aa_end = A2AngleAxis(A_end)

    pygame.time.set_timer(pygame.USEREVENT, 20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit("Zatvaramo aplikaciju")
            if event.type == pygame.USEREVENT and not animationEnd:
                e = find_angles(e2b = e2b,e2e = e2e,t0 = t, t = tm) # TODO:
                t += 1

            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            gluLookAt(0.01, 0.5, 2.5,
                      0, 0, 0,
                      0, 1, 0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glClearColor(179/255, 218/255, 255/255, 0)

            glPushMatrix()
            glLineWidth(20)

            glPushMatrix()
            glRotatef(Aa_begin[1] * (180 / math.pi), Aa_begin[0][0], Aa_begin[0][1], Aa_begin[0][2])
            glColor3f(255 / 255, 204 / 255, 153 / 255)
            glPushMatrix()
            glScalef(0.8, 1.2, 0.8)
            glCallList(draw_shell)
            glPopMatrix()
            draw_cartesian()
            glPopMatrix()

            glPushMatrix()
            glTranslatef(1.0,1.0,0.0)
            glRotatef(Aa_end[1] * (180 / math.pi), Aa_end[0][0], Aa_end[0][1], Aa_end[0][2])
            glColor3f(255/255,204/255, 153/255)
            glPushMatrix()
            glScalef(0.8,1.2,0.8)
            glCallList(draw_shell)
            glPopMatrix()
            draw_cartesian()
            glPopMatrix()

            glPushMatrix()
            glTranslatef(t/tm, t/tm, 0) # TODO
            A = conversionFromEulersToMatrix(e)
            Aa = A2AngleAxis(A)

            glRotatef(Aa[1] * (180/ math.pi), Aa[0][0], Aa[0][1], Aa[0][2])
            glColor3f(255/255,153/255, 102/255)
            glPushMatrix()
            glScalef(0.8,1.2,0.8)
            glCallList(draw_shell)
            glPopMatrix()
            draw_cartesian()
            glPopMatrix()
            glPopMatrix()

            pygame.display.flip()
            if t == tm:
                animationEnd = True

def main():
    e2b = (-math.pi / 6, math.pi, 0.75 * math.pi)
    e2e = (-math.pi / 2, math.pi / 3, math.pi * 1.5)
    '''
    print("Unesite redom Ojlerove uglove pocetnog polozaja (X,Y,Z, u radijanima): ")
    rolling_b = float(input())
    pitch_b = float(input())
    yaw_b = float(input())
    

    e2b = (rolling_b, pitch_b, yaw_b)

    print("Sada unesite redom Ojlerove uglove krajnjeg polozaja (X,Y,Z, u radijanima): ")
    rolling_e = float(input())
    pitch_e = float(input())
    yaw_e = float(input())

    e2e = (rolling_e, pitch_e, yaw_e)'''

    print("Sada unesite zeljeno trajanje Vase animacije (u sekundama) : ")
    t = int(input())

    graphic_animation(e2b = e2b,e2e = e2e,tm = t)


main()