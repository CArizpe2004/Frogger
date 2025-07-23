from includes.utils import extractRow, getBusSprite, getSafeSpaceSprite, getBackgroundSprites
from includes.space import Space
from includes.frog import Frog
from includes.enemies import Bus, LeftRacecar, RightRacecar, Tractor, PinkCar, Turtle, Log
from includes.Queue import Queue
from includes.Node import Node
from enum import Enum
import pygame
import os
import math


#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
BACKGROUND_COLOR = (0, 0, 71)

#constants

SPRITE_PATH = os.path.join(os.getcwd(), r'includes\sprites.png')
print(SPRITE_PATH)

SCALE_FACTOR = 3

GRID_COLS = 14
GRID_ROWS = 14
TILE_WIDTH = 16 * SCALE_FACTOR
TILE_HEIGHT = 20 * SCALE_FACTOR

GRID_WIDTH = GRID_COLS * TILE_WIDTH
GRID_HEIGHT = GRID_ROWS * TILE_HEIGHT
SCREEN_WIDTH = GRID_WIDTH
SCREEN_HEIGHT = GRID_HEIGHT

JUMP_DURATION = 200 # ms
JUMP_TIMER = 0
DEATH_DURATION = 1500 # ms
DEATH_TIMER = 0
TURTLE_ANIMATION_DURATION = 300 # ms
TURTLE_TIMER = 0
dt = 16.67

LEVEL = 1

MOVEMENT_KEYS : list = [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s, pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]
inputQueue = Queue()

pygame.init()
pygame.display.set_icon(pygame.image.load(r'includes\frog.jpg'))
screen : pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Frogger')

SPRITE_SHEET : pygame.Surface = pygame.image.load(SPRITE_PATH).convert()
SPRITE_SHEET.set_colorkey(BLACK)

SAFE_ROWS = [GRID_ROWS - 8, GRID_ROWS - 2]



# sprites

frogList = extractRow(SPRITE_SHEET, 1, 1)
deathList = extractRow(SPRITE_SHEET, 1, 80, 7)
class playerSprites(Enum):
    FORWARD : pygame.Surface = frogList[0]
    FORWARD_JUMP : pygame.Surface = frogList[1]
    LEFT : pygame.Surface = frogList[2]
    LEFT_JUMP : pygame.Surface = frogList[3]
    BACKWARD : pygame.Surface = frogList[4]
    BACKWARD_JUMP : pygame.Surface = frogList[5]
    RIGHT : pygame.Surface = frogList[6]
    RIGHT_JUMP : pygame.Surface = frogList[7]
    DEATH_ONE : pygame.Surface = deathList[0]
    DEATH_TWO : pygame.Surface = deathList[1]
    DEATH_THREE : pygame.Surface = deathList[2]
    DEATH_FOUR : pygame.Surface = deathList[6]
    WIDTH = HEIGHT = 16 * SCALE_FACTOR

carList = extractRow(SPRITE_SHEET, 1, 116, 4)
class enemySprites(Enum):
    BUS : pygame.Surface = getBusSprite(SPRITE_SHEET)
    PINK_CAR : pygame.Surface = carList[0]
    LEFT_RACECAR : pygame.Surface = carList[1]
    RIGHT_RACECAR : pygame.Surface = carList[2]
    TRACTOR : pygame.Surface = carList[3]

turtleList = extractRow(SPRITE_SHEET, 1, 152, 5)
logList = extractRow(SPRITE_SHEET, 1, 134, 3)
class safeSpaces(Enum):
    safeSprite : pygame.Surface = getSafeSpaceSprite(SPRITE_SHEET)
    TURTLE1 : pygame.Surface = turtleList[0]
    TURTLE2 : pygame.Surface = turtleList[1]
    TURTLE3 : pygame.Surface = turtleList[2]
    TURTLE_SHELL : pygame.Surface = turtleList[3]
    TURTLE_SHELL_SMALL : pygame.Surface = turtleList[4]
    LOG_TAIL : pygame.Surface = logList[0]
    LOG_MIDDLE : pygame.Surface = logList[1]
    LOG_FRONT : pygame.Surface = logList[2]

backgroundList : list = getBackgroundSprites(SPRITE_SHEET)
class backgroundSprites(Enum):
    LEFT_WALL : pygame.Surface = backgroundList[0]
    TOP : pygame.Surface = backgroundList[1]
    RIGHT_WALL : pygame.Surface = backgroundList[2]
    MIDDLE_WALL : pygame.Surface = backgroundList[3]
    SHORT_WIDTH = 8 * SCALE_FACTOR
    LONG_WIDTH = 16 * SCALE_FACTOR
    SHORT_HEIGHT = 8
    LONG_HEIGHT = 24
    

def generateGrid() -> list:
    ypos = 0

    grid = []

    for y in range(GRID_ROWS):
        list = []
        xpos = 0
        for x in range(GRID_COLS):
            boardSpace : Space = Space(xpos, ypos)
            list.append(boardSpace)
            xpos += TILE_WIDTH
        grid.append(list)
        ypos += TILE_HEIGHT
    return grid

def jumpAnimation(frog : Frog, t):
    if t > .1 and t < .7:
        if frog.UP:
            frog.sprite = playerSprites.FORWARD_JUMP
        if frog.DOWN:
            frog.sprite = playerSprites.BACKWARD_JUMP
        if frog.LEFT:
            frog.sprite = playerSprites.LEFT_JUMP
        if frog.RIGHT:
            frog.sprite = playerSprites.RIGHT_JUMP
    else:
        if frog.UP:
            frog.sprite = playerSprites.FORWARD
        if frog.DOWN:
            frog.sprite = playerSprites.BACKWARD
        if frog.LEFT:
            frog.sprite = playerSprites.LEFT
        if frog.RIGHT:
            frog.sprite = playerSprites.RIGHT
    frog.pixelPos = (frog.startPos[0] + (frog.endPos[0] - frog.startPos[0]) * t, frog.startPos[1] + (frog.endPos[1] - frog.startPos[1]) * t)

def deathAnimation(frog : Frog, t):
    if t < 250:
        frog.sprite = playerSprites.DEATH_ONE
    elif t < 500:
        frog.sprite = playerSprites.DEATH_TWO
    elif t < 750:
        frog.sprite = playerSprites.DEATH_THREE
    elif t < 1000:
        frog.sprite = playerSprites.DEATH_FOUR
        
def drawEnts() -> None:
    for key in ENTITY_MAP:
        for ent in ENTITY_MAP[key]:
            if type(ent) == Turtle:
                assert isinstance(ent, Turtle)
                ent.ANIMATION_TIMER += dt
                if ent.dissapearing == False:
                    if ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 3: ent.sprite = safeSpaces.TURTLE1.value
                    elif ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 3 * 2: ent.sprite = safeSpaces.TURTLE2.value
                    elif ent.ANIMATION_TIMER < ent.ANIMATION_DURATION: ent.sprite = safeSpaces.TURTLE3.value
                    else:
                        ent.ANIMATION_TIMER = 0
                        ent.sprite = safeSpaces.TURTLE1.value
                
                else:
                    

                    if ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 12: ent.sprite = safeSpaces.TURTLE1.value
                    elif ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 12 * 2: ent.sprite = safeSpaces.TURTLE2.value
                    elif ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 12 * 3: ent.sprite = safeSpaces.TURTLE3.value
                    elif ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 12 * 4: ent.sprite = safeSpaces.TURTLE1.value
                    elif ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 12 * 5: ent.sprite = safeSpaces.TURTLE2.value
                    elif ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 12 * 6: ent.sprite = safeSpaces.TURTLE3.value
                    elif ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 12 * 7: ent.sprite = safeSpaces.TURTLE_SHELL.value
                    elif ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 12 * 8: ent.sprite = safeSpaces.TURTLE_SHELL_SMALL.value
                    elif ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 12 * 9: ent.IS_SAFE = False
                    elif ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 12 * 10: 
                        ent.sprite = safeSpaces.TURTLE_SHELL_SMALL.value
                        ent.IS_SAFE = True
                    elif ent.ANIMATION_TIMER < ent.ANIMATION_DURATION / 12 * 11: ent.sprite = safeSpaces.TURTLE_SHELL.value
                    else:
                        ent.ANIMATION_TIMER = 0
                        ent.sprite = safeSpaces.TURTLE1.value
                    

                if ent.xpos - ent.speed < -ent.WIDTH:
                    ent.xpos = GRID_WIDTH + TILE_WIDTH
                else: ent.xpos -= ent.speed

            elif ent.RIGHT:
                if ent.xpos > GRID_WIDTH and type(ent) == Log:
                    ent.xpos = -ent.WIDTH
                elif ent.xpos > GRID_WIDTH: ent.xpos = -ent.WIDTH
                else: ent.xpos += ent.speed
            else:
                if ent.xpos - ent.speed < -ent.WIDTH:
                    ent.xpos = GRID_WIDTH
                else: ent.xpos -= ent.speed
            
            if type(ent) == Turtle:
                if ent.IS_SAFE : screen.blit(ent.sprite, (ent.xpos, ent.ypos))
            elif type(ent) == Log:
                assert isinstance(ent, Log)
                for i in range(len(ent.spriteList)):
                    screen.blit(ent.spriteList[i], (ent.xpos + 48 * i, ent.ypos))
            else: 
                screen.blit(ent.sprite, (ent.xpos, ent.ypos))
                # pygame.draw.circle(screen, RED, (ent.xpos, ent.ypos), 3)
                # pygame.draw.circle(screen, RED, (ent.xpos + ent.WIDTH, ent.ypos + ent.HEIGHT), 3)

def drawBackground() -> None:
    xpos = backgroundSprites.SHORT_WIDTH.value * -1
    for i in range(5):
        screen.blit(backgroundSprites.MIDDLE_WALL.value, (xpos, 0))
        xpos += backgroundSprites.SHORT_WIDTH.value
        screen.blit(backgroundSprites.LEFT_WALL.value, (xpos, 0))
        xpos += backgroundSprites.SHORT_WIDTH.value
        screen.blit(backgroundSprites.TOP.value, (xpos, 0))
        xpos += backgroundSprites.LONG_WIDTH.value
        screen.blit(backgroundSprites.RIGHT_WALL.value, (xpos, 0))
        xpos += backgroundSprites.SHORT_WIDTH.value
        screen.blit(backgroundSprites.MIDDLE_WALL.value, (xpos, 0))
        xpos += backgroundSprites.SHORT_WIDTH.value
    screen.blit(backgroundSprites.MIDDLE_WALL.value, (xpos, 0))


def movementInput(frog: Frog, key):
    if key == pygame.K_w or key == pygame.K_UP:
        frog.move = (0, -1)
        frog.sprite = playerSprites.FORWARD
        frog.UP = True
        frog.DOWN = False
        frog.LEFT = False
        frog.RIGHT = False
        frog.jumping = True

        

    if key == pygame.K_s or key == pygame.K_DOWN:
        frog.move = (0, 1)
        frog.sprite = playerSprites.BACKWARD
        frog.UP = False
        frog.DOWN = True
        frog.LEFT = False
        frog.RIGHT = False
        frog.jumping = True

        
    if key == pygame.K_a or key == pygame.K_LEFT:
        frog.sprite = playerSprites.LEFT
        frog.move = (-1, 0)
        frog.UP = False
        frog.DOWN = False
        frog.LEFT = True
        frog.RIGHT = False
        frog.jumping = True

        
    if key == pygame.K_d or key == pygame.K_RIGHT:
        frog.sprite = playerSprites.RIGHT
        frog.move = (1, 0)
        frog.UP = False
        frog.DOWN = False
        frog.LEFT = False
        frog.RIGHT = True
        frog.jumping = True
        
    if key in MOVEMENT_KEYS and (frog.xpos + frog.move[0] < 0 or frog.xpos + frog.move[0] == GRID_COLS) == False and (frog.ypos + frog.move[1] < 0 or frog.ypos + frog.move[1] == GRID_ROWS - 1) == False:
        # frog.xpos += frog.move[0]
        # frog.ypos += frog.move[1]
        if frog.ypos + frog.move[1] > 5:
            startSpace : Space = GRID[frog.ypos][frog.xpos]
            endSpace : Space = GRID[frog.ypos + frog.move[1]][frog.xpos + frog.move[0]]
            frog.startPos = (startSpace.xpos + 2, startSpace.ypos + startSpace.HEIGHT / 2 - 24)
            frog.pixelPos = frog.startPos
            frog.endPos = (endSpace.xpos + 2, endSpace.ypos + startSpace.HEIGHT / 2 - 24)

            frog.xpos += frog.move[0]
            frog.ypos += frog.move[1]
            print(frog.xpos, frog.ypos)
            print(frog.UP, frog.DOWN, frog.LEFT, frog.RIGHT)
        else:
            print('johnson')
            frog.startPos = frog.pixelPos
            frog.endPos = (frog.startPos[0] + 48 * frog.move[0], frog.startPos[1] + 60 * frog.move[1])
            frog.xpos += frog.move[0]
            frog.ypos += frog.move[1]

    else: frog.jumping = False

   

GRID = generateGrid()

pos = (7, GRID_ROWS - 2)
frog : Frog = Frog(pos[0], pos[1], playerSprites.FORWARD)
# frog : Frog = Frog(pos[0], 5, playerSprites.FORWARD)
currentSpace : Space = GRID[frog.ypos][frog.xpos]
frog.pixelPos = (currentSpace.xpos + 2, currentSpace.ypos + currentSpace.HEIGHT / 2 - 24)



BLACK_BACKGROUND = pygame.Rect(GRID[SAFE_ROWS[0]][0].xpos, GRID[SAFE_ROWS[0]][0].ypos + GRID[SAFE_ROWS[0]][0].HEIGHT / 2, GRID_WIDTH, TILE_HEIGHT * 8)


def generateEntDict() -> dict:
    BUS_ROW = GRID_ROWS - 7
    BUS_SPACE : Space = GRID[BUS_ROW][0]
    BUS_LIST : list = []

    xpos = GRID_WIDTH / 2

    for i in range(2):
        BUS_LIST.append(Bus(xpos + 81 * i + TILE_WIDTH * 3 * i, BUS_SPACE.ypos + 15, BUS_ROW, enemySprites.BUS.value))


    LEFT_RACECAR_ROW = GRID_ROWS - 3
    LEFT_RACECAR_SPACE : Space = GRID[LEFT_RACECAR_ROW][0]
    LEFT_RACECAR_LIST : list = []
    xpos = 100

    for i in range(3):
        LEFT_RACECAR_LIST.append(LeftRacecar(xpos + 48 * i + TILE_WIDTH * 3 * i, LEFT_RACECAR_SPACE.ypos + 8, LEFT_RACECAR_ROW, enemySprites.LEFT_RACECAR.value))

    TRACTOR_ROW = GRID_ROWS - 4
    TRACTOR_SPACE : Space = GRID[TRACTOR_ROW][0]
    TRACTOR_LIST : list = []

    xpos = GRID_WIDTH - 100
    for i in range(3):
        TRACTOR_LIST.append(Tractor(xpos - 46 * i - TILE_WIDTH * 3 * i, TRACTOR_SPACE.ypos + 8, TRACTOR_ROW, enemySprites.TRACTOR.value))

    PINK_CAR_ROW = GRID_ROWS - 5
    PINK_CAR_SPACE : Space = GRID[PINK_CAR_ROW][0]
    PINK_CAR_LIST : list = []
    xpos = 200
    for i in range(4):
        PINK_CAR_LIST.append(PinkCar(xpos + 47 * i + TILE_WIDTH * 3 * i, PINK_CAR_SPACE.ypos + 8, PINK_CAR_ROW, enemySprites.PINK_CAR.value))

    RIGHT_RACECAR_ROW = GRID_ROWS - 6
    RIGHT_RACECAR_SPACE : Space = GRID[RIGHT_RACECAR_ROW][0]
    RIGHT_RACECAR_LIST : list = []
    RIGHT_RACECAR_LIST.append(RightRacecar(-150, RIGHT_RACECAR_SPACE.ypos + 8, RIGHT_RACECAR_ROW, enemySprites.RIGHT_RACECAR.value))

    FIRST_TURTLE_ROW = GRID_ROWS - 9
    FIRST_TURTLE_SPACE : Space = GRID[FIRST_TURTLE_ROW][0]
    FIRST_TURTLE_LIST : list = []

    xpos = 250
    for i in range(4):
        for j in range(3):
            if i == 2: FIRST_TURTLE_LIST.append(Turtle(xpos + 48 * j, FIRST_TURTLE_SPACE.ypos + FIRST_TURTLE_SPACE.HEIGHT / 2 - 24, FIRST_TURTLE_ROW, True, 2000, 150/60, safeSpaces.TURTLE1.value))
            else: FIRST_TURTLE_LIST.append(Turtle(xpos + 48 * j, FIRST_TURTLE_SPACE.ypos + FIRST_TURTLE_SPACE.HEIGHT / 2 - 24, FIRST_TURTLE_ROW, False, 500, 150/60, safeSpaces.TURTLE1.value))

        xpos += TILE_WIDTH + 48 * 3



    FIRST_LOG_ROW = GRID_ROWS - 10
    FIRST_LOG_SPACE : Space = GRID[FIRST_LOG_ROW][0]
    FIRST_LOG_LIST : list = []
    xpos = GRID_WIDTH - 200

    for i in range(3):
        FIRST_LOG_LIST.append(Log(xpos - 48 * i * 3 - TILE_WIDTH * 3 * i, FIRST_LOG_SPACE.ypos + FIRST_LOG_SPACE.HEIGHT / 2 - 24, FIRST_LOG_ROW, 2, 3, 
                                  [safeSpaces.LOG_TAIL.value, safeSpaces.LOG_MIDDLE.value, safeSpaces.LOG_FRONT.value]))
    
    xpos = 0
    SECOND_LOG_ROW = GRID_ROWS - 11
    SECOND_LOG_SPACE : Space = GRID[SECOND_LOG_ROW][0]
    SECOND_LOG_LIST : list = []
    xpos = GRID_WIDTH - 200

    SECOND_LOG_LIST.append(Log(xpos, SECOND_LOG_SPACE.ypos + SECOND_LOG_SPACE.HEIGHT / 2 - 24, SECOND_LOG_ROW, 4, 6, 
                                [safeSpaces.LOG_TAIL.value, safeSpaces.LOG_MIDDLE.value, safeSpaces.LOG_FRONT.value]))
    
    SECOND_TURTLE_ROW = GRID_ROWS - 12
    SECOND_TURTLE_SPACE : Space = GRID[SECOND_TURTLE_ROW][0]
    SECOND_TURTLE_LIST : list = []

    xpos = 250
    for i in range(4):
        for j in range(2):
            if i == 3: SECOND_TURTLE_LIST.append(Turtle(xpos + 48 * j, SECOND_TURTLE_SPACE.ypos + SECOND_TURTLE_SPACE.HEIGHT / 2 - 24, SECOND_TURTLE_ROW, True, 2000, 150/60, safeSpaces.TURTLE1.value))
            else: SECOND_TURTLE_LIST.append(Turtle(xpos + 48 * j, SECOND_TURTLE_SPACE.ypos + SECOND_TURTLE_SPACE.HEIGHT / 2 - 24, SECOND_TURTLE_ROW, False, 500, 150/60, safeSpaces.TURTLE1.value))

        xpos += TILE_WIDTH + 48 * 3
    
    THIRD_LOG_ROW = GRID_ROWS - 13
    THIRD_LOG_SPACE : Space = GRID[THIRD_LOG_ROW][0]
    THIRD_LOG_LIST : list = []
    xpos = GRID_WIDTH - 200

    for i in range(3):
        THIRD_LOG_LIST.append(Log(xpos - 48 * i * 3 - TILE_WIDTH * 3 * i, THIRD_LOG_SPACE.ypos + THIRD_LOG_SPACE.HEIGHT / 2 - 24, THIRD_LOG_ROW, 3, 4, 
                                  [safeSpaces.LOG_TAIL.value, safeSpaces.LOG_MIDDLE.value, safeSpaces.LOG_FRONT.value]))


    ENTITY_MAP = {
        BUS_ROW : BUS_LIST,
        LEFT_RACECAR_ROW : LEFT_RACECAR_LIST,
        RIGHT_RACECAR_ROW : RIGHT_RACECAR_LIST,
        TRACTOR_ROW : TRACTOR_LIST,
        PINK_CAR_ROW : PINK_CAR_LIST,
        FIRST_TURTLE_ROW : FIRST_TURTLE_LIST,
        FIRST_LOG_ROW : FIRST_LOG_LIST,
        SECOND_LOG_ROW : SECOND_LOG_LIST,
        SECOND_TURTLE_ROW : SECOND_TURTLE_LIST,
        THIRD_LOG_ROW : THIRD_LOG_LIST,
        6 : []
    }
    return ENTITY_MAP

def detectOverlap(list : list) -> bool:
    print('CHECKING OVERLAPS')
    for ent in list:
        overlap = 0
        overlapLeft = max(ent.xpos, frog.pixelPos[0])
        overlapTop = max(ent.ypos, frog.pixelPos[1])
        overlapRight = min(ent.xpos + ent.WIDTH, frog.pixelPos[0] + frog.WIDTH)
        overlapBottom = min(ent.ypos + ent.HEIGHT, frog.pixelPos[1] + frog.HEIGHT)

        if overlapLeft < overlapRight and overlapTop < overlapBottom:
            overlap = (overlapRight - overlapLeft) * (overlapBottom - overlapTop)

        if overlap > frog.WIDTH * frog.HEIGHT / 2: 
            print('RIDING ON WATER')
            # frog.pixelPos[0] += ent.speed * 1 if ent.RIGHT else -1
            frog.pixelPos = (frog.pixelPos[0] + ent.speed * (1 if ent.RIGHT else -1), frog.pixelPos[1])
            frog.xpos = round(frog.pixelPos[0] / 48)
            print(overlap)
            if type(ent) == Turtle:
                if ent.IS_SAFE == False: return False
            return True
    print('NO OVERLAP')
    return False
            
ENTITY_MAP : dict = generateEntDict()
CLOSEST_ENTITIES = []

for ent in ENTITY_MAP[GRID_ROWS - 9]:
    print(ent.ANIMATION_DURATION)


def drawGridLines(screen : pygame.display, circles : bool) -> None:
    for i in range(GRID_COLS):
        pygame.draw.line(screen, WHITE, ((1 + i * TILE_WIDTH), 0), ((1 + i * TILE_WIDTH), GRID_HEIGHT))

    for i in range(GRID_ROWS):
        pygame.draw.line(screen, WHITE, (0, (1 + i * TILE_HEIGHT)), (GRID_WIDTH, (1 + i * TILE_HEIGHT)))

    if circles:
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                pygame.draw.circle(screen, RED, (x * TILE_WIDTH, y * TILE_HEIGHT), 3)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key in MOVEMENT_KEYS:
                inputQueue.add(event.key)
            if event.key == pygame.K_r: 
                print(f'({frog.xpos}, {frog.ypos})')
                print(f'({frog.pixelPos[0]}, {frog.pixelPos[1]})')

    screen.fill(BACKGROUND_COLOR)  # background color


    pygame.draw.rect(screen, BLACK, BLACK_BACKGROUND)
    # drawGridLines(screen)

    for row in SAFE_ROWS:
        for space in GRID[row]:
            assert isinstance(space, Space)

            screen.blit(safeSpaces.safeSprite.value, (space.xpos, space.ypos))

    drawEnts()


    if frog.alive:
        if inputQueue.isEmpty() == False and frog.jumping == False:
            JUMP_TIMER = 0
            movementInput(frog, inputQueue.pop().getData())

        if frog.jumping:
            # print('jumping')
            JUMP_TIMER += dt
            t = JUMP_TIMER / JUMP_DURATION
            if t >= 1:
                t = 1
                frog.jumping = False
                # print('not jumping')
                if frog.ypos > 7 and frog.ypos < 12: print('CAR COLLISIONS')
                elif frog.ypos > 0 and frog.ypos < 6: 
                    print('WATER')

            jumpAnimation(frog, t)



        collisionList : list = []

        if frog.ypos < 12 and frog.ypos > 0: 
            collisionList.extend(x for x in ENTITY_MAP[frog.ypos])
            # # print(ENTITY_MAP[frog.ypos])
            # # print(x for x in ENTITY_MAP[frog.ypos])
            if frog.ypos == 11:
                collisionList.extend(x for x in ENTITY_MAP[frog.ypos - 1])
            else:
                collisionList.extend(x for x in ENTITY_MAP[frog.ypos + 1])
                # collisionList.extend(x for x in ENTITY_MAP[frog.ypos - 1])

        elif frog.ypos == 12: collisionList.extend(x for x in ENTITY_MAP[frog.ypos - 1])
        elif frog.ypos == 6: collisionList.extend(x for x in ENTITY_MAP[frog.ypos + 1])


        if frog.ypos < 12 and frog.ypos > 0: 
            for ent in collisionList:

                if type(ent) == Log or type(ent) == Turtle:

                    floatingEnts = [x for x in collisionList if type(x) == Log or type(x) == Turtle]
                 
                    if (not frog.jumping or frog.jumping == False) and detectOverlap(floatingEnts) == False:
                        # print(f'OVERLAP TOO SMALL - {overlap}')
                        frog.dying = True
                        frog.alive = False
                        frog.jumping = False

                        pygame.draw.circle(screen, RED, (ent.xpos, ent.ypos), 3)
                        pygame.draw.circle(screen, RED, (ent.xpos + ent.WIDTH, ent.ypos + ent.HEIGHT), 3)
                    else: break
                
                elif (frog.pixelPos[0] < ent.xpos + ent.WIDTH and
                      frog.pixelPos[0] + frog.WIDTH > ent.xpos and
                      frog.pixelPos[1] < ent.ypos + ent.HEIGHT and
                      frog.pixelPos[1] + frog.HEIGHT > ent.ypos):
                    frog.dying = True
                    frog.alive = False
                    frog.jumping = False

    elif frog.dying:
        
        deathAnimation(frog, DEATH_TIMER)
        DEATH_TIMER += dt

        if DEATH_TIMER >= DEATH_DURATION:
            DEATH_TIMER = 0
            frog.dying = False
            frog.dead = True
    elif frog.dead:
        frog.xpos = pos[0]
        frog.ypos = pos[1]
        currentSpace : Space = GRID[frog.ypos][frog.xpos]
        frog.pixelPos = (currentSpace.xpos + 2, currentSpace.ypos + currentSpace.HEIGHT / 2 - 24)
        frog.sprite = playerSprites.FORWARD
        frog.dead = False
        frog.alive = True
        inputQueue.clearQueue()


    drawBackground()
    screen.blit(frog.sprite.value, (frog.pixelPos[0], frog.pixelPos[1]))


    pygame.display.flip()
    clock.tick(60)

pygame.quit()