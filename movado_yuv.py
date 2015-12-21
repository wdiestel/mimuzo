# -*- coding: utf-8 -*-
"""
(c) 2015 ĉe Wolfram Diestel
laŭ GPL 2.0
"""
 
import pygame as pygame
import pygame.camera
import numpy as np
import numpy.random
 
#from time import sleep

# Preparu la kameramodulon de "pygame"
pygame.camera.init()

class CamMoves(object):
    def __init__(self,screen_size,cam_size):
 
        # Uzu la unuan troveblan kameraon
        print pygame.camera.list_cameras()
        cam_choice = 0

        # Preparu la kameraon. 
        # FARENDA: Che YUV mi fakte ne povis elekti la formaton, sed devas uzi tiun de la kamerao
        # Do eble forigu _cam_size ele la argumentoj
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[cam_choice],cam_size,"YUV")

        #camera.exposure_mode = 'night'
        self.cam.start()
 
        # Formato de la kamera-bildo
        #size = cam.get_size()
 
        # Surfaco por akcepti la bildojn el la kamerao
        self.cam_surface = pygame.Surface(cam_size,depth=24)
        bpp = self.cam_surface.get_bytesize()
        print("cam byte size: "+str(bpp))

        # Surfaco por akcepti poste la diferencbildon de movoj
        self.projection = pygame.Surface(screen_size, depth=24)
        # Konvertu laubezone al ekran-ecoj por plirapdigi montradon (blit) poste
	if pygame.display.get_init():
          self.cam_surface = self.cam_surface.convert(24)
          self.projection = self.projection.convert(24)

        # la procedo simplige estos tiel:
        # kamerao -> cam_surface -> new_array - old_array -> blitting_array -> projection -> display

        # Valoraro kun la helecdiferencoj poste uzata por la projekcio
        self.blitting_array = np.zeros((cam_size[0],cam_size[1],3),dtype=int)
 
        # Valoraro por memori la malnovajn helecerojn, preparu per la unua kamerabildo
        self.cam_surface = self.cam.get_image(self.cam_surface)
        self.old_array = pygame.surfarray.pixels3d(self.cam_surface)[:,:,0]
        ###self.old_array = numpy.array(self.cam_surface.get_view('R'), copy=False)
        print self.old_array.dtype

        self.position = (0,0)


    def get_diff(self):
        """la procedo simplige estos tiel:
        kamerao -> cam_surface -> new_array - old_array -> blitting_array -> projection -> display"""

        if self.cam.query_image(): # chu estas bildo preta en la kamerao?

            # Prenu bildon de kamerao en cam_surface kaj knovertu al valoraro
            # La unua kanalo [...,0] de YUV estas la heleco 
            self.cam_surface = self.cam.get_image(self.cam_surface)
            new_array = pygame.surfarray.pixels3d(self.cam_surface)[:,:,0]

            # Char la valoroj estas uint8, t.e. 0..255 por diferenco ni bezonas
            # valoraron kiu permesas ankaŭ negativajn nombroj (int8)
            diff = np.zeros(new_array.shape, dtype=np.int8)
            np.subtract(new_array,self.old_array,diff)
            
            # Memoru la helecon en old_array por la sekva ciklo
            self.old_array = new_array.copy()

            # Ni devos nun plenigi chiujn tri kanalojn de RGB (ruĝa-verda-blua) surfaco
            # per heleco por havi grizan bildon, flanke ni positivigas chiujn nombrojn
            for dd in [0,1,2]:
                self.blitting_array[:,:,dd] = 255-np.abs(diff)

            # Bildigu la helecvalorojn al surfaco, uzighas cam_surface, 
            # char ghi havas la taugan grandecon
            pygame.surfarray.blit_array(self.cam_surface,self.blitting_array)

            # adaptu la bildon por la "ekranon"
            pygame.transform.scale(self.cam_surface,self.projection.get_size(),self.projection)

            return diff

    def get_values(self,rows,cols):
        """prenu la valorojn de heleco por malgranda tabelo de valoroj,
        necesas, ke diff antaŭ estis trairita por ke cam_surface enhavu diferencbildon"""
        scores = pygame.Surface((cols,rows),depth=24)
        pygame.transform.scale(self.cam_surface,scores.get_size(),scores)
        scores = pygame.transform.flip(scores,True,False)
        values = pygame.surfarray.pixels3d(scores)[:,:,0]
        values[:] = 255-values
        return values
       
    def blit(self,background):
        """sendu la diferencbildon el projection al la ekranfono"""
        #background.blit(self.projection, self.position)
        background.blit(pygame.transform.flip(self.projection,True,False), self.position)
    
