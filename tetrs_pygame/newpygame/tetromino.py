import random, time, pygame, sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 23
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = LIGHTBLUE
BGCOLOR = WHITE
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = BLACK
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]
                     

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

bg_image = pygame.image.load("bgimg.png")
Pause_img = pygame.image.load("Pause.png")
start_img = pygame.image.load("start.png")
meme = pygame.image.load("meme.gif")
bu = pygame.image.load("bu.gif")
ifk_p = False



def main():
    global FPSCLOCK, screen, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetris_진하림')
    screen.blit(bg_image,[0,0])
    showTextScreen('Tetris',ifk_p)
    while True: # game loop
        # if random.randint(0, 1) == 0:
        #     pygame.mixer.music.load('tetrisb.mid')
        # else:
        #     pygame.mixer.music.load('tetrisc.mid')
        # pygame.mixer.music.play(-1, 0.0)
        board = getBlankBoard()#비어 있는 보드를 만든다.
        tetrisGame(board)
        # pygame.mixer.music.stop()
        screen.blit(bg_image,[0,0])
        showTextScreen('Game Over',ifk_p)


def tetrisGame(board):
    
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)
    ck =  True


    mousex = 0
    mousey = 0

    if ck == False:
        fallingPiece = getNewPiece()
        nextPiece = getNewPiece()
    elif ck == True:
        fallingPiece = getNewPieceO()
        nextPiece = getNewPieceO()
        
    screen.blit(bg_image,[0,0])
    # screen.fill(BGCOLOR)
    while True: # game loop
        print(ck)
        if ck == False:
            
            if fallingPiece == None:
                # No falling piece in play, so start a new piece at the top
                fallingPiece = nextPiece
                nextPiece = getNewPiece()
                lastFallTime = time.time() # reset lastFallTime

                if not isValidPosition(board, fallingPiece):
                    return # can't fit a new piece on the board, so game over
            
            checkForQuit()
            
            for event in pygame.event.get(): # event handling loop
                if event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == KEYUP:
                    if (event.key == K_p):
                        ifk_p = True
                        # pygame.mixer.music.stop()
                        showTextScreen('Paused', ifk_p) # pause until a key press
                        # pygame.mixer.music.play(-1, 0.0)
                        ifk_p = False
                        lastFallTime = time.time()
                        lastMoveDownTime = time.time()
                        lastMoveSidewaysTime = time.time()
                    elif (event.key == K_LEFT or event.key == K_a):
                        movingLeft = False
                    elif (event.key == K_RIGHT or event.key == K_d):
                        movingRight = False
                    elif (event.key == K_DOWN or event.key == K_s):
                        movingDown = False


                elif event.type == KEYDOWN:
                    # moving the piece sideways
                    if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                        fallingPiece['x'] -= 1
                        movingLeft = True
                        movingRight = False
                        lastMoveSidewaysTime = time.time()

                    elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                        fallingPiece['x'] += 1
                        movingRight = True
                        movingLeft = False
                        lastMoveSidewaysTime = time.time()

                    # rotating the piece (if there is room to rotate)
                    elif (event.key == K_UP or event.key == K_w):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                        if not isValidPosition(board, fallingPiece):
                            fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    elif (event.key == K_q): # rotate the other direction
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                        if not isValidPosition(board, fallingPiece):
                            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                    # making the piece fall faster with the down key
                    elif (event.key == K_DOWN or event.key == K_s):
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjY=1):
                            fallingPiece['y'] += 1
                        lastMoveDownTime = time.time()

                    # move the current piece all the way down
                    elif event.key == K_SPACE:
                        movingDown = False
                        movingLeft = False
                        movingRight = False
                        for i in range(1, BOARDHEIGHT):
                            if not isValidPosition(board, fallingPiece, adjY=i):
                                break
                        fallingPiece['y'] += i - 1

            # handle moving the piece because of user input
            if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
                if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                lastMoveSidewaysTime = time.time()

            if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
                fallingPiece['y'] += 1
                lastMoveDownTime = time.time()

            # 떨어진 시간이 되면 피스를 떨어뜨린다. 
            if time.time() - lastFallTime > fallFreq:
                #피스착지했는지 검사 
                if not isValidPosition(board, fallingPiece, adjY=1):
                    # 착지 했다면 보드에 두기 
                    addToBoard(board, fallingPiece)
                    score += removeCompleteLines(board)
                    level, fallFreq = calculateLevelAndFallFreq(score)
                    fallingPiece = None
                else:
                    # piece did not land, just move the piece down
                    fallingPiece['y'] += 1
                    lastFallTime = time.time()

        if ck == True:
            if fallingPiece == None:
                fallingPiece = nextPiece
                nextPiece = getNewPieceO()
                lastFallTime = time.time() 

                if not isValidPosition(board, fallingPiece):
                    return
            
            checkForQuit()
            
            for event in pygame.event.get(): 
                if event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == KEYUP:
                    if (event.key == K_p):
                        ifk_p = True
                        # pygame.mixer.music.stop()
                        showTextScreen('Paused', ifk_p) # pause until a key press
                        # pygame.mixer.music.play(-1, 0.0)
                        ifk_p = False
                        lastFallTime = time.time()
                        lastMoveDownTime = time.time()
                        lastMoveSidewaysTime = time.time()
                    elif (event.key == K_LEFT or event.key == K_a):
                        movingLeft = False
                    elif (event.key == K_RIGHT or event.key == K_d):
                        movingRight = False
                    elif (event.key == K_DOWN or event.key == K_s):
                        movingDown = False


                elif event.type == KEYDOWN:
                    # moving the piece sideways
                    if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                        fallingPiece['x'] -= 1
                        movingLeft = True
                        movingRight = False
                        lastMoveSidewaysTime = time.time()

                    elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                        fallingPiece['x'] += 1
                        movingRight = True
                        movingLeft = False
                        lastMoveSidewaysTime = time.time()

                    # rotating the piece (if there is room to rotate)
                    elif (event.key == K_UP or event.key == K_w):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                        if not isValidPosition(board, fallingPiece):
                            fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    elif (event.key == K_q): # rotate the other direction
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                        if not isValidPosition(board, fallingPiece):
                            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                    # making the piece fall faster with the down key
                    elif (event.key == K_DOWN or event.key == K_s):
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjY=1):
                            fallingPiece['y'] += 1
                        lastMoveDownTime = time.time()

                    # move the current piece all the way down
                    elif event.key == K_SPACE:
                        movingDown = False
                        movingLeft = False
                        movingRight = False
                        for i in range(1, BOARDHEIGHT):
                            if not isValidPosition(board, fallingPiece, adjY=i):
                                break
                        fallingPiece['y'] += i - 1

            # handle moving the piece because of user input
            if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
                if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                lastMoveSidewaysTime = time.time()

            if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
                fallingPiece['y'] += 1
                lastMoveDownTime = time.time()

            # 떨어진 시간이 되면 피스를 떨어뜨린다. 
            if time.time() - lastFallTime > fallFreq:
                #피스착지했는지 검사 
                if not isValidPosition(board, fallingPiece, adjY=1):
                    # 착지 했다면 보드에 두기 
                    score += removeCompleteLines(board)
                    level, fallFreq = calculateLevelAndFallFreq(score)
                    fallingPiece = None
                else:
                    # piece did not land, just move the piece down
                    fallingPiece['y'] += 1
                    lastFallTime = time.time()
            # # 떨어진 시간이 되면 피스를 떨어뜨린다. 
            # if time.time() - lastFallTime > fallFreq:
            #     #피스착지했는지 검사 
            #     if not isValidPosition(board, fallingPiece, adjY=1):
            #         # 착지 했다면 보드에 두기 
            #         addToBoard(board, fallingPiece)
            #         score += removeCompleteLines(board)
            #         level, fallFreq = calculateLevelAndFallFreq(score)
            #         fallingPiece = None
            #     else:
            #         # piece did not land, just move the piece down
            #         fallingPiece['y'] += 1
            #         lastFallTime = time.time()     
                        

        # drawing everything on the screen
        # screen.fill(BGCOLOR)
        screen.blit(bg_image,[0,0])
        screen.blit(start_img,[50,20])
        drawBoard(board)
        drawStatus(score, level)
        ck = changemode(mousex,mousey,ck)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(screen, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():#창닫기 
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text , k_p):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    screen.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    screen.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, WHITE)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    screen.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        if k_p == True:
            screen.blit(Pause_img,[50,20])
        pygame.display.update()
        FPSCLOCK.tick()


def normalshowTextScreen(text):
    Self_destructiveness = 0
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    screen.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    screen.blit(titleSurf, titleRect)

    while Self_destructiveness < 200:
        Self_destructiveness += 1
        print(Self_destructiveness)
        pygame.display.update()
        FPSCLOCK.tick()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def calculateLevelAndFallFreq(score):
    level = int(score / 5) + 1
    fallFreq = 0.27 - (level * 0.02)
    # 레벨이 올라갈수록 떨어지는 속도가 빨라짐 
    return level, fallFreq


def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece


def addToBoard(board, piece):
    # 떨어진 피스 포함해서 보드를 구성 
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # 피스와 겹치는지 안겹치는지 확인(true:겹치지않을 시 , false: 겹칠 시)
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True

def removeComplete(board, piece, adjX=0, adjY=0):#shooting 게임시 사용 
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):#겹치는 순간 사라지기 
                board[piece['x']][piece['y']] = BLANK
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:#겹치는 순간 사라지기 
                board[piece['x']][piece['y']] = BLANK
                return False
    return True
                

def removeCompleteLines(board):
    # 완성된 줄은 없애고 다른 줄은 없앤다
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1 # move on to check next row up
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))


def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(screen, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(screen, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def drawBoard(board):
    # draw the border around the board
    pygame.draw.rect(screen, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 7, (BOARDHEIGHT * BOXSIZE) + 8.5), 10)

    # fill the background of the board
    pygame.draw.rect(screen, BGCOLOR, (XMARGIN, TOPMARGIN, (BOXSIZE * BOARDWIDTH)+1, BOXSIZE * BOARDHEIGHT))
    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])


def drawStatus(score, level):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    screen.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    screen.blit(levelSurf, levelRect)


def drawPiece(piece, pixelx=None, pixely=None):#퍼즐 만들기 
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))



def drawNextPiece(piece):# 다음 퍼즐 만들기 
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 150, 80)
    screen.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=80)

def changemode(mousex,mousey,ck): #모드 바꾸기 위한 버튼 제작?
    LEFT = 1
    mode1 = BASICFONT.render('Tetris', True, TEXTCOLOR)
    modeRect1 = mode1.get_rect()
    modeRect1.topleft = (WINDOWWIDTH - 125, 215)
    screen.blit(mode1, modeRect1)
    
    mode2 = BASICFONT.render('Shooting', True, TEXTCOLOR)
    modeRect2 = mode2.get_rect()
    modeRect2.topleft = (WINDOWWIDTH - 140, 295)
    screen.blit(mode2, modeRect2)

    no2 = BASICFONT.render("Don't on mouse", True, RED)
    noRect2 = no2.get_rect()
    noRect2.topleft = (WINDOWWIDTH - 190, 420)
    screen.blit(no2, noRect2)

    if (mousex > WINDOWWIDTH - 155 and mousey > 200) and (mousex < WINDOWWIDTH - 45 and mousey < 250):
        pygame.draw.rect(screen, BLUE, (WINDOWWIDTH - 155, 200, 110, 50),5)
        screen.blit(meme,[100,60])
        for event in pygame.event.get(MOUSEBUTTONDOWN):# 클릭시  tetrisgame 시작 
            if event.button == LEFT:
                ck = False
                print("no")
                return ck
                

    if (mousex > WINDOWWIDTH - 155 and mousey > 280) and (mousex < WINDOWWIDTH - 45 and mousey < 330) :
        pygame.draw.rect(screen, BLUE, (WINDOWWIDTH - 155, 280, 110, 50),5)
        for event in pygame.event.get(MOUSEBUTTONDOWN):# shooting 클릭시  shootinggame 시작 
            if event.button == LEFT:
                ck = True
                print("yes")
                return ck    

    #강제종료
    if (mousex > WINDOWWIDTH - 200 and mousey > 400) and (mousex < WINDOWWIDTH -30 and mousey < 450):
        pygame.draw.rect(screen, RED, (WINDOWWIDTH - 200, 400, 170, 50),5)
        normalshowTextScreen('NO!!!!')
        terminate()
    return ck    

def getNewPieceO():
    shape = 'O'
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': random.randint(0, len(COLORS)-1)}
    print(newPiece)
    return newPiece


    
if __name__ == '__main__':
    main()