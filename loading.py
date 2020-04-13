#Loading Animation
import pygame
import os
import time
pygame.init()
gameDisplay =  pygame.display.set_mode(flags=pygame.FULLSCREEN)
for i in range(0,253):
    asurf = pygame.image.load(os.path.join('images', 'loading',i+'.gif')).convert()
    pygame.display.update()
    time.sleep(0.5)