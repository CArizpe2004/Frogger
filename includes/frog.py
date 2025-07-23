import pygame
class Frog:
    def __init__(self, xpos, ypos, sprite):

        # grid positions
        self.xpos = xpos
        self.ypos = ypos
        self.WIDTH = self.HEIGHT = 48
    
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
        self.move = (0, 0)
        self.jumping = False

        self.alive = True
        self.dying = False
        self.dead = False

        #  pixel positions for jump animation
        self.pixelPos = (0, 0)
        self.startPos = (0, 0)
        self.endPos = (0, 0)
        
        self.sprite : pygame.Surface = sprite