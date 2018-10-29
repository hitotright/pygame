# -*- coding: UTF-8 -*-
import pygame, sys ,random

from pygame.locals import *

'''
贪吃蛇 
参考地址：https://github.com/memoiry/Snaky
'''


FPS = 5
windows_width = 640
windows_height = 480
cell_size = 40
assert windows_width % cell_size == 0,"窗口高和宽都必须可以整除格子大小"
assert windows_height % cell_size == 0,"窗口高和宽都必须可以整除格子大小"
cell_width = int(windows_width/cell_size)
cell_height = int(windows_height/cell_size)

# 定义几个颜色
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARK_GREEN = (  0, 155,   0)
DARK_GRAY  = ( 40,  40,  40)
BG_COLOR = BLACK

#操作键
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#虫头
HEAD = 0

#主函数
def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT
    pygame.init() # 模块初始化
    FPS_CLOCK = pygame.time.Clock() # 创建Pygame时钟对象
    DISPLAY_SURF = pygame.display.set_mode((windows_width, windows_height)) #
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption("Python 贪吃蛇小游戏") #设置标题

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()
#游戏主体
def runGame():
    # 蛇开始位置
    startX = random.randint(5, cell_width - 6)
    startY = random.randint(5, cell_height - 6)
    snake = [{'x': startX, 'y': startY},
                  {'x': startX - 1, 'y': startY},
                  {'x': startX - 2, 'y': startY}]
    direction = RIGHT

    #随机一个苹果
    apple = getRandomLocation(snake)

    while True: # main game loop
        pre_direction = direction
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
        # check if the worm has hit itself or the edge
        if snake[HEAD]['x'] == -1 or snake[HEAD]['x'] == cell_width or snake[HEAD]['y'] == -1 or snake[HEAD]['y'] == cell_height:
            return # game over
        for wormBody in snake[1:]:
            if wormBody['x'] == snake[HEAD]['x'] and wormBody['y'] == snake[HEAD]['y']:
                return # game over

        # check if worm has eaten an apply
        if snake[HEAD]['x'] == apple['x'] and snake[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation(snake) # set a new apple somewhere
        else:
            del snake[-1] # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if not examine_direction(direction, pre_direction):
            direction = pre_direction
        if direction == UP:
            newHead = {'x': snake[HEAD]['x'], 'y': snake[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': snake[HEAD]['x'], 'y': snake[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': snake[HEAD]['x'] - 1, 'y': snake[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': snake[HEAD]['x'] + 1, 'y': snake[HEAD]['y']}
        else:
            newHead = {'x': snake[HEAD]['x'] + 1, 'y': snake[HEAD]['y']}
        snake.insert(0, newHead)
        DISPLAY_SURF.fill(BG_COLOR)
        drawGrid()
        drawWorm(snake)
        drawApple(apple)
        drawScore(len(snake) - 3)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
        
#开始屏
def showStartScreen():
    font = pygame.font.Font('freesansbold.ttf', 40)
    tip = font.render('按任意键开始游戏~~~', True, (65, 105, 225))
    DISPLAY_SURF.blit(tip, (240, 550))
    pygame.display.update()

    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Snaky!', True, WHITE)
    titleSurf2 = titleFont.render('Snaky!', True, GREEN)

    degrees1 = 270
    degrees2 = 0
    while True:
        DISPLAY_SURF.fill(BG_COLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (windows_width / 2, windows_height / 2)
        DISPLAY_SURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (windows_width / 2, windows_height / 2)
        DISPLAY_SURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame

#结束屏
def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (windows_width / 2, 10)
    overRect.midtop = (windows_width / 2, gameRect.height + 10 + 25)

    DISPLAY_SURF.blit(gameSurf, gameRect)
    DISPLAY_SURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

def drawGrid():
    for x in range(0, windows_width, cell_size): # draw vertical lines
        pygame.draw.line(DISPLAY_SURF, DARK_GRAY, (x, 0), (x, windows_height))
    for y in range(0, windows_height, cell_size): # draw horizontal lines
        pygame.draw.line(DISPLAY_SURF, DARK_GRAY, (0, y), (windows_width, y))

def drawScore(score):
    scoreSurf = BASIC_FONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (windows_width - 120, 10)
    DISPLAY_SURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * cell_size
        y = coord['y'] * cell_size
        wormSegmentRect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(DISPLAY_SURF, DARK_GREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, cell_size - 8, cell_size - 8)
        pygame.draw.rect(DISPLAY_SURF, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * cell_size
    y = coord['y'] * cell_size
    appleRect = pygame.Rect(x, y, cell_size, cell_size)
    pygame.draw.rect(DISPLAY_SURF, RED, appleRect)

def examine_direction(temp , direction):
    if direction == UP:
        if temp == DOWN:
            return False
    elif direction == RIGHT:
        if temp == LEFT:
            return False
    elif direction == LEFT:
        if temp == RIGHT:
            return False
    elif direction == DOWN:
        if temp == UP:
            return False
    return True

def getRandomLocation(worm):
    temp = {'x': random.randint(0, cell_width - 1), 'y': random.randint(0, cell_height - 1)}
    while test_not_ok(temp, worm):
        temp = {'x': random.randint(0, cell_width - 1), 'y': random.randint(0, cell_height - 1)}
    return temp

def test_not_ok(temp, worm):
    for body in worm:
        if temp['x'] == body['x'] and temp['y'] == body['y']:
            return True
    return False

def drawPressKeyMsg():
    pressKeySurf = BASIC_FONT.render('Press a key to play.', True, DARK_GRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (windows_width - 200, windows_height - 30)
    DISPLAY_SURF.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
