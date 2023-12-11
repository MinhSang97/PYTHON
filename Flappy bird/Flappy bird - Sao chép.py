import pygame, sys

pygame.init()
screen = pygame.display.set_mode((480,640))
clock = pygame.time.Clock()
bg = pygame.image.load('D:/Programs/python/Flappy bird/FileGame/assets/background-night.png')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    screen.blit(bg,(0,0))
    pygame.display.update()
    clock.tick(45)
