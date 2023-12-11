import pygame,sys

pygame.init()
screen = pygame.display.set_mode((800,533))
clock =  pygame.time.Clock()
fps = 120
background = pygame.image.load('sky.jpg')
grass =  pygame.image.load('grass.png')
grass = pygame.transform.scale(grass,(1050,1050))
phitieu = pygame.image.load('phitieu.png')
phitieu = pygame.transform.scale(phitieu,(15,15))
npc = pygame.image.load('npc.png')
npc = pygame.transform.scale(npc,(123,123))
npc_rect = npc.get_rect(center = (1,310))
die = pygame.image.load('die_pic.png') 
mau = 100
heath =  pygame.image.load('thanhmau.png')
heath = pygame.transform.scale(heath,(150,300/7))
a = 0
npc_movoment  = 0 
gravity = 1.25
run = True
phitieu_x = npc_rect.centerx
phitieu_movoment = 0
shoot = False 
while True:

    heath_rect = heath.get_rect(center= (npc_rect.centerx,npc_rect.centery-65))
    phitieu_y = npc_rect.centery
    phitieu_movoment = 0 
    if  phitieu_x > npc_rect.centerx and shoot == False :
        phitieu_movoment +=12
        phitieu_x-=phitieu_movoment
    elif phitieu_x < npc_rect.centerx and shoot == False:
        phitieu_movoment +=12
        phitieu_x += phitieu_movoment 
    else:
        phitieu_movoment +=0
        phitieu_x-=phitieu_movoment
    phim = pygame.key.get_pressed()
    x,y =pygame.mouse.get_pos()
    pygame.key.start_text_input()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button ==1:
                mousex = x
                shoot = True
                mau -=10
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                a = 5
            if event.key == pygame.K_LEFT:
                a = -5
            if event.key == pygame.K_LEFT and event.key == pygame.K_RIGHT and pygame.K_SPACE:
                continue 
            if event.key == pygame.K_SPACE:
                npc_rect.centery-=120
            if run == False and pygame.K_SPACE:
                run  = True 
                mau = 100
        else:
            a = 0 
            phitieu_movoment = 0
    if mau <= 0:
        run = False
    npc_rect.centerx+=a
    if npc_rect.centerx > 800 :
        npc_rect.centerx =1
    elif npc_rect.centerx <0:
        npc_rect.centerx = 799
    npc_movoment += gravity
    if npc_rect.centery >=310:
        npc_rect.centery+=0
        npc_movoment = 0
    if npc_rect.centery <310:
        npc_rect.centery+=npc_movoment
    
    if shoot:
        if mousex > npc_rect.centerx:
            if phitieu_x < (npc_rect.centerx+150):
                phitieu_x +=12
            else:
                shoot= False
        elif mousex < npc_rect.centerx:
            if phitieu_x > (npc_rect.centerx-150):
                phitieu_x -=12
            else:
                shoot= False
    if run :
        color_heath = (102, 255, 102)
        thanhmau_x = heath_rect.centerx
        thanhmau_y = heath_rect.centery
        screen.blit(background,(0,0))
        screen.blit(heath,(heath_rect))
        screen.blit(grass,(0,0))
        screen.blit(phitieu,(phitieu_x,phitieu_y))
        screen.blit(npc,npc_rect)
        pygame.draw.rect(screen,color_heath,(thanhmau_x-23,thanhmau_y-14,mau,19))
    else:
        screen.blit(background,(0,0))
        screen.blit(grass,(0,0))
        screen.blit(die,(150,0))
    clock.tick(fps)
    pygame.display.update()