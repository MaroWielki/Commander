import pygame
import sys


from pygame import K_ESCAPE, K_LEFT, K_RIGHT, KSCAN_UP, K_DOWN, K_SPACE
from my_utils import *
from data import *

pygame.init()

screen=pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

img_org=pygame.image.load('img/weapon/sword1_left.png')

pivot=(42,49)

#pivot=(45,45)

degree=0.


def blitRotateZoomXY( original_image, origin, pivot, angle):

    image_rect = original_image.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center

    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)

    rotozoom_image = pygame.transform.rotate(original_image, angle)
    rect = rotozoom_image.get_rect(center = rotated_image_center)

    return rotozoom_image,rect



while True:
    screen.fill("black")


    img, img_rect=blitRotateZoomXY( img_org, (200,100), pivot, floor(degree))
    pygame.draw.rect(img, "white", img.get_rect(),1)
    screen.blit(img,img_rect)

    degree=degree+1

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