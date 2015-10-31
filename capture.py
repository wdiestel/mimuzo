#import cProfile

import pygame
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()




class Capture(object):
    def __init__(self):
        self.size = (640,480)
        # krei surfacon
        self.display = pygame.display.set_mode(self.size,0)
        # trovu kameraon
        self.clist = pygame.camera.list_cameras()
        print self.clist
        if not self.clist:
            raise ValueError("Ne trovis kameraron.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
       

#v4l2-ctl -c exposure_auto_priority=0

        self.cam.start()
        #self.cam.set_controls(hflip=True, vflip=False)
        print self.cam.get_controls()

        # kreu surfacon por kamerao
        self.snapshot = pygame.surface.Surface(self.size,0,self.display)
        self.mirror = pygame.surface.Surface(self.size,0,self.display)

    def get_and_flip(self):
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)

        # metu bildon sur la ekranon
        self.mirror = pygame.transform.flip(self.snapshot,True,False)
        self.display.blit(self.mirror, (0,0))
        pygame.display.flip()

    def main(self):
        going = True
        clock = pygame.time.Clock()

        while going:
            clock.tick(30)

            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type==KEYDOWN and e.key ==K_ESCAPE):
                    self.cam.stop()
                    going = False
            
            self.get_and_flip()


capture = Capture()
cProfile.run('capture.main()')

