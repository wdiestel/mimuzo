import pygame
import math

maxval = 10

class Spot(object):
  def __init__(self,sizeX,sizeY,pos,color,value):
    self.sizeY = sizeY
    self.sizeX = sizeX
    self.color = color
    self.value = value
    self.position = pos
    self.addval = 0
    self.surface = pygame.Surface((sizeX,sizeY))
    #self.surface = self.surface.convert() # for faster blitting. 
  
  def draw(self):
    #pygame.draw.rect(self.surface,(10,10,10),(0,0,self.sizeX,self.sizeY),10)
    self.surface.fill((0,0,0))
    #if int(self.value*50) > 0:  
    radius = int(math.sqrt(min(self.sizeX,self.sizeY)*self.value))
    pygame.draw.circle(self.surface,self.color,(self.sizeX/2,self.sizeY/2),radius)
   
    # to avoid the black background, make black the transparent color:
    self.surface.set_colorkey((0,0,0))
    self.surface = self.surface.convert_alpha() 

  def setValue(self,value):
    self.value = value
    self.draw()

  def add(self,pval):
    self.addval += pval

  def update(self):
   self.value = self.value + self.addval
   self.addval = 0
   if self.value > maxval:
       self.value = maxval
   self.draw()

  def blit(self, background):
      """blit the Ball on the background"""
      background.blit(self.surface, self.position)

