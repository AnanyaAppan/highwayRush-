import pygame, gameFunctions, random
from pygame.locals import *
from gameFunctions import *

pygame.init()

#function definitions. These functions are being defined here as they will call the main gameLoop


def unpause():
	'''
	use - to resume the game
	parameters - None
	return - None
	'''
	global pause
	pause = False

def paused():
	'''
	use - to pause the game when sapce bar is pressed and to display that the game has been paused
	parameters - None
	returns - None
	'''
	global pause
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(WHITE)

		smallText = pygame.font.Font("freesansbold.ttf",80)
		TextSurf = smallText.render("paused", True, BLACK)
		TextRect = TextSurf.get_rect()
		TextRect.center = ((width/2,height/2))
		gameDisplay.blit(TextSurf, TextRect)
		button("continue",width*0.3,height *0.7,100,50,GREEN,LIGHTGREEN,unpause)
		button("quit!",width*0.7,height *0.7,100,50,RED,LIGHTRED,quit)
		pygame.display.update()

def gameintro():
	'''
	use - to generate start page
	parameters - None
	returns - None
	'''
	pygame.mixer.music.load('music/menumusic.mp3')
	pygame.mixer.music.play(-1, 0.0)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(WHITE)
		#menuImg = pygame.image.load('images/images.jpeg')
		#gameDisplay.blit(menuImg,(0,0))
		
		times=(pygame.time.get_ticks()/1000)

		smallText = pygame.font.Font("freesansbold.ttf",60)
		TextSurf = smallText.render("Highway Rush", True, BLACK)
		TextRect = TextSurf.get_rect()
		TextRect.center = ((width/2,height*0.4))
		gameDisplay.blit(TextSurf, TextRect)
		smallText = pygame.font.Font("freesansbold.ttf",40)
		TextSurf2 = smallText.render("Game rules",True,RED)
		TextRect2 = TextSurf2.get_rect()
		TextRect2.center = ((width/2,height*0.5))
		gameDisplay.blit(TextSurf2,TextRect2)
		smallText = pygame.font.Font("freesansbold.ttf",20)
		TextSurf3 = smallText.render("1.save your health to survive",True,YELLOW)
		TextRect3 = TextSurf3.get_rect()
		TextRect3.center = ((width/2,height*0.65))
		gameDisplay.blit(TextSurf3,TextRect3)
		TextSurf4 = smallText.render("2.police just follows when u dash when he is not there ",True,YELLOW)
		TextRect4 = TextSurf4.get_rect()
		TextRect4.center = ((width/2,height*0.7))
		gameDisplay.blit(TextSurf4,TextRect4)
		TextSurf4 = smallText.render("3.dash when police follows you and get yourself busted!!",True,YELLOW)
		TextRect4 = TextSurf4.get_rect()
		TextRect4.center = ((width/2,height*0.75))
		gameDisplay.blit(TextSurf4,TextRect4)
		TextSurf5 = smallText.render("hit SPACE to pause the game",True,RED)
		gameDisplay.blit(TextSurf5,(0,0))
		x=highscoreintro(scoreintro())
		TextSurf6 = smallText.render("Highest score:"+x,True,RED)
		gameDisplay.blit(TextSurf6,(500,25))
		button("go!",width*0.2,height *0.85,100,50,GREEN,LIGHTGREEN,gameLoop)
		button("quit!",width*0.7,height *0.85,100,50,RED,LIGHTRED,quit)
		pygame.display.update()

def crash(gameDisplay):
	'''
	use - to display a sreen when the car crashes
	parameters - gameDisplay : the surface on which the game is being drawn repeatedly
	returns - None
	'''
	global reset 
	reset+=1
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
	
		menuImg = pygame.image.load('images/wasted.png')
		gameDisplay.blit(menuImg,(0,0))
	
		button("play again",width*0.3,height *0.7,100,50,GREEN,LIGHTGREEN,gameLoop)
		button("quit!",width*0.7,height *0.7,100,50,RED,LIGHTRED,quit)

		pygame.display.update()

def caught():
	'''
	use - To display an appropriate screen when the car is caught by the police
	paraneters - None
	return - None
	'''
	global reset 
	reset+=1
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
	
		menuImg = pygame.image.load('images/busted.jpg')
		gameDisplay.blit(menuImg,(0,0))
	
		button("play again",width*0.3,height *0.7,100,50,GREEN,LIGHTGREEN,gameLoop)
		button("quit!",width*0.7,height *0.7,100,50,RED,LIGHTRED,quit)

		pygame.display.update()


def gameLoop():
	'''
	use - to restart the game once you get busted
	parameters - None
	return - None
	'''
	
	global scored, boostTime ,boostX, boostY,isBoostOpp, delay, savedCar, policeFlag, policeTime, clock, potholeY, potholeX, isPotholeOpp, carOpp, cars, health, carVelX, crashed, crashedCar, roadCounter,pause

	delay = 100 #delay time to run the program
	resetscore()

	pygame.mixer.music.load('music/game.mp3')
	pygame.mixer.music.play(-1, 0.0)
	
	#stating that the police haven't come yet
	policeFlag = False

	#setting up pothole

	isPotholeOpp = False #to check if a pothole is coming opposite
	potholeWidth = 70
	potholeHeight = 23
	potholeY = -1
	potholeX = 0
	pothole = pygame.image.load('images/barricade.png')

	#setting up boost

	isBoostOpp = False #to check if boost is coming opposite
	boostY = -1
	boostX = 0
	boost = pygame.image.load('images/petrol.png')

	#setting up opposite car images

	car1 = carOpp(random.choice(['images/yellowCar.png','images/blueCar.png','images/orangeCar.png','images/truck.png']))
	car2 = carOpp(random.choice(['images/yellowCar.png','images/blueCar.png','images/orangeCar.png','images/truck.png']))
	car3 = carOpp(random.choice(['images/yellowCar.png','images/blueCar.png','images/orangeCar.png','images/truck.png']))
	cars = [car1, car2, car3]

	#setting up crashed cars to empty list
	crashedCar = None

	#setting up a list of cars which crashed, but now are free
	savedCar = None

	#initialising police time to 0
	policeTime = 0

	#setting up car parameters
	carX = width/2
	carY = 0.8*height
	health = 1000
	carWidth = 40
	carHeight = 59
	carVelX = 0
	carVelY = 0
	crashed = False

	def drawScreen(gameDisplay):
		'''
		function to draw the screen repeatedly. All updates in the game will be handled by drawScreen.
		parameters: gameDisplay - the surface object on which the game is being drawn.
		return value: None 
		Note - unless pygame.display.update() is called, whatever changes are made will not be seen.
		'''
		global boostTime ,boostX, boostY,isBoostOpp, delay, potholeDash, policeFlag, savedCar, policeTime, clock, potholeY, potholeX, isPotholeOpp, carOpp, cars, health, carVelX, crashed, crashedCar, roadCounter
		
		gameDisplay.fill(LIGHTGREEN)
		
		#drawing the footpath
		pygame.draw.rect(gameDisplay, LIGHTGREY, (0,0,width/4 - 82,height))
		pygame.draw.rect(gameDisplay, LIGHTGREY, (3*width/4+55,0,width/4-55,height))
		pygame.draw.line(gameDisplay,BLACK,(width/4-82,0),(width/4-82,height),4)
		pygame.draw.line(gameDisplay,BLACK,(3*width/4+55,0),(3*width/4+55,height),4)
		
		#drawing the road
		pygame.draw.rect(gameDisplay, GRAY, (width/4,0,width/2,height))
		pygame.draw.line(gameDisplay,YELLOW,(width/4+10,0),(width/4+10,height),4)
		pygame.draw.line(gameDisplay,YELLOW,(3*width/4-10,0),(3*width/4-10,height),4)
		
		#drawing the parts which will scroll...

		if crashed:
			roadCounter = abs(roadCounter - 1)
		
		if roadCounter == 0:

			#drawing the white lines of the road
			for subHeight in range(0,height,35):
				pygame.draw.line(gameDisplay, WHITE,(width/2,subHeight),(width/2,subHeight+30),5)

			# drawing the streetlights    
			for subHeight in range(0,height,60):
				gameDisplay.blit(light,(width/4-100,subHeight))
				gameDisplay.blit(light,(3*width/4+60,subHeight))
				pygame.draw.line(gameDisplay,BLACK,(0,subHeight),(width/4-82,subHeight),2)
				pygame.draw.line(gameDisplay,BLACK,(3*width/4+55,subHeight),(width,subHeight),2)
		else:
			#drawing the white lines of the road
			for subHeight in range(10,height,35):
				pygame.draw.line(gameDisplay, WHITE,(width/2,subHeight),(width/2,subHeight+30),5)

			# drawing the streetlights   
			for subHeight in range(15,height,60):
				gameDisplay.blit(light,(width/4-100,subHeight))
				gameDisplay.blit(light,(3*width/4+60,subHeight))
				pygame.draw.line(gameDisplay,BLACK,(0,subHeight),(width/4-82,subHeight),2)
				pygame.draw.line(gameDisplay,BLACK,(3*width/4+55,subHeight),(width,subHeight),2)

		#making the crashed car move after it has crashed
		
		if crashedCar != None:
			gameDisplay.blit(crashedCar.carOpp,(crashedCar.carOppX,crashedCar.carOppY))
			if not isInContact(carX,carY,crashedCar.carOppX,crashedCar.carOppY):
				crashed = False
				crashedCar.crashed = False
				savedCar = crashedCar
				crashedCar = None
		if savedCar != None:
			if savedCar.carOppY >= height:
				savedCar.carOppY = -1
				savedCar.isCarOpp = False
			pygame.display.update()
					

		time = pygame.time.get_ticks()

		#drawing a car if time elapsed is a multiple of 5
		for i in range(len(cars)):
			if not cars[i].isCarOpp:
				if i==0 :
					cars[i].carOppX = genObstacleX(roadStartX,roadStartX+(roadEndX-roadStartX)/3-40)
				elif i==1:
					cars[i].carOppX = genObstacleX(roadStartX+(roadEndX-roadStartX)/3+40,roadStartX+2*(roadEndX-roadStartX)/3-40)
				else:
					cars[i].carOppX = genObstacleX(roadStartX+2*(roadEndX-roadStartX)/3+40, roadEndX)
				cars[i].isCarOpp = True
				if i==0:
					cars[i].carOppY = 0
				elif i==1:
					cars[i].carOppY = -20
				else:
					cars[i].carOppY = -40
			
		for i in cars:
			if i.carOppY != -1:
				gameDisplay.blit(i.carOpp,(i.carOppX,i.carOppY))
				if not i.crashed:
					i.carOppY += 15
				if i.carOppY >= height:
					i.carOppY = -1
					i.isCarOpp = False
					i.carOpp = pygame.image.load(random.choice(['images/truck.png','images/yellowCar.png','images/blueCar.png','images/orangeCar.png']))
			time += random.choice(range(10))

		#drawing pothole

		if (not isPotholeOpp) and (time/10)%7==0:
			potholeX = random.choice(range(roadStartX+(roadEndX-roadStartX)/3-20,roadStartX+(roadEndX-roadStartX)/3 +20)+range(roadStartX+2*(roadEndX-roadStartX)/3-20,roadStartX+2*(roadEndX-roadStartX)/3+20))
			potholeY = 0
			isPotholeOpp = True

		if potholeY != -1:
			gameDisplay.blit(pothole,(potholeX,potholeY))
			if not crashed:
				potholeY += 15
			if potholeY >= height:
				potholeY = -1
				isPotholeOpp = False

		#generating random posiion of boost
		if (not isBoostOpp):
			num = random.choice([0,1,2])
			boostX = cars[num].carOppX
			boostY = cars[num].carOppY - 70
			isBoostOpp = True

		if boostY != -1:
			gameDisplay.blit(boost,(boostX,boostY))
			if not crashed:
				boostY += 15
			if boostY >= height:
				boostY = -1
				isBoostOpp = False

		#to check if the car is hitting an obstacle

		if isInContact(carX,carY,potholeX, potholeY):
			health = reduceHealth(health,'pothole')
			gameDisplay.blit(cloud,(carX- carWidth/2,carY - carHeight/2))
			crashed = True
			potholeDash = True

		else: 
			potholeDash = False
			crashed = False

		# checking if car has collected boost
		if isInContact(carX,carY,boostX, boostY):
			delay = 50
			boostTime = pygame.time.get_ticks()

		#checking if car has boosted for 3 seconds
		if time-boostTime>3000:
			delay = 100

		for i in cars:

			if isInContact(carX,carY,i.carOppX,i.carOppY):
				health = reduceHealth(health, 'car')
				crashed = True
				crashedCar = i
				crashedCar.crashed = True
	
		#Once health goes below 0, game over
		if health <= 0:
			crash(gameDisplay)

		#to call the police car
		if crashed:
			policeTime = pygame.time.get_ticks()
			gameDisplay.blit(cloud,(carX- carWidth/2,carY - carHeight/2))
			if policeCar.carOppY == -1:
				policeCar.carOppY = height
				policeCar.carOppX = carX
			gameDisplay.blit(policeCar.carOpp,(policeCar.carOppX,policeCar.carOppY))

		#makes the police car stay with the player for 6 seconds after the crash
		if savedCar != None:
			
			if policeFlag:
				prevX = policeCar.carOppX
				policeCar.carOppX = carX + 40
				flag = False
				for i in cars:
					if isInContact(policeCar.carOppX, policeCar.carOppY, i.carOppX, i.carOppY):
						flag = True
						break
				if flag:
					policeCar.carOppX = prevX
				if policeCar.carOppY <= carY:
					policeCar.carOppY = -1
					policeCar.isCarOpp = False
					caught()

			if (savedCar.carOppY < height) and (time - policeTime < 6000):

					if crashed:
						policeFlag = True
						if carX < roadEndX - 40:
							policeCar.carOppX = carX + 40
						else: policeCar.carOppX = carX - 40
				
					elif (policeCar.carOppY-carY> 60):
						policeCar.carOppY -= 5
						prevX = policeCar.carOppX
						if carX < roadEndX - 40:
							policeCar.carOppX = carX + 40
						else: policeCar.carOppX = carX - 40
						flag = False
						for i in cars:
							if isInContact(policeCar.carOppX, policeCar.carOppY, i.carOppX, i.carOppY):
								flag = True
								break
						if flag:
							policeCar.carOppX = prevX
					
					else:
						if not policeFlag:
							policeCar.carOppY = carY + 60
						else:
							policeCar.carOppY = carY
						prevX = policeCar.carOppX
						if carX < roadEndX - 40:
							policeCar.carOppX = carX + 40
						else: policeCar.carOppX = carX - 40
						flag = False
						for i in cars:
							if isInContact(policeCar.carOppX, policeCar.carOppY, i.carOppX, i.carOppY):
								flag = True
								break
						if flag:
							policeCar.carOppX = prevX
			
			else:
				policeFlag = False
				if(policeCar.carOppY < height):
					prevX = policeCar.carOppX
					policeCar.carOppY += 5
					if carX < roadEndX - 40:
						policeCar.carOppX = carX + 40
					else: policeCar.carOppX = carX - 40
					flag = False
					for i in cars:
						if isInContact(policeCar.carOppX, policeCar.carOppY, i.carOppX, i.carOppY):
							flag = True
							break
					if flag:
						policeCar.carOppX = prevX
				else:
					savedCar = None
					
			gameDisplay.blit(policeCar.carOpp,(policeCar.carOppX,policeCar.carOppY))
			pygame.display.update()
		
		gameDisplay.blit(car,(carX , carY))
		pygame.display.update()

	#the actual start of the game loop
	while True:

		for event in pygame.event.get():

			if event.type == QUIT:
				pygame.quit()
				exit()

			if event.type == KEYDOWN:
				if event.key == K_RIGHT:
						carVelX += 10
				elif event.key == K_LEFT:
						carVelX -= 10
				elif event.key == pygame.K_SPACE:
					pause = True
					paused()
				elif event.key == K_UP:
				   carVelY-=10
				elif event.key == K_DOWN:
				   carVelY+=10
			
			if event.type == KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN :
					carVelX = 0
					carVelY = 0
 		
		times=(pygame.time.get_ticks()/1000)
		drawScreen(gameDisplay)
		if(pause!=True):
			scoreloop()
		  
		health_remaining(health)
		highscoreloop(scoreloop())

		if checkBoundaryPos(carX, carY, roadStartX, roadEndX + 40):
			carX += carVelX
			carY += carVelY
		else:
			if carX > roadEndX:
				carX = roadEndX - carVelX
			else: carX = roadStartX + carVelX

		if carY+carHeight > height:
			carY = height-carHeight

		if carY < 0:
			carY = 0	
		pygame.display.update()
		roadCounter = (roadCounter+1)%2
		pygame.time.delay(delay)
		fpsClock.tick(FPS)
	
gameintro()
