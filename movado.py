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
pygame.init()
 
# Initialize pygame camera module
pygame.camera.init()
 
# See what cameras are available
print pygame.camera.list_cameras()
# Which of those do you want to use?
cam_choice = 0
 
# Instantiate and start camera object
# In the next line, you can also define the resolution
# I was happy with the default, so I did not enter that option
cam = pygame.camera.Camera(pygame.camera.list_cameras()[cam_choice],(640,480),"RGB")
cam.start()
 
# Get camera size
size = cam.get_size()
 
# Clock to keep track of the frame rate
the_clock = pygame.time.Clock()
frame_rate = 30 # target frames per second
 
# Initialize a screen of same size as camera picture
screen = pygame.display.set_mode(size)
pygame.display.init()
 
# Surface to hold the camera frame
cam_surface = pygame.Surface(size)
mirror = pygame.Surface(size)
# Make surface compliant with display
cam_surface = cam_surface.convert()
mirror = mirror.convert()
# Array to contain and display pixel brightness differences
blitting_array = np.zeros((size[0],size[1],3),dtype=int)
 
# Array to keep track and plot the changes in image
changes_length = 1000 # How many to store?
changes = np.zeros(changes_length) #Preallocate array
changes_plot_support = np.linspace(0,size[0],changes_length)
 
# Container array for last frame pixel values
# The array3d returns a width*height*3 integer array
# By specifying the second argument (2), the mean is taken over
# the third dimension, i.e. the color channels
old_array = np.mean(pygame.surfarray.array3d(cam_surface),2)

    
# simple main loop of the game, run forever
run = True
while run:
 
    # frame per second control
    the_clock.tick(frame_rate)
 
    #print the_clock.get_fps() # monitor performance by fps
 
    if cam.query_image():
        # If there is an image ready 'in' camera
 
        # Make surface from camera image
        cam_surface = cam.get_image(cam_surface)
 
        # Take mean across the three color channels (RGB).
        # The pixels3d returns a width*height*3 integer array
        # By specifying the second argument (2), the mean is taken over
        # the third dimension, i.e. the color channels
        new_array = np.mean(pygame.surfarray.pixels3d(cam_surface),2)
        diff = np.abs(new_array-old_array) # absolute differences
        changes[0:-1] = changes[1:] # Move mean changes one step left
        # Insert new mean change value at the very right
        # Scale so that values are between 0 and 1
        changes[-1] = np.sum(diff[:])/(size[0]*size[1])/255.
        # Store the current array as the old array for next frame
        old_array = new_array.copy()
 
        # Make surface that displays the differences
        for dd in [0,1,2]:
            # Assign for all three color channels
            blitting_array[:,:,dd] = 255-diff
        # Blit from array to the camera surface
        pygame.surfarray.blit_array(mirror,blitting_array)

        # metu bildon sur la ekranon
        cam_surface = pygame.transform.flip(mirror,True,False)

 
        # Make point list that works in the draw.lines command
        point_list = np.vstack( \
            (changes_plot_support,(1-changes)*size[1])).transpose()
        # Draw the time course of differences into the image
        pygame.draw.lines(cam_surface,(255,0,0),False,point_list)
 
        # blit image to the display surface.
        screen.blit(cam_surface,(0,0))
 
        # Update the display
        pygame.display.flip()
