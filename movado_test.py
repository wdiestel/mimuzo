#!/usr/bin/python
# -*- coding: utf-8 -*-

# import cProfile

import os, sys
import time
import pygame
from pygame.locals import *

from movado_yuv import CamMoves

if not pygame.font: print('Averto, tiparoj neaktivaj')
if not pygame.mixer: print('Averto: sono malŝaltita')

cols=4
rows=3

# screen size
height = 600
width = 800

# cam size
cam_size = (640,480)
#cam_size = (320,320)
#cam_size = (160,120)

frequence = 10 # kiom ofte en sekundo trakuri la tuton

def main():
    """ĉefa funkcio, kiu rulas ĉion"""

    # preparu ekranon
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Mimuzo')

    bg = pygame.Surface(screen.get_size())
    bg = bg.convert()
    bg.fill((230,250,160))

    screen.blit(bg,(0,0))
    # pygame.display.flip()

####
    # preparu objektojn
    clock = pygame.time.Clock()

    pygame.display.flip()

    moves = CamMoves((width,height),cam_size)

    clock.tick(frequence)
    diff = moves.get_diff() # unuan diferencbildon ignoru char chio aperas nove
#    values = moves.get_values(rows,cols)

    # fld.setValue(1,2,1.2)

    while 1:
        clock.tick(frequence)

        diff = moves.get_diff()
#        values = moves.get_values(rows,cols)
        # print values

 
        for event in pygame.event.get():
            if event.type ==QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
 
        # repentru
        screen.blit(bg,(0,0))
        # allsprites.draw(screen)

        moves.blit(screen)
        pygame.display.flip()


# voku 'main'
if __name__ == '__main__': main()




