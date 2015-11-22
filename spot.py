import pygame
import math
from observ import *

minval = 0
maxval = 10
threshold_discharge = 0.4 # je tiu valoro la makulo discharghigas, t.e. perdas sian energion 
threshold_update = 0.1 # 10% da changho inter value kaj oldvalue kauzas signalon "update"

class Spot(Observable):
  def __init__(self,sizeX,sizeY,pos,color,value):
    Observable.__init__(self)
    self.sizeY = sizeY
    self.sizeX = sizeX
    self.color = color
    self.oldvalue = value
    self.value = value
    self.position = pos
    self.addval = 0
    self.surface = pygame.Surface((sizeX,sizeY),flags=pygame.SRCALPHA)
    self.surface = self.surface.convert() # for faster blitting. 
  
  def draw(self):
    #pygame.draw.rect(self.surface,(10,10,10),(0,0,self.sizeX,self.sizeY),10)
    self.surface.fill((0,0,0))
    #if int(self.value*50) > 0:  
    radius = int(math.sqrt(min(self.sizeX,self.sizeY)*self.value))
    pygame.draw.circle(self.surface,self.color,(self.sizeX/2,self.sizeY/2),radius)
   
    # to avoid the black background, make black the transparent color:
    self.surface.set_colorkey((0,0,0))
    ### self.surface = self.surface.convert_alpha() 

  def setValue(self,value):
    self.value = value
    if self.value < minval:
      self.value = minval
    if self.value > maxval:
     self.value = maxval
    self.draw()

  def add(self,pval):
    self.addval += pval


  def update(self,r,c):
    self.value = self.value + self.addval
    self.addval = 0

    # print "value "+str(r)+", "+str(c)+": "+str(self.value)

    if self.value > maxval:
      self.value = maxval

    if self.value < minval:
      self.value = minval

    if self.value > threshold_discharge:
      self.discharge(r,c)

    if self.oldvalue > 0:
      delta = abs((self.value-self.oldvalue)/self.oldvalue)
    else:
      delta = self.value

    if delta > threshold_update:
      self.sendVal(r,c)

    self.oldvalue = self.value

    self.draw()


  def blit(self, background):
      """blit the Ball on the background"""
      background.blit(self.surface, self.position)

  def discharge(self,r,c):
    print "discharge "+str(r) + "," + str(c)
    i = threshold_discharge
    e = Event()
    e.name = "discharge"
    e.row = r
    e.col = c
    e.impuls = i
    self.fire(e)
    self.value -= i

  def sendVal(self,r,c):
    # print "update "+str(r) + "," + str(c) + ":" + str(self.value)
    #i = threshold_discharge
    e = Event()
    e.name = "update"
    e.row = r
    e.col = c
    e.value = self.value
    self.fire(e)
    #self.value -= i
