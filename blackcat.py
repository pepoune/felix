# Blackcat
# By Thomas Portet
#
# Adapted from:
# Memory Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys, math
from pygame.locals import *



FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 1000 # size of window's width in pixels
WINDOWHEIGHT = 800 # size of windows' height in pixels
#REVEALSPEED = 8 # speed boxes' sliding reveals and covers
#BOXSIZE = 40 # size of box height & width in pixels
#GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 500 # 10 # number of columns of icons
BOARDHEIGHT = 400 # 7 # number of rows of icons
# assert (BOARDWIDTH*BOARDHEIGHT)%2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN= int((WINDOWWIDTH - (BOARDWIDTH)) / 2)
YMARGIN= int((WINDOWHEIGHT - (BOARDHEIGHT)) / 2)

NUMTYPES=10 # number of types of objects
NUMEACHTYPE=50 # number of objects of each type
NUMOBJECTS=NUMTYPES*NUMEACHTYPE # total number of objects

MINRANDOMWIDTH = min(BOARDWIDTH/40,BOARDHEIGHT/40)
MAXRANDOMWIDTH = min(BOARDWIDTH/4,BOARDHEIGHT/4)

GUESSLINEWIDTH=5 # width of the guess circle drawn by user

#            R    G    B
ALPHA=255
SILVER = (192, 192, 192)
NAVYBLUE = ( 60,  60, 100)
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)





#DARKBLUE = ( 0, 0, 128)
#TEAL = ( 0, 128, 128)
#MAROON = (128, 0, 0)
#DARKPURPLE = (128, 0, 128)
#DARKGRAY     = (80, 80, 80)
#LIME = (0,255,0)
#PURPLE   = (255,   0, 255)
#GRAY = (128, 128, 128)
#RED      = (255,   0,   0)
#GREEN    = (  0, 128,   0)
#BLUE     = (  0,   0, 255)
#YELLOW   = (255, 255,   0)
#ORANGE   = (255, 128,   0)
#CYAN     = (  0, 255, 255)

DARKBLUE = ( 0, 0, 128)
TEAL = ( 0, 128, 128)
MAROON = (128, 0, 0)
DARKPURPLE = (128, 0, 128)
DARKGRAY     = (80, 80, 80)
LIME = (0,255,0)
PURPLE   = (255,   0, 255)
GRAY = (128, 128, 128)
RED      = (255,   0,   0)
GREEN    = (  0, 128,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
CYAN     = (  0, 255, 255)





BGCOLOR=SILVER
LIGHTBGCOLOR=GRAY
BOARDCOLOR=WHITE
RADIUS=10
ELEMSELECTORSIZE=5*RADIUS
SELECTEDCOLOR=RED
LINEWIDTH=1
HIGHLIGHTCOLOR=BLUE
TEXTCOLOR=SILVER
TILECOLOR=NAVYBLUE
BUTTONCOLOR=NAVYBLUE
BASICFONTSIZE = 20

DONUT='donut'
SQUARE='square'
DIAMOND='diamond'
LINES='lines'
OVAL='oval'

ALLCOLORS=(DARKBLUE,TEAL,MAROON,DARKPURPLE,DARKGRAY,LIME,PURPLE,GRAY,RED,GREEN,BLUE,YELLOW,ORANGE,CYAN)
ALLSHAPES=(DONUT,SQUARE,DIAMOND,LINES,OVAL)

assert len(ALLCOLORS)>=NUMTYPES, "Not enough colors for so many types. Use fewer types or increase nuumber of colors"

# assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def main():
	global FPSCLOCK, DISPLAYSURF, NEW_SURF, NEW_RECT, BASICFONT
	pygame.init()
	FPSCLOCK=pygame.time.Clock()
	DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
	
	NEW_SURF, NEW_RECT = makeText('New Board', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
	selectorSurf=makeSelector(NUMTYPES)

	mousex = 0 # used to store x coordinate of mouse event
	mousey = 0 # used to store y coordinate of mouse event
	centerx=0 # used to store x coordinate on center chosen when clicking down
	centery=0 # used to store y coordinate on center chosen when clicking down
	guessRadius=0 # radius of the circle drawn by user
	updateCircles=False



    	pygame.display.set_caption('Clusterz_v02')
	
	objects=getRandomizedObjects()
	circles=range(NUMTYPES)
	for i in range(NUMTYPES):
		circles[i]=[0,0,0,0]
	guessType=0

	# print objects
		
	DISPLAYSURF.fill(BGCOLOR)
	
	#startGameAnimation(mainBoard)
	
	while True: # main game loop
					
		DISPLAYSURF.fill(BGCOLOR) # drawing the window
		drawBoard(objects)
		
		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex,mousey=event.pos
				guessRadius=distance(mousex,mousey,centerx,centery)
			elif event.type == MOUSEBUTTONDOWN:
				centerx, centery=event.pos
				if isOnBoard(centerx-XMARGIN,centery-YMARGIN): # if click on the board (don't forget to substract the margin values to be in coard coordinates)
					guessRadius=0
					updateCircles = True
				elif NEW_RECT.collidepoint(event.pos):
					objects=getRandomizedObjects()
					circles=range(NUMTYPES)
					for i in range(NUMTYPES):
						circles[i]=[0,0,0,0]
					guessType=0
			elif event.type == MOUSEBUTTONUP:
				mousex,mousey=event.pos
				guessRadius=distance(mousex,mousey,centerx,centery)
				if updateCircles:
					circles[guessType]=[centerx, centery, guessRadius,guessType]
				updateCircles = False
				if not NEW_RECT.collidepoint(event.pos): #if on New board button, don't go to the next guess type
					guessType=(guessType+1)%NUMTYPES



#		boxx, boxy = getBoxAtPixel(mousex,mousey)
#		if boxx != None and boxy != None:
#			#the mouse is currently over a box
#			if not revealedBoxes[boxx][boxy]:
#				drawHighlightBox(boxx,boxy)
#			if not revealedBoxes[boxx][boxy] and mouseClicked:
#				revealBoxesAnimation(mainBoard,[(boxx,boxy)])
#				revealedBoxes[boxx][boxy]=True # set the box as "revealed"
#				if firstSelection == None: #the current box was the first box clicked
#					firstSelection=(boxx,boxy)
#				else: #the current box was the second box clicked
					# Check if there's a match between the 2 icons
#					icon1shape, icon1color=getShapeAndColor(mainBoard,firstSelection[0], firstSelection[1])
#					icon2shape, icon2color=getShapeAndColor(mainBoard, boxx, boxy)
#
#					if icon1shape != icon2shape or icon1color != icon2color:
						# Icons don't match. Re-cover up both selections.
#						pygame.time.wait(1000) # 1000ms = 1s
#						coverBoxesAnimation(mainBoard,[(firstSelection[0],firstSelection[1]),(boxx,boxy)])
#						revealedBoxes[firstSelection[0]][firstSelection[1]]=False
#						revealedBoxes[boxx][boxy]=False
#					elif hasWon(revealedBoxes): # check if all pairs found
#						gameWonAnimation(mainBoard)
#						pygame.time.wait(2000)
#
#						# Reset the board
#						mainBoard=getRandomizedBoard()
#						revealedBoxes = generateRevealedBoxesData(False)
#
#						# Show the fully unrevealed board for a second
#						drawBoard(mainBoard, revealedBoxes)
#						pygame.display.update()
#						pygame.time.wait(1000)
#
#						# Replay the start game animation
#						startGameAnimation(mainBoard)
#					firstSelection = None

		# Redraw the screen and wait for a clock tick.
		
		if updateCircles:
			circles[guessType]=[centerx, centery, guessRadius,guessType]


		#if mouseDown:
		drawCircles(circles)
		drawSelector(selectorSurf,guessType)
		
		
		pygame.display.update()
		FPSCLOCK.tick(FPS)


def distance(x0,y0,x1,y1):
	# returns the distance between points x0,y0 and x1,y1
	return math.sqrt((x0-x1)**2+(y0-y1)**2)


def generateRevealedBoxesData(val):
	revealedBoxes = []
	for i in range(BOARDWIDTH):
		revealedBoxes.append([val]*BOARDHEIGHT)
	return revealedBoxes

def getRandomizedObjects():
	# returns the objects structure, a list of NUMTYPE lists of NUMEACHTYPE points
	objects=[]
	randomSeeds=[]
	randomWidths=[]
	for i in range(NUMTYPES):
		randomSeeds.append(getRandomizedPoint())
		randomWidths.append(getRandomizedWidth())
		objectstype=[]
		for j in range(NUMEACHTYPE):
			randx, randy =getGaussianPoint(randomSeeds[i],randomWidths[i]) # draws a point at random
			objectstype.append((randx,randy))
		objectstype=tuple(objectstype)
		objects.append(objectstype)

	# print randomWidths
			
	return tuple(objects)

def getRandomizedPoint():
	# draws points at random on the board with a uniform distributions
	x=random.randint(0,BOARDWIDTH-1)
	y=random.randint(0,BOARDHEIGHT-1)
	return x, y

def getGaussianPoint(seed,width):
	# returns a random point from a circular gaussian distribution centered on seed and with stdev width
	x=-1
	y=-1
	while not isOnBoard(x,y): # make sure that the random point lies on the board
		randtheta=random.uniform(0,2*math.pi)
		randr=random.gauss(0,width)
		x, y = polarToBoardCoords(seed,randtheta,randr)	
	return x,y

def polarToBoardCoords(P0,theta,r):
	# function that returns the board coordinates x, y of a point having coordinates theta, r in polar coordinates with P0 as origin
	x=P0[0]+int(r*math.cos(theta))
	y=P0[1]+int(r*math.sin(theta))
	return x, y

def isOnBoard(x,y):
	# tells whether point with coordinates x, y is on the board
	if (x<0 or y<0 or x>BOARDWIDTH-1 or y>BOARDHEIGHT-1):
		return False
	else:
		return True


def getRandomizedWidth():
	return random.uniform(MINRANDOMWIDTH,MAXRANDOMWIDTH)


def splitIntoGroupsOf(groupSize,theList):
	# split a list into a list of lists, where the inner lists have at most groupSize number of items
	result=[]
	for i in range(0,len(theList),groupSize):
		result.append(theList[i:i+groupSize])
	return result


def leftTopCoordsOfBox(boxx,boxy):
	# convert board coordinates to pixel coordinates
	left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
	top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
	return (left, top)


def getBoxAtPixel(x,y):
	for boxx in range(BOARDWIDTH):
		for boxy in range(BOARDHEIGHT):
			left,top=leftTopCoordsOfBox(boxx,boxy)
			boxRect=pygame.Rect(left,top,BOXSIZE,BOXSIZE)
			if boxRect.collidepoint(x,y):
				return (boxx,boxy)
	return (None,None)


def drawIcon(shape, color, boxx, boxy):
	quarter = int(BOXSIZE * 0.25) # syntactic sugar
	half =    int(BOXSIZE * 0.5)  # syntactic sugar

	left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    	# Draw the shapes
    	if shape == DONUT:
    	  	pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
    	  	pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    	elif shape == SQUARE:
    	  	pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    	elif shape == DIAMOND:
    	  	pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    	elif shape == LINES:
    		for i in range(0, BOXSIZE, 4):
    	  		pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
    	        	pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    	elif shape == OVAL:
    	    	pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def getShapeAndColor(board,boxx,boxy):
	# shape value for x,y spot is stored in board[x][y][0]
	# color value for x,y spot is stored in board[x][y][1]
	return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
	# Draws boxes being covered/revealed. "boxes" is a list
	# of two-item lists, which have the x & y spot of the box.
	for box in boxes:
        	left, top = leftTopCoordsOfBox(box[0], box[1])
        	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        	shape, color = getShapeAndColor(board, box[0], box[1])
        	drawIcon(shape, color, box[0], box[1])
        	if coverage > 0: # only draw the cover if there is an coverage
        		pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
	pygame.display.update()
	FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
	# do the boxreveal animation
	for coverage in range(BOXSIZE, (-REVEALSPEED) -1, -REVEALSPEED):
		drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
	# do the boxrcover animation
	for coverage in range(0,BOXSIZE + REVEALSPEED, REVEALSPEED):
		drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(objects):
	
	# draw the board first
	pygame.draw.rect(DISPLAYSURF, BOARDCOLOR, (XMARGIN, YMARGIN, BOARDWIDTH, BOARDHEIGHT))

	# now we'll write objects with transparency
	#objectsSurface=DISPLAYSURF.convert_alpha()

	for objecttype in range(NUMTYPES):
		for objectid in range(NUMEACHTYPE):
			pygame.draw.circle(DISPLAYSURF, ALLCOLORS[objecttype], (XMARGIN+objects[objecttype][objectid][0],YMARGIN+objects[objecttype][objectid][1] ), RADIUS)
			pygame.draw.circle(DISPLAYSURF, BLACK, (XMARGIN+objects[objecttype][objectid][0],YMARGIN+objects[objecttype][objectid][1] ), RADIUS,LINEWIDTH)

	#DISPLAYSURF.blit(objectsSurface,(0,0))
	DISPLAYSURF.blit(NEW_SURF,NEW_RECT)

def drawCircles(circles):
	for circle in circles:
		if circle[2]>GUESSLINEWIDTH: # only draw circle if radius > line width of circle
			pygame.draw.circle(DISPLAYSURF,ALLCOLORS[circle[3]],(circle[0],circle[1]),int(circle[2]), GUESSLINEWIDTH)



def drawHighlightBox(boxx, boxy):
	left, top=leftTopCoordsOfBox(boxx,boxy)
	pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
	# randomly reveal the boxes 8 at a time
	coveredBoxes=generateRevealedBoxesData(False)
	boxes=[]
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			boxes.append( (x,y) )
	random.shuffle(boxes)
	boxGroups=splitIntoGroupsOf(8,boxes)

	drawBoard(board, coveredBoxes)
	for boxGroup in boxGroups:
		revealBoxesAnimation(board,boxGroup)
		coverBoxesAnimation(board,boxGroup)


def gameWonAnimation(board):
	# flash bg color when player has won
	coveredBoxes=generateRevealedBoxesData(True)
	color1=LIGHTBGCOLOR
	color2=BGCOLOR

	for i in range(13):
		color1, color2=color2, color1 # swap colors
		DISPLAYSURF.fill(color1)
		drawBoard(board,coveredBoxes)
		pygame.display.update()
		pygame.time.wait(300)

def hasWon(revealedBoxes):
	# return true if all boxes have been revealed
	for i in revealedBoxes:
		if False in i:
			return False
	return True

def makeText(text, color, bgcolor, top, left):
	# create the Surface and Rect objects for some text.
	textSurf = BASICFONT.render(text, True, color, bgcolor)
	textRect = textSurf.get_rect()	
	textRect.topleft = (top, left)
	return (textSurf, textRect)

def makeSelector(numtypes):
	# create the surface for the selector
	selheight=ELEMSELECTORSIZE
	selwidth=numtypes*ELEMSELECTORSIZE	
	top=YMARGIN/2
	left=(WINDOWWIDTH-selwidth)/2
	selectorSurf=pygame.Rect(left,top,selwidth,selheight)
	return selectorSurf

def drawSelector(selectorSurf,guessType):
	guesstop=selectorSurf.top
	guessleft=selectorSurf.left+guessType*ELEMSELECTORSIZE
	selectedSurf=pygame.Rect(guessleft,guesstop,ELEMSELECTORSIZE,ELEMSELECTORSIZE)
	pygame.draw.rect(DISPLAYSURF, BUTTONCOLOR,selectorSurf)# (selectorSurf.top,selectorSurf.left,selectorSurf.height,selectorSurf.width))
	pygame.draw.rect(DISPLAYSURF,SELECTEDCOLOR,selectedSurf)

	for i in range(NUMTYPES):
		xcenter=int(selectorSurf.left+(i+0.5)*ELEMSELECTORSIZE)
		ycenter=selectorSurf.top+ELEMSELECTORSIZE/2
		pygame.draw.circle(DISPLAYSURF, ALLCOLORS[i], (xcenter,ycenter), RADIUS)
		pygame.draw.circle(DISPLAYSURF, BLACK, (xcenter,ycenter ), RADIUS,LINEWIDTH)







if __name__ == '__main__':
	main()


