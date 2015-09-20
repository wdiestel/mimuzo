#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import time
import pygame
from pygame.locals import *

import spot
import field
from i_sine import Sine
from i_fm import Fm
from transmit import Transmitter

if not pygame.font: print('Averto, tiparoj neaktivaj')
if not pygame.mixer: print('Averto: sono malŝaltita')

cols=8
rows=6

height = 600
width = 800



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

    # preparu objektojn
    clock = pygame.time.Clock()
    fld = field.Field(screen,rows,cols,width,height,(200,60,90))
    instr = Fm(rows,cols)
    tr = Transmitter(fld,instr)
    pygame.display.flip()

    # fld.setValue(1,2,1.2)

    while 1:
        clock.tick(3)

        fld.propagate_all()   
        # fld.dump()

        for event in pygame.event.get():
            if event.type ==QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                # pentru...
                (x,y) = pygame.mouse.get_pos()
                c = cols * x / width
                r = rows * y / height
                fld.charge(r,c,1.0)

        # allsprites.update()
        # fld.propagate_all()   
        # fld.dump()

        # repentru
        screen.blit(bg,(0,0))
        # allsprites.draw(screen)
            
        fld.blit(screen)
        pygame.display.flip()


# voku 'main'
if __name__ == '__main__': main()




