import pygame
from pygame import key
from pygame import color
from pygame.display import flip
from pygame.event import EventType
from network import Network
class Player():
    width = height = 50
    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 5
        self.color = color
    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.x, self.y, self.width, self.height), 0)
class Game:
    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(1,270)
        self.player2 = Player(700,270)
        self.phitieu1 = Player(self.player.x,self.player.y)
        self.phitieu2 = Player(self.player2.x,self.player2.y)
        self.canvas = Canvas(self.width, self.height, "Testing...")
    def run(self):
        clock = pygame.time.Clock()
        run = True
        npc = pygame.image.load('npc.png')
        npc = pygame.transform.scale(npc,(123,123))
        npc_rect = npc.get_rect (center = (1,270))
        npc2 = pygame.image.load('npc.png')
        npc2 = pygame.transform.scale(npc2,(123,123))
        npc2_rect = npc2.get_rect(center = (700,270))
        background = pygame.image.load('sky.jpg')
        grass =  pygame.image.load('grass.png')
        grass = pygame.transform.scale(grass,(1050,1050))
        die = pygame.image.load('die_pic.png')
        phitieu1 = pygame.image.load('phitieu.png')
        phitieu1 = pygame.transform.scale(phitieu1,(15,15))
        phitieu2 = phitieu1
        phitieu1_rect = phitieu1.get_rect(center = (npc_rect.centerx,npc_rect.centery))
        phitieu2_rect = phitieu2.get_rect(center = (npc2_rect.centerx,npc2_rect.centery))
        npc_movoment = 0 
        shoot_test_for_run = False
        shoot = False
        gravity = 1.25
        self.mau1 = 101
        self.mau2 = 102
        self.who_shoot = 0  
        self.life1 = True
        self.life2 = True
        self.reset = 0
        score = 0
        while run:
            mousex,mousey= pygame.mouse.get_pos()#Tọa độ chuột 
            #Nhận gửi và phân tích dữ liệu của người chơi khác
            self.player2.x, self.player2.y ,self.phitieu2.x,self.mau1,self.reset= self.parse_data(self.send_data()) 
            #Xét Điều Kiện Để Người Chơi Được Hồi Sinh
            if self.reset == 1 and ((self.life1 == False or self.life2 == False) or (self.mau1<=0 or self.mau2<=0)):
                self.mau1 = 100
                self.mau2 = 100
                self.life1 = True
                self.life2 = True
                self.reset = 0     
            #Khởi tạo sự kiện trong game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:#Thoát
                    run = False
                elif event.type == pygame.KEYDOWN:#Nếu Phát hiện sự kiện từ bàn phím
                    if self.life1  == False and pygame.K_SPACE:
                        self.reset = 1
                elif event.type == pygame.MOUSEBUTTONDOWN:#Nếu phát hiện sự kiện từ trỏ chuột
                    if shoot == False and self.player2.x!= 100 and self.player2.y!=100 and self.mau1 >0:
                        m_x = mousex # Lấy tọa độ trỏ chuột
                        shoot = True
                        shoot_test_for_run =  True   
            #Màu Máu    
            if self.mau1<30  :
                color_heath1= (255, 26, 26)
            elif self.mau2 <30:
                color_heath2 = (255,26,26)
            else:
                color_heath1 = (0, 255, 0)
                color_heath2 = (0,255,0)
            #Khi máu của người chơi <=0 thì sự sống của người chơi sẽ chết =))
            if self.mau1<=0:
                self.life1 = False
            else:
                self.life1 = True
            if self.mau2<=0:
                self.life2 = False
            else:
                self.life2 = True
            #Bắn Ra Phi Tiêu
            if shoot:
                if m_x > npc_rect.centerx:
                    if phitieu1_rect.centerx <= npc_rect.centerx+300:
                        phitieu1_rect.centerx+=12
                    else:shoot_test_for_run = False
                elif m_x < npc_rect.centerx:
                    if phitieu1_rect.centerx >= npc_rect.centerx-300:
                        phitieu1_rect.centerx-=12
                    else:shoot_test_for_run = False
            else:
                phitieu1_rect.centerx = npc_rect.centerx       
            phitieu1_rect.centery = npc_rect.centery
            if shoot_test_for_run  == False and shoot == True:
                shoot = False
            #Ghi Nhận Dữ Liệu Từ Bàn Phím
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                    x = 5
            elif keys[pygame.K_a]:
                    x= -5
            elif keys[pygame.K_SPACE] or keys[pygame.K_w]:
                    y = -20
            else:
                x = 0 
                y = 0
            #Di Chuyển
            self.player.x += x
            self.player.y += y
            #Jump
            npc_movoment += gravity 
            if self.player.y >=270:
                self.player.y+=0
                npc_movoment = 0
            if self.player.y <270:
                self.player.y+=npc_movoment
            #Xữ lí các va chạm (Phi tiêu & Người chơi)
            if self.player2.x < phitieu1_rect.centerx < self.player2.x+50 and shoot :
                self.mau2 -=5
            #Trả về cho self.player tọa độ => Hiển thị
            npc_rect.centerx = self.player.x
            npc_rect.centery = self.player.y
            self.phitieu1.x = phitieu1_rect.centerx+50
            self.phitieu1.y = phitieu1_rect.centery+50
            #Cập Nhật Và Bối cảnh trong Game
            self.canvas.draw_background()
            self.canvas.screen.blit(background,(0,0))
            self.canvas.screen.blit(grass,(0,0))
            if self.life1:
                self.canvas.screen.blit(phitieu1,(self.phitieu1.x,self.phitieu1.y))#Phi tiêu của người chơi số 1
                self.canvas.screen.blit(npc,(self.player.x,self.player.y))#Người chơi số 1
                pygame.draw.rect((self.canvas.screen),color_heath1,(self.player.x+22,self.player.y-5,(90 *self.mau1)/100,12))# Máu2
            else:
                self.canvas.screen.blit(die,(150,0))#Hiển thị màn hình khi chết
            if self.life2 :
                self.canvas.screen.blit(phitieu2,(self.phitieu2.x+50,self.phitieu2.y+50))# Phi tiêu của người chơi số 2
                self.canvas.screen.blit(npc2,(self.player2.x,self.player2.y))#Người chơi số 2
                pygame.draw.rect((self.canvas.screen),color_heath2,(self.player2.x+22,self.player2.y-5,(90 *self.mau2)/100,12))#Máu1
            clock.tick(200)#FPS cho game
            self.canvas.update()#Cập nhật màn hình game
        pygame.quit()
    def send_data(self):
            """
            Gửi dữ liệu đến sv
            :return: None
            """
            data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y) + "," + str(self.phitieu1.x) + ","+ str(self.phitieu1.y) + ","+str(self.mau2)+","+str(self.reset)
            reply = self.net.send(data)
            return reply
    @staticmethod
    def parse_data(data):
            try:
                #Nếu Online
                d = data.split(":")[1].split(",")
                print(d)
                return float(d[0]), float(d[1]) ,float(d[2]),float(d[4]),float(d[5])#,float(d[4]) #,float(d[6]) #,float(d[7]),float(d[8])
            except:
                try:
                    #Nếu Offline
                    print(d)
                    return float(d[0]), float(d[1]) ,float(d[2]),float(100),float(0) #,float(d[3]) #,float(d[4]),float(d[5])
                except:
                    return 0,0

class Canvas:
    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)
    @staticmethod
    def update():
        pygame.display.update()
    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))
        self.screen.draw(render, (x,y))
    def get_canvas(self):
        return self.screen
    def draw_background(self):
        self.screen.fill((255,255,255))
# if self.player2.x == self.player2.y == 100:
            #     self.phitieu2.y = self.player.y
            # else:
            #     self.phitieu2.y = self.player2.y