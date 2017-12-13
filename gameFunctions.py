import pygame, random, init
from pygame.locals import *
from init import *

pygame.init()

def resetscore():
  global scored
  scored =0

#impementing buttons in the game
def button(msg,x,y,w,h,ic,ac,action):
	'''
	use - to generate button to get message
	parameters - msg - the message displayed on the button
				 x, y - the x and y coordinates of the button rectangle
				 w,h - th ewidth and height of the button rectangle
				 ic, ac - the color of the button before and while pressing
				 action - a funciton
	return - None
	'''
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(gameDisplay,ic,(x,y,w,h))
		if click[0] == 1:
			action()
			
	else:
		pygame.draw.rect(gameDisplay,ac,(x,y,w,h))



	smallText = pygame.font.Font("freesansbold.ttf",20)
	TextSurf = smallText.render(msg, True, BLACK)
	TextRect = TextSurf.get_rect()
	TextRect.center = ((x+w/2,y+h/2))
	gameDisplay.blit(TextSurf, TextRect)

def health_remaining(health):
	'''
	use - to display car health in up-left corner
	parameters - None
	return - None
	'''
	smallText = pygame.font.Font("freesansbold.ttf",20)
	TextSurf = smallText.render("Health: "+str(health), True, BLACK)
	gameDisplay.blit(TextSurf,(0,0))

def scoreloop():
	'''
	use - to dislay the score according to othe time for which the car survives on the road
	parameters - None
	returns - None
	'''
	global scored
	scored+=1
	smallText = pygame.font.Font("freesansbold.ttf",20) 
	TextSurf = smallText.render("SCORE:"+str(scored/15),True,RED)
	gameDisplay.blit(TextSurf,(0,25))
	return (scored/15)

def scoreintro():
	'''
	use - to get the score as a function of time
	parameters - None
	returns - None
	'''
	global scored
	return (scored/15)

def highscoreloop(score):
	'''
	use - to generate score and save it in a seperate text file if it is a high score
	parameters - score : the score of our car
	return - None
	'''
	with open ('highestscore.txt','r')  as f :
		k=f.readlines()

	if(score>=int(k[0])):
		with open ('highestscore.txt','w') as f:
			f.write(str(score))
		smallText = pygame.font.Font("freesansbold.ttf",20)
		TextSurf = smallText.render("Highestscore"+str(score),True,RED)
		gameDisplay.blit(TextSurf,(500,25))
		return
	smallText = pygame.font.Font("freesansbold.ttf",20)
  	TextSurf = smallText.render("Highscore"+k[0],True,RED)
  	gameDisplay.blit(TextSurf,(500,25))

def highscoreintro(score):
	with open ('highestscore.txt','r')  as f :
		  k=f.readlines()

	if(score>int(k[0])):
		with open ('highestscore.txt','w') as f:
			f.write(str(score))
			return str(score)
	return k[0]
	
def isInContact(CarX,CarY,obstacleX,obstacleY):
	'''
	use - to check if the car crashes with another car or an object(such as a pothole), so that the car's health can be 
	reduced appropriately
	parameters - CarX,CarY : the x and y co-ordinates of the car
				 Obstacle_width,obstacle_height : the width and height of the obstacle
	return value - Boolean(True/False)
	'''
	carWidth = 40
	carHeight = 59
	obstacle_width = 45
	obstacle_height = 80

	if (CarY < obstacleY+obstacle_height and CarY > obstacleY) or ( CarY + carHeight >obstacleY and CarY + carHeight < obstacleY + obstacle_height):
		if ((CarX > obstacleX and CarX < obstacleX + obstacle_width) or (CarX+carWidth > obstacleX and CarX + carWidth < obstacleX+obstacle_width)):
			#returns true if there is a contact
			return True 
	return False

def genObstacleX(roadStartX,roadEndX):
	'''
	use - to randomly generate the x co-ordinate of the obstacle coming opposite by using random function. 
	Note - the x co-ordinate must lie within the x-coordinates of the road
	parameters -roadStartX,roadEndX: to find out where the road starts and ends
	returns - the x-coordinate
	'''
	x = random.randrange(roadStartX,roadEndX)
	return x

def checkBoundaryPos(carX, carY, roadStartX, roadEndX):
	'''
	use - to check if the car is going off the road.
	parameters - carX, carY :the x and y coordinates of the car
				roadStartX, roadEndX : the start and end positions of teh road
				leftSideWalk, rightSideWalk : the x coordinates of the side walks.
	return - position of car as string
	'''
	if (carX>roadStartX and carX<roadEndX):
		return True
	return False


def reduceHealth(health, obstacle):
	'''
	use - to reduce the health depending on what obstacle the car is getting hit by
	parameters - health of the car, the obstacle as a string('pothole'/'car'/''.....if it is an empty string, 
				health remains same)
	return  - the new health
	'''
	if obstacle == 'pothole':
		health = health-10
		return health

	elif obstacle == 'car':
		health = health-50
		return health

	elif obstacle == '':	
		return health

def message_display(gameDisplay,text):
	'''
	use - to display a message by creating a surface object on which text is rendered
	parameters - gameDisplay : the screen on which the game is being drawn
				 text : the text to be renered as a message
	return - None
	'''
	largeText = pygame.font.Font('freesansbold.ttf',115)
	TextSurf = largeText.render(text, True, BLACK)
	TextRect = TextSurf.get_rect()
	TextRect.center = ((width/2),(height/2))
	gameDisplay.blit(TextSurf, TextRect)

	pygame.display.update()
	

def crash(gameDisplay):
	'''
	use - to display that the car has crashed
	parameters -  gameDisplay : the screen on which the game is being drawn
	returns - None
	'''
	message_display(gameDisplay,'You Crashed')
	pygame.time.delay(50)




	