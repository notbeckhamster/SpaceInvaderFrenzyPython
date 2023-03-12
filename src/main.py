import pygame, sys, random
from pygame.math import Vector2

#Starts pygame
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.mixer.init()

machinegun_sound = pygame.mixer.Sound("audio\\machinegun.mp3")
background_sound = pygame.mixer.Sound("audio\\music.wav")
death_sound = pygame.mixer.Sound("audio\death.wav")
background_sound.play(loops = -1)
background_sound.set_volume(0.5)
mouse_pressed = pygame.mouse.get_pressed()[0]
width = 600
length = 800
#Sets window size and creates display window object
screen = pygame.display.set_mode((width,length))
pygame.display.set_caption("SpaceInvaderFrenzyPython")
game_over_bool = False
#Creates clock object
clock = pygame.time.Clock()
#custom events
STARUPDATE = pygame.event.custom_type()
GAMEOVER = pygame.event.custom_type()
GAMERESTART = pygame.event.custom_type()
GAMEOVER_EVENT = pygame.event.Event(GAMEOVER)
GAMERESTART_EVENT = pygame.event.Event(GAMERESTART)
pygame.time.set_timer(STARUPDATE, 1000) 
font_path = 'fonts//ARCADECLASSIC.ttf'
size = int(length*0.1)
arcade_font = pygame.font.Font(font_path, size)

class MONSTER(object):
    def __init__(self, image, movespeed, intital_location, direction):
        self.monster_img = image
        self.monster_rect = self.monster_img.get_rect()
        self.movespeed = movespeed
        self.monster_rect.center = intital_location
        self.direction = direction
    def move(self):
        self.monster_rect.x += self.direction*(self.movespeed)
    
class RED(MONSTER):
    def __init__(self, movespeed, intital_location):
        super(RED, self).__init__(pygame.image.load('graphics\\red.png').convert_alpha(), movespeed, intital_location, 1)    

class BLOCK:
    def __init__(self, startingPt, numPerRow, numOfRow):
        self.list = list()
        for y in range(0, numOfRow):
            for x in range(1,numPerRow+1):
                self.list.append(RED(5, (startingPt[0]*x, startingPt[1] if self.list.__len__() == 0 else startingPt[1] + y*self.list[0].monster_rect.height)))
                
        
        for each_mon in self.list:
            screen.blit(each_mon.monster_img, each_mon.monster_rect)
    
    def moveBlock(self):
        for x in self.list:
            if (x.monster_rect.left < 0 or x.monster_rect.right > width):
                self.moveDown()
                return
        
        self.moveAcross()
        
    def moveDown(self):
        for curr in self.list:
            curr.direction = 1 if curr.direction == -1 else -1
            curr.monster_rect.y += curr.monster_rect.height
            curr.monster_rect.x += curr.direction*(curr.movespeed*2)

    def moveAcross(self):
        for curr in self.list:
            curr.move()
    def remove_monster(self, monster):
        self.list.remove(monster)
        death_sound.play()


    def displayMonsters(self):
        global GAMEOVER
        for each_mon in self.list:
            screen.blit(each_mon.monster_img, each_mon.monster_rect)
            if (game_over_bool == False and each_mon.monster_rect.bottom > main_game.player.protect_line_height_left[1]):
                pygame.event.post(GAMEOVER_EVENT)


class PLAYER:
    def __init__(self):
        self.player_img = pygame.image.load('graphics\\player.png').convert_alpha()
        self.player1_rect = self.player_img.get_rect()
        self.player2_rect = self.player_img.get_rect()
        self.crosshair_img = pygame.image.load('graphics\\crosshair.png').convert_alpha()
        self.crosshair_rect = self.crosshair_img.get_rect()
        self.player1_rect.bottomleft = (width*0.05, length)
        self.player2_rect.bottomright = (width*0.95, length)
        self.crosshair_rect.center = (width*0.5, length*0.5)
        self.crosshair_angle = 0
        self.protect_color = (255,0,0)
        self.protect_text = arcade_font.render("PROTECT", True, self.protect_color)
        self.protect_text_rect = self.protect_text.get_rect(midbottom = (width/2,self.player1_rect.midbottom[1]))
        self.protect_line_height_left = (0, self.protect_text_rect.midtop[1]-10)
        self.protect_line_height_right = (width, self.protect_text_rect.midtop[1]-10)
    def drawLines(self):

        pygame.draw.line(screen, "red", self.player1_rect.midtop, self.crosshair_rect.center,5)
        pygame.draw.line(screen, "red", self.player2_rect.midtop, self.crosshair_rect.center,5)
    def blit_elements(self):
        screen.blit(self.player_img, self.player1_rect)
        screen.blit(self.player_img, self.player2_rect)
        screen.blit(self.protect_text, self.protect_text_rect)
        pygame.draw.line(screen, "red", self.protect_line_height_left, self.protect_line_height_right,5)
    def blit_crosshair(self):
        pygame.transform.rotate(self.crosshair_img, 70)
        #Reason for creating a new rect is that roataion will ruin the original rect
        rotated_image = pygame.transform.rotate(self.crosshair_img, self.crosshair_angle)
        self.crosshair_angle += 1
        mousex = pygame.mouse.get_pos()[0]
        mousey = pygame.mouse.get_pos()[1]
        mousex = pygame.math.clamp(mousex,0,width) 
        mousey = pygame.math.clamp(mousey,0,length) 
        new_rect = rotated_image.get_rect(center = (mousex, mousey))
        screen.blit(rotated_image, new_rect)
  
class MAIN:
    def __init__(self):
        #Set cursor to middle of screen with crosshair and disable the cursor
        pygame.mouse.set_pos((width*0.5, length*0.5))
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        self.bg_color_black = (0,0,0)
        self.bg_color_stars = (255,255,255)
        self.player = PLAYER()
        self.star_list = self.create_star_list()
        self.block_red = BLOCK((width*0.1, length*0.1),5,3)
    def draw_background(self):
        screen.fill(self.bg_color_black)
        self.draw_stars()
        
    

    def draw_foreground(self):
        self.update_crosshair_movement()
        self.player.blit_elements()
        self.player.blit_crosshair()
        self.block_red.moveBlock()
        self.block_red.displayMonsters()
        
    def update_crosshair_movement(self):
        mousex = pygame.mouse.get_pos()[0]
        mousey = pygame.mouse.get_pos()[1]
        mousex = pygame.math.clamp(mousex,0,width) 
        mousey = pygame.math.clamp(mousey,0,length) 
        self.player.crosshair_rect.center = (mousex, mousey)

    def update_crosshair_lines(self):
        if random.randint(0,1) == 0:
            self.player.drawLines()
    
    def draw_stars(self):
        for x in self.star_list:
            screen.blit(x[0], x[1])
    def change_stars(self):
        for x in range(0,3):
            self.star_list[random.randint(0, self.star_list.__len__()-1)][1].topleft = (random.randint(0,width-size), random.randint(0,length-size))
        
    def create_star_list(self):
        temp_list = []
        for x in range(0,20):
          size = random.randint(3,10)
          temp_surface = pygame.Surface((size,size))
          temp_surface.fill("white")
          temp_list.append((temp_surface, temp_surface.get_rect(topleft = (random.randint(0,width-size), random.randint(0,length-size)))))
        return temp_list
    
    def check_collision(self):
        for x in self.block_red.list:
            mousex = pygame.mouse.get_pos()[0]
            mousey = pygame.mouse.get_pos()[1]
            mousex = pygame.math.clamp(mousex,0,width) 
            mousey = pygame.math.clamp(mousey,0,length) 
            if x.monster_rect.collidepoint((mousex, mousey)) == True:
                self.block_red.remove_monster(x)
class GameOver:
    def __init__(self):
        self.text_color = (255,0,0)
        self.text_size = int(length*0.05)
        self.text_font = pygame.font.Font(font_path, self.text_size)
        self.list = self.createList()
    def display(self):
        for each_pair in self.list:
            screen.blit(each_pair[0], each_pair[1])
    
    def createList(self):
        points = 100
        bonus_points = 15
        text = ["PRESS ANY BUTTON", "TO RESTART", "POINTS ", str(points), "BONUS POINTS ", str(bonus_points), "TOTAL POINTS ", str(points + bonus_points)]
        text_surf_rect_list = []
        count=0
        for each_text in text:
            self.info = self.text_font.render(each_text, True, self.text_color)
            self.info_rect = self.info.get_rect(midbottom = (width/2,length*0.1 + count*self.info.get_rect().height))
            count+=1
            text_surf_rect_list.append([self.info, self.info_rect])
        return text_surf_rect_list

class ScoreBoard:
    def __init__(self):
        self.text_color = (255,0,0)
        self.text_size = int(length*0.03)
        self.text_font = pygame.font.Font(font_path, self.text_size)
        self.list = self.createList()
    def display(self):
        for each_pair in self.list:
            screen.blit(each_pair[0], each_pair[1])
    
    def createList(self):
        total_points = 56
        text = ["P1", str(total_points)]
        text_surf_rect_list = []
        count=0
        for each_text in text:
            each_surface = self.text_font.render(each_text, True, self.text_color)
            each_rect = each_surface.get_rect(topleft = (0, 0 + count*each_surface.get_rect().height))
            text_surf_rect_list.append([each_surface, each_rect])
            count+=1
        return text_surf_rect_list

main_game = MAIN()
game_over = GameOver()
score_board = ScoreBoard()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #ends all pygames stuff..
            pygame.quit()
            #actually ends all python processes
            sys.exit()
        if event.type == GAMEOVER:
            game_over_bool = True
            machinegun_sound.stop()
        if event.type == STARUPDATE:
            main_game.change_stars()
        if event.type == GAMERESTART:
            game_over_bool = False
            main_game = MAIN()
        if game_over_bool == False:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
                machinegun_sound.play()
            if event.type == pygame.MOUSEBUTTONUP:
                machinegun_sound.stop()
                mouse_pressed = False
        else:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.event.post(GAMERESTART_EVENT)


    main_game.draw_background()

    if game_over_bool == False:
        main_game.draw_foreground()
        if mouse_pressed == True:
            main_game.check_collision()
            main_game.update_crosshair_lines()
        score_board.display()
    else:
        game_over.display()

    
   
   
    pygame.display.update()
    clock.tick(60)