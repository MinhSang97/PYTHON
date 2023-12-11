import time
import pygame,time
pygame.init()

h, p ,s = map(int,input().split())

while True:
    s +=1
    if s == 60:
        s=0
        p+=1
    if p ==60:
        p = 0
        h +=1
    if h == 23:
        h == 0
    print(h,":",p,":",s)
    time.sleep(1)  
    if h ==3 and 0<=p<45:
        song =  pygame.mixer.Sound("baothuc.mp3")
        pygame.mixer.Sound.play(song)
        time.sleep(17)


    