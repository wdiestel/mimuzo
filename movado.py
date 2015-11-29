# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 14:40:44 2012
 
@author: lhilbert
"""
 
import pygame as pygame
import pygame.camera
import numpy as np
import numpy.random
 
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
        self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[cam_choice],cam_size,"RGB")
        self.cam.start()
 
        # Get camera size
        #size = cam.get_size()
 
# Clock to keep track of the frame rate
#the_clock = pygame.time.Clock()
#frame_rate = 30 # target frames per second
 
## Initialize a screen of same size as camera picture
#screen = pygame.display.set_mode(size)
#pygame.display.init()
 
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
        self.old_array = np.mean(pygame.surfarray.array3d(self.cam_surface),2)

        self.position = (0,0)
        #self.screen_size = screen_size

        
# simple main loop of the game, run forever
#run = True
#while run:
 
    # frame per second control
#    the_clock.tick(frame_rate)
 
    #print the_clock.get_fps() # monitor performance by fps
 
    def get_diff(self):
        if self.cam.query_image():
            # If there is an image ready 'in' camera
 
            # Make surface from camera image
            self.cam_surface = self.cam.get_image(self.cam_surface)
 
            # Take mean across the three color channels (RGB).
            # The pixels3d returns a width*height*3 integer array
            # By specifying the second argument (2), the mean is taken over
            # the third dimension, i.e. the color channels
            new_array = np.mean(pygame.surfarray.pixels3d(self.cam_surface),2)
            diff = np.abs(new_array-self.old_array) # absolute differences
            #changes[0:-1] = changes[1:] # Move mean changes one step left
            # Insert new mean change value at the very right
            # Scale so that values are between 0 and 1
            #changes[-1] = np.sum(diff[:])/(size[0]*size[1])/255.

            # Store the current array as the old array for next frame
            self.old_array = new_array.copy()
 
            # Make surface that displays the differences
            for dd in [0,1,2]:
                # Assign for all three color channels
                self.blitting_array[:,:,dd] = 255-diff
            
            # Blit from array to the camera surface
            pygame.surfarray.blit_array(self.cam_surface,self.blitting_array)

            #surface = self.mirror

            # metu bildon sur la "ekranon"
            #self.mirror = pygame.transform.flip(self.cam_surface,True,False)
            pygame.transform.scale(self.cam_surface,self.mirror.get_size(),self.mirror)

            return diff

    def get_values(self,rows,cols):
        scores = pygame.Surface((cols,rows),depth=24)
        pygame.transform.scale(self.cam_surface,scores.get_size(),scores)
        scores = pygame.transform.flip(scores,True,False)
        values = np.mean(pygame.surfarray.pixels3d(scores),2)
        values[:] = 255-values
        return values
       
    def blit(self,background):
        #pygame.transform.scale(self.cam_surface,background.get_size(),background)
        background.blit(pygame.transform.flip(self.mirror,True,False), self.position)
    

        # Make point list that works in the draw.lines command
       # point_list = np.vstack( \
        #    (changes_plot_support,(1-changes)*size[1])).transpose()
        # Draw the time course of differences into the image
        #pygame.draw.lines(cam_surface,(255,0,0),False,point_list)
 
        # blit image to the display surface.
        #screen.blit(cam_surface,(0,0))
 
        # Update the display
        #pygame.display.flip()
