import pygame
from includes.space import Space
from includes.frog import Frog

class Bus:
    def __init__(self, xpos : float, ypos : float, row : int, sprite : pygame.Surface):
        self.WIDTH : int = 81
        self.HEIGHT : int = 30
        self.xpos : float = xpos
        self.ypos : float = ypos
        self.row : int = row
        self.RIGHT = False

        self.speed : float = 150 / 60 # pixels per second
        self.sprite : pygame.Surface = sprite


class LeftRacecar:
    def __init__(self, xpos : float, ypos : float, row : int, sprite : pygame.Surface):
        self.WIDTH : int = 48
        self.HEIGHT : int = 46
        self.xpos : float = xpos
        self.ypos : float = ypos
        self.row : int = row
        self.RIGHT = False

        self.speed : float = 120 / 60 # pixels per second
        self.sprite : pygame.Surface = sprite

class RightRacecar:
    def __init__(self, xpos : float, ypos : float, row : int, sprite : pygame.Surface):
        self.WIDTH : int = 48
        self.HEIGHT : int = 46
        self.xpos : float = xpos
        self.ypos : float = ypos
        self.row : int = row
        self.RIGHT = True

        self.speed : float = 140 / 60 # pixels per second
        self.sprite : pygame.Surface = sprite
    
class Tractor:
    def __init__(self, xpos : float, ypos : float, row : int, sprite : pygame.Surface):
        self.WIDTH : int = 46
        self.HEIGHT : int = 44
        self.xpos : float = xpos
        self.ypos : float = ypos
        self.row : int = row
        self.RIGHT = True

        self.speed : float = 120 / 60 # pixels per second
        self.sprite : pygame.Surface = sprite

class PinkCar:
    def __init__(self, xpos : float, ypos : float, row : int, sprite : pygame.Surface):
        self.WIDTH : int = 47
        self.HEIGHT : int = 42
        self.xpos : float = xpos
        self.ypos : float = ypos
        self.row : int = row
        self.RIGHT = False

        self.speed : float = 140 / 60 # pixels per second
        self.sprite : pygame.Surface = sprite

class Turtle:
    def __init__(self, xpos : float, ypos : float, row : int, dissapearing : bool, animationDuration : float, speed : float, sprite : pygame.Surface):
        self.WIDTH : int = 48
        self.HEIGHT : int = 46
        self.xpos : float = xpos
        self.ypos : float = ypos
        self.row : int = row
        self.RIGHT = False
        self.dissapearing : bool = dissapearing
        self.ANIMATION_DURATION : float = animationDuration # ms
        self.ANIMATION_TIMER : float = 0

        self.IS_SAFE : bool = True

        self.speed : float = speed # pixels per second
        self.sprite : pygame.Surface = sprite

class Log:
    def __init__(self, xpos : float, ypos : float, row : int, speed : float, length : int ,spriteList : list):
        self.WIDTH : int = 47 * length
        self.HEIGHT : int = 42
        self.xpos : float = xpos
        self.ypos : float = ypos
        self.row : int = row
        self.RIGHT = True
        self.length = length

        self.speed : float = speed # pixels per second
        self.spriteList : list = []
        self.spriteList.append(spriteList[0])

        for i in range(length - 2): self.spriteList.append(spriteList[1])
        self.spriteList.append(spriteList[2])