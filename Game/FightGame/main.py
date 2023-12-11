import pygame,sys
sys.stdin = open("money.txt","r")
money = int(input())
sys.stdin.close()
sys.stdin = open("weapon.txt","r")
weapon = int(input())
sys.stdin.close()
pygame.init()
screen = pygame.display.set_mode((800,533))
clock =  pygame.time.Clock()
fps = 120
background = pygame.image.load('sky.jpg')
grass =  pygame.image.load('grass.png')
grass = pygame.transform.scale(grass,(1050,1050))
phitieu = pygame.image.load('phitieu.png')
phitieu = pygame.transform.scale(phitieu,(15,15))
phitieu1 = pygame.transform.scale(phitieu,(15,15))
npc = pygame.image.load('npc.png')
npc = pygame.transform.scale(npc,(123,123))
npc_rect = npc.get_rect(center = (1,310))
die = pygame.image.load('die_pic.png') 
mau = 100
heath =  pygame.image.load('thanhmau.png')
heath = pygame.transform.scale(heath,(150,300/7))
heath_boss = pygame.image.load('thanhmau_boss.png')
heath_boss = pygame.transform.scale(heath_boss,(100,300/7))
gun = pygame.image.load('gun.png')
gun = pygame.transform.scale(gun,(100,100))
a = 0
npc_movoment  = 0 
gravity = 1.25
run = True
phitieu_x = npc_rect.centerx
phitieu_movoment = 0
shoot = False 
test_shoot = False 
phitieu_rect = phitieu.get_rect
shoot_test_for_run = False
run_boss =  True
boss = pygame.image.load('npc_boss.png')
boss = pygame.transform.scale(boss,(123,123))
boss = pygame.transform.flip(boss,True,False)
boss_rect = boss.get_rect(center = (700,305))
mau_boss  = 100
dame = 0
i = 0 
h = 0 
j = 0 
phitieu_x_boss = boss_rect.centerx
shoot_boss = False
boss_test_shoot = True
move_boss = 0
boss_run= 0
speed= 4
dame_boss = 0
score= 0
score_plus = False
color_black = (255,51,51)
font =  pygame.font.SysFont('sans',50)
while True:
    text  = font.render(str("Score:"+str(score)),True,color_black)
    text_money = font.render(str("Beli:"+str(money)+"$"),True,(26, 255, 102))
    heath_rect = heath.get_rect(center= (npc_rect.centerx,npc_rect.centery-65))
    heath_boss_rect = heath_boss.get_rect(center =  (boss_rect.centerx-50,boss_rect.centery-64))
    phitieu_y_boss = boss_rect.centery
    phitieu_y = npc_rect.centery
    phim = pygame.key.get_pressed()
    mousex,mousey =pygame.mouse.get_pos()
    pygame.key.start_text_input()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.stdout = open("money.txt","w")
            print(money)
            sys.stdout.close()
            sys.stdout = open("weapon.txt","w")
            print(weapon)
            
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button ==1:
                if shoot == False:
                    x = mousex
                    shoot = True
                    shoot_test_for_run =  True
                    print(weapon)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                a = 5
            if event.key == pygame.K_LEFT or event.key == pygame.K_a :
                a = -5
            if event.key == pygame.K_LEFT and event.key == pygame.K_RIGHT and pygame.K_SPACE:
                continue 
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                npc_rect.centery-=120
            if run == False and pygame.K_SPACE:
                run  = True 
                mau = 100
            if event.key == pygame.K_RCTRL:
                if weapon == 0:
                    if money >= 500:
                        weapon = 1
                        money -=500
                elif weapon == 1:
                    if money>=250:
                        weapon = 0 
                        money-=250
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
        screen.blit(text,(0,0))
        screen.blit(text_money,(0,50))
        if weapon == 1:
            screen.blit(gun,(npc_rect.centerx + 15,npc_rect.centery-35))
    else:
        screen.blit(background,(0,0))
        screen.blit(grass,(0,0))
        screen.blit(die,(150,0))
        score = 0
    if run_boss:
        i = 0
        h+=1
        j += 1
        thanhmau_boss_x = heath_boss_rect.centerx
        thanhmau_boss_y =  heath_boss_rect.centery
        screen.blit(phitieu1,(phitieu_x_boss,phitieu_y_boss))
        screen.blit(heath_boss,heath_boss_rect)
        screen.blit(boss,boss_rect)
        pygame.draw.rect(screen,color_heath,(thanhmau_boss_x-10,thanhmau_boss_y-13,mau_boss,19))
    else:
        i+=1
    if shoot == True and shoot_test_for_run == False:
        shoot =  False
        dame = 0
    if shoot:
        if x  > npc_rect.centerx :
            if phitieu_x < npc_rect.centerx+300  and shoot_test_for_run  == True:
                phitieu_x += 12
            else :
                shoot_test_for_run = False
            if shoot_test_for_run == False:
                phitieu_x -=12
            if phitieu_x <= npc_rect.centerx:
                phitieu_x =  npc_rect.centerx
                shoot_test_for_run = False
        elif x< npc_rect.centerx:
            if phitieu_x> npc_rect.centerx - 300 and shoot_test_for_run == True:
                phitieu_x  -= 12
            else:
                shoot_test_for_run  = False
            if shoot_test_for_run == False:
                phitieu_x +=12
            if phitieu_x >= npc_rect.centerx:
                phitieu_x =  npc_rect.centerx
                shoot_test_for_run  = False
    else:
        phitieu_x = npc_rect.centerx
    if shoot == True and  boss_rect.centerx + 85> phitieu_x > boss_rect.centerx and dame ==0  :
        if weapon == 0:
            mau_boss -= 20
            dame = 1
        else:
            mau_boss -=15
    if shoot_boss == True and npc_rect.centerx+85 > phitieu_x_boss > boss_rect.centerx and dame_boss == 0:
        mau-=20
        dame_boss = 1
    if h > 100:
        shoot_boss = True
    if shoot_boss == True and boss_test_shoot==False :
        h = 0 
        dame_boss = 0
        shoot_boss = False
        boss_test_shoot = True
    if shoot_boss:
        if boss_rect.centerx < npc_rect.centerx :
            if phitieu_x_boss < boss_rect.centerx+300 and boss_test_shoot == True:
                phitieu_x_boss+=12
            else:
                boss_test_shoot = False
            if boss_test_shoot == False:
                phitieu_x_boss -=12
            if boss_rect.centerx >= phitieu_x_boss:
                phitieu_x_boss  = boss_rect.centerx
        elif boss_rect.centerx > npc_rect.centerx :
            if phitieu_x_boss > boss_rect.centerx-300 and boss_test_shoot== True:
                phitieu_x_boss-=12
            else:
                boss_test_shoot = False
            if boss_test_shoot == False:
                phitieu_x_boss +=12
            if boss_rect.centerx <= phitieu_x_boss:
                phitieu_x_boss  = boss_rect.centerx
    else:
        phitieu_x_boss= boss_rect.centerx
    if j > 40 :
        if boss_rect.centerx < npc_rect.centerx :
            boss_run = True
            move_boss = speed*0.334804*1
        elif  boss_rect.centerx > npc_rect.centerx :
            move_boss = speed*0.334804*-1
            boss_run = False
    boss_rect.centerx +=move_boss
    if boss_run == True :
        boss_run = False
        j = 0
    if mau_boss <=0:
        run_boss = False
    if i >= 450:
        mau_boss = 100
        boss_rect.centerx = 700
        run_boss = True
        score+=1
        money+=100
        i = 0
    if  score_plus:
        score_plus = False 
        score+=1    
    clock.tick(fps)
    pygame.display.update()