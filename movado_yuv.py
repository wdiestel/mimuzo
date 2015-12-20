# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 14:40:44 2012
 
@author: lhilbert
"""
 
import pygame as pygame
import pygame.camera
import numpy as np
import numpy.random
 
from time import sleep

# Initialize pygame
#pygame.init()

# Initialize pygame camera module
pygame.camera.init()

class CamMoves(object):
    def __init__(self,screen_size,cam_size):
 
        # See what cameras are available
        print pygame.camera.list_cameras()
        # Which of those do you want to use?
        cam_choice = 0

         # Instantiate and start camera object
        # In the next line, you can also define the resolution
        # I was happy with the default, so I did not enter that option
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[cam_choice],cam_size,"YUV")
        # self.cam.rotation = 90
        #camera.exposure_mode = 'night'
        self.cam.start()
 
        # Get camera size
        #size = cam.get_size()
 
        # Surface to hold the camera frame
        self.cam_surface = pygame.Surface(cam_size,depth=24)
        bpp = self.cam_surface.get_bytesize()
        print("cam byte size: "+str(bpp))
        self.mirror = pygame.Surface(screen_size, depth=24)
        # Make surface compliant with display
	if pygame.display.get_init():
          self.cam_surface = self.cam_surface.convert(24)
          self.mirror = self.mirror.convert(24)

        # Array to contain and display pixel brightness differences
        self.blitting_array = np.zeros((cam_size[0],cam_size[1],3),dtype=int)
 
        # Array to keep track and plot the changes in image
        #changes_length = 1000 # How many to store?
        #changes = np.zeros(changes_length) #Preallocate array
        #changes_plot_support = np.linspace(0,size[0],changes_length)
 
        # Container array for last frame pixel values
        # The array3d returns a width*height*3 integer array
        # By specifying the second argument (2), the mean is taken over
        # the third dimension, i.e. the color channels

        self.old_array = pygame.surfarray.pixels3d(self.cam_surface)[:,:,0]
        ###self.old_array = numpy.array(self.cam_surface.get_view('R'), copy=False)
        print self.old_array.dtype

        self.position = (0,0)
        #self.screen_size = screen_size

    def get_diff(self):
        if self.cam.query_image():
            # If there is an image ready 'in' camera

#            sleep(2)
#            print self.cam_surface.get_locks()

            # Make surface from camera image
            self.cam_surface = self.cam.get_image(self.cam_surface)

#            test = pygame.surfarray.pixels3d(self.cam_surface)
#            print test
 
            # Take mean across the three color channels (RGB).
            # The pixels3d returns a width*height*3 integer array
            # By specifying the second argument (2), the mean is taken over
            # the third dimension, i.e. the color channels

            new_array = pygame.surfarray.pixels3d(self.cam_surface)[:,:,0]
            ###new_array = pygame.surfarray.array3d(self.cam_surface)[:,:,0]
            ###new_array = numpy.array(self.cam_surface.get_view('R'), copy=False)

            diff = np.zeros(new_array.shape, dtype=np.int8)
            np.subtract(new_array,self.old_array,diff)
            
           
#            diff = np.absolute(new_array-self.old_array) # absolute differences
#            diff = (new_array-self.old_array) # absolute differences

            #diff = self.old_array

#            print new_array
#            print self.old_array
#            print diff
#            sys.exit(0)

            # Store the current array as the old array for next frame
            self.old_array = new_array.copy()

            ###np.abs(diff,new_array)

            # Make surface that displays the differences
            for dd in [0,1,2]:
                # Assign for all three color channels
                #self.blitting_array[:,:,dd] = 255-diff
                self.blitting_array[:,:,dd] = 255-np.abs(diff)
#???
#            self.blitting_array[:,:] = 255-diff

            # Blit from array to the camera surface
            pygame.surfarray.blit_array(self.cam_surface,self.blitting_array)
##            pygame.surfarray.blit_array(self.mirror,self.blitting_array)

            #surface = self.mirror

            # metu bildon sur la "ekranon"
            ###self.temp = pygame.transform.rotate(self.cam_surface,90)
            pygame.transform.scale(self.cam_surface,self.mirror.get_size(),self.mirror)
##            pygame.transform.scale(self.cam_surface,self.mirror.get_size(),self.mirror)
##            self.mirror = pygame.transform.rotozoom(self.cam_surface,90,2)

            return diff

    def get_values(self,rows,cols):
        scores = pygame.Surface((cols,rows),depth=24)
        pygame.transform.scale(self.cam_surface,scores.get_size(),scores)
        scores = pygame.transform.flip(scores,True,False)
        values = pygame.surfarray.pixels3d(scores)[:,:,0]
        values[:] = 255-values
        return values
       
    def blit(self,background):
        #pygame.transform.scale(self.cam_surface,background.get_size(),background)
        #background.blit(pygame.transform.flip(self.mirror,True,False), self.position)
        background.blit(self.mirror, self.position)
    
