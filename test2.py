import pygame

pygame.init()

r = pygame.rect.Rect(100,100,100,100)
print(r.clipline(90,90,400,90))
