#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import time
import pygame
from pygame.locals import *

import spot
import field
#from i_sine import Sine
#from i_fm import Fm
#from sonic import Sonic
from i_synth import Synth
from transmit import Transmitter
from movado import CamMoves

if not pygame.font: print('Averto, tiparoj neaktivaj')
if not pygame.mixer: print('Averto: sono malŝaltita')

cols=8
rows=6

# screen size
height = 600
width = 800

# cam size
cam_size = (640,480)


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
    instr = Synth("growl",rows,cols)
    # FIXME ne funkcias tiel, momente mem lanchu jackd kaj sonic-pi mane...
    instr.jack_in()

    tr = Transmitter(fld,instr)
    pygame.display.flip()

    moves = CamMoves((width,height),cam_size)

    # fld.setValue(1,2,1.2)

    while 10:
        clock.tick(3)

        diff = moves.get_diff()
        values = moves.get_values(rows,cols)
        print values

        fld.charge_all(values)
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

        moves.blit(screen)
        fld.blit(screen)
       
        pygame.display.flip()


# voku 'main'
if __name__ == '__main__': main()




