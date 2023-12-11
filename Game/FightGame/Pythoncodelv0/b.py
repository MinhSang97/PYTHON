import pygame,time
pygame.init()
song =  pygame.mixer.Sound("baothuc.mp3")
pygame.mixer.Sound.play(song)
time.sleep(60)