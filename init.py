import pygame
from pygame.locals import *
import random

#car class definition
class carOpp:
	'''
	carOpp - class which decribes the features of the cars which are coming opposite the player car
	'''
	carWidth = 40
	carHeight = 74

	def __init__(self,imagePath):
		self.isCarOpp = False #to check if a car is coming opposite
		self.carOppY = -1
		self.carOppX = 0
		self.carOpp = pygame.image.load(imagePath)
		self.crashed = False

FPS=60  #frames per second setting
fpsClock = pygame.time.Clock()

#setting score to 0
scored=0

#setting up screen parameters
width = 700
height = 600

#setting up player car image
car = pygame.image.load('images/car.png')

#setting up car parameters
carX = width/2
carY = 0.8*height
health = 1000
carWidth = 40
carHeight = 59
carVelX = 0
carVelY = 0
crashed = False

#setting up street lights
light = pygame.image.load('images/light.png')

#stating that the car hasn't hit a pothole:
potholeDash = False

#setting up boost

isBoostOpp = False #to check if boost is coming opposite
boostY = -1
boostX = 0
boost = pygame.image.load('images/petrol.png')

#initialising boost time
boostTime = 0

#setting up colours 
#            R    G    B 
GRAY     = (100, 100, 100) 
NAVYBLUE = ( 60,  60, 100) 
WHITE    = (255, 255, 255) 
RED      = (255,   0,   0) 
GREEN    = (  0, 255,   0) 
BLUE     = (  0,   0, 255) 
YELLOW   = (255, 255,   0) 
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255) 
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
LIGHTGREEN = (50, 205, 50)
LIGHTGREY = (169, 169, 169)
LIGHTRED = (190,0,0)

#setting up police car 
policeCar = carOpp('images/policeCar.png')

#setting up screen as game display
gameDisplay = pygame.display.set_mode((width,height))

#setting up road parameters
roadStartX = width/4	
roadEndX = 3*width/4-80
roadCounter = 0 # helps in scrolling... i.e making the car appear as if it is moving forward

#setting up crash cloud
cloud = pygame.image.load('images/boom.png')

#setting up crashed cars to empty list
crashedCar = None

#setting up a list of cars which crashed, but now are free
savedCar = None

#initialising police time to 0
policeTime = 0

#stating that the police haven't arrived!
policeFlag = False

#stating that the game runs by default
pause = False

#setting up delay time
delay = 100
reset = 0
