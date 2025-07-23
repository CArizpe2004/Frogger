import pygame
import os
from enum import Enum
from includes.space import Space
from includes.frog import Frog



SPRITE_PATH = os.path.join(os.getcwd(), r'includes\sprites.png')


WIDTH = HEIGHT = 16
BUS_WIDTH = 27
BUS_HEIGHT = 10
SCALE = 3


def otherGetSprite(sheet, x, y, width, height, scale = 3):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), pygame.Rect(x, y, width, height))

    sprite = pygame.transform.scale(sprite, (int(width * scale), int(height * scale)))
    return sprite


def extractRow(sheet : pygame.Surface, xpos : int, ypos : int, images : int = 8):
    spriteList = []
    for i in range(images):
        sprite = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        sprite.blit(sheet, (0, 0), pygame.Rect(xpos, ypos, WIDTH, HEIGHT))
        sprite = pygame.transform.scale(sprite, (WIDTH * SCALE, HEIGHT * SCALE))
        spriteList.append(sprite)
        xpos += 18
    
    return spriteList

def getBusSprite(sheet : pygame.Surface):
    xpos = 76
    ypos = 119
    sprite = pygame.Surface((BUS_WIDTH, BUS_HEIGHT), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), pygame.Rect(xpos, ypos, BUS_WIDTH, BUS_HEIGHT))
    sprite = pygame.transform.scale(sprite, (BUS_WIDTH * SCALE, BUS_HEIGHT * SCALE))

    return sprite

def getSafeSpaceSprite(sheet : pygame.Surface):
    xpos = 135
    ypos = 196
    sprite = pygame.SurfaceType((WIDTH, HEIGHT), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), pygame.Rect(xpos, ypos, WIDTH, HEIGHT))
    sprite = pygame.transform.scale(sprite, (WIDTH * SCALE, HEIGHT * SCALE))

    return sprite

    
def getBackgroundSprites(sheet : pygame.Surface):
    xpos = 1
    ypos = 188
    width = 8
    height = 24
    sprite = pygame.SurfaceType((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), pygame.Rect(xpos, ypos, width, height))
    sprite = pygame.transform.scale(sprite, (width * SCALE, height * SCALE))

    spriteTwo = pygame.SurfaceType((16, 8), pygame.SRCALPHA)
    spriteTwo.blit(sheet, (0, 0), pygame.Rect(9, 188, 16, 8))
    spriteTwo = pygame.transform.scale(spriteTwo, (16 * SCALE, 8 * SCALE))

    spriteThree = pygame.SurfaceType((width, height), pygame.SRCALPHA)
    spriteThree.blit(sheet, (0, 0), pygame.Rect(25, 188, width, height))
    spriteThree = pygame.transform.scale(spriteThree, (width * SCALE, height * SCALE))

    spriteFour = pygame.SurfaceType((width, height), pygame.SRCALPHA)
    spriteFour.blit(sheet, (0, 0), pygame.Rect(35, 188, width, height))
    spriteFour = pygame.transform.scale(spriteFour, (width * SCALE, height * SCALE))

    return [sprite, spriteTwo, spriteThree, spriteFour]
