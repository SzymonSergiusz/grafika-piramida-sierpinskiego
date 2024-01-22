import math
import pygame
from PIL import Image
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

surfaces = (
    (0, 1, 2),
    (0, 1, 3),
    (0, 2, 3),
    (0, 2, 1),
    (1, 2, 3),

    (1, 2, 0),
    (1, 3, 0),
    (2, 3, 1),
    (2, 3, 0),
    (2, 1, 0),

    (3, 1, 2),
    (3, 2, 1),
    (3, 1, 0),
    (3, 0, 2),
    (3, 0, 1),
)

texture_coordinates = (
    (0, 0),
    (1, 0),
    (0.5, 1),
    (0, 0.5),
)


def solid_pyramid(punkt, level=3):
    draw_next(punkt, level)


def draw_next(vers, level):
    if level > 0:
        if czy_tekstura:
            v1, v2, v3 = trojkat_tekstura(vers)
        else:
            v1, v2, v3 = trojkat_kolor(vers)
        draw_next(v1, level - 1)
        draw_next(v2, level - 1)
        draw_next(v3, level - 1)


def loadTexture():
    path = '/Users/sergiusz/PycharmProjects/grafika-komputerowa/tekstury/D1_t.tga'
    texture = glGenTextures(1)
    glEnable(GL_TEXTURE_2D)
    # glEnable(GL_CULL_FACE)
    # glCullFace(GL_BACK)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open(path)

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )
    return texture


a = 1
h = (a * math.sqrt(3) / 3)


def trojkat_tekstura(vers):
    new_x, new_y, new_z = vers
    newH = new_y - (a * math.sqrt(6) / 3)
    v0 = (new_x, new_y, new_z)
    v1 = (new_x + h, newH, new_z + h)
    v2 = (new_x - h, newH, new_z + h)
    v3 = (new_x + h, newH, new_z - h)
    id = loadTexture()
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glBegin(GL_TRIANGLES)

    for trio in surfaces:

        for i, ver in enumerate(trio):
            glTexCoord2fv(texture_coordinates[i])

            glVertex3fv((v0, v1, v2, v3)[ver])

    glEnd()
    glDisable(GL_TEXTURE_2D)
    # glDisable(GL_CULL_FACE)
    return v1, v2, v3


def trojkat_kolor(vers):
    new_x, new_y, new_z = vers
    newH = new_y - (a * math.sqrt(6) / 3)
    v0 = (new_x, new_y, new_z)
    v1 = (new_x + h, newH, new_z + h)
    v2 = (new_x - h, newH, new_z + h)
    v3 = (new_x + h, newH, new_z - h)

    glBegin(GL_LINES)
    for trio in surfaces:
        for i, ver in enumerate(trio):
            glColor3fv((255, 0, 0))

            glVertex3fv((v0, v1, v2, v3)[ver])
    glEnd()

    glBegin(GL_TRIANGLES)
    for trio in surfaces:
        for i, ver in enumerate(trio):
            glColor3fv((1.0, 1.0, 1.0))
            glVertex3fv((v0, v1, v2, v3)[ver])
    glEnd()

    return v1, v2, v3


def obracaj(angle):
    glRotatef(angle, 0.0, 1.0, 0.0)


def light():
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)

    # Punktowe źródło światła góra prawo
    glLight(GL_LIGHT0, GL_POSITION, (1, 1, 1, 1))

    # Kierunkowe źródło światła z przodu
    glLight(GL_LIGHT1, GL_POSITION, (0, 0, 1, 0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (1, 1.0, 0.0, 1))
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


czy_tekstura = False
do_rotate = False
do_obracaj = False
if __name__ == '__main__':
    pygame.init()
    display = (1600, 1200)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)

    Sx = 1.0
    Sy = 1.0
    Sz = 1.0
    viewer = [0.0, 0.0, 0.0]
    theta = 0.0
    mouse_prev_pos = None

    angle = 20
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEWHEEL:
                print(event.x, event.y)

                if event.y == -1:
                    glScalef(Sx / 1.1, Sy / 1.1, Sz / 1.1)
                if event.y == 1:
                    glScalef(1.1 * Sx, 1.1 * Sy, 1.1 * Sz)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    czy_tekstura = not czy_tekstura

                if event.key == pygame.K_UP:
                    glRotatef(angle, 1.0, 0, 0)
                if event.key == pygame.K_DOWN:
                    glRotatef(angle, -1.0, 0, 0)
                if event.key == pygame.K_LEFT:
                    glRotatef(angle, 0.0, -1.0, 0)
                if event.key == pygame.K_RIGHT:
                    glRotatef(angle, 0.0, 1.0, 0)

                if event.unicode == "+":
                    glScalef(1.1 * Sx, 1.1 * Sy, 1.1 * Sz)

                if event.unicode == "-":
                    glScalef(Sx / 1.1, Sy / 1.1, Sz / 1.1)
                if event.unicode == 'r':
                    do_rotate = not do_rotate
                if event.unicode == 'o':
                    do_obracaj = not do_obracaj

            state = pygame.mouse.get_pressed()
            if state[0]:
                mouse_prev_pos = pygame.mouse.get_pos()
                dx, dy = pygame.mouse.get_rel()
                theta += dx * 0.003
                glRotatef(theta, 0.0, 1.0, 0)
                mouse_prev_pos = pygame.mouse.get_pos()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        light()
        solid_pyramid((0, 1, 0), 4)

        if do_obracaj:
            obracaj(0.01 * 180 / 3.14)
        if do_rotate:
            glRotatef(1, 1, 1, 1)
        pygame.display.flip()
        pygame.time.wait(10)
