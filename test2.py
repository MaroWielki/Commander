import pygame
from time import time

pygame.init()
r = pygame.rect.Rect(100,100,100,100)
t=time()

for i in range(80000):
    a=r.clipline(90,90,400,90)

print(time()-t)

tmp=[]
t=time()

for i in range(80000):
    tmp.append(i)

print(time()-t)