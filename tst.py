import pygame
import sys


from pygame import K_ESCAPE, K_LEFT, K_RIGHT, KSCAN_UP, K_DOWN, K_SPACE
from my_utils import *
from data import *

pygame.init()

screen=pygame.display.set_mode((800,600))
clock = pygame.time.Clock()



while True:
    screen.fill("black")



    pygame.display.update()
    clock.tick(60)
    pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()