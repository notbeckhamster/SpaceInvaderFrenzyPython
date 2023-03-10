import pygame, sys, random
from pygame.math import Vector2

#Starts pygame
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

mouse_pressed = pygame.mouse.get_pressed()[0]
width = 600
length = 800
#Sets window size and creates display window object
screen = pygame.display.set_mode((width,length))
#Creates clock object
clock = pygame.time.Clock()
#custom event
SCREEN_UPDATE = pygame.USEREVENT

class MAIN:
    def __init__(self):
        #Set cursor to middle of screen with crosshair and disable the cursor
        pygame.mouse.set_pos((width*0.5, length*0.5))
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        self.bg_color_black = (0,0,0)
        self.bg_color_stars = (255,255,255)
        self.player = PLAYER()
        self.player.player1_rect.bottomleft = (width*0.05, length)
        self.player.player2_rect.bottomright = (width*0.95, length)
        self.player.crosshair_rect.center = (width*0.5, length*0.5)
        self.crosshair_angle = 0
    def draw_elements(self):
        self.draw_background()
        self.draw_foreground()

    def draw_background(self):
        screen.fill(self.bg_color_black)
        screen.blit(self.player.player_img, self.player.player1_rect)
        screen.blit(self.player.player_img, self.player.player2_rect)
    

    def draw_foreground(self):
        pygame.transform.rotate(self.player.crosshair_img, 70)
        #Reason for keeping original image due to distortion by rotation
        rotated_image = pygame.transform.rotate(self.player.crosshair_img, self.crosshair_angle)
        self.crosshair_angle += 1
        new_rect = rotated_image.get_rect(center = pygame.mouse.get_pos())
        screen.blit(rotated_image, new_rect)
        
    def update_crosshair_movement(self):
        self.player.crosshair_rect.center = pygame.mouse.get_pos()

    def update_crosshair_lines(self):
        if random.randint(0,1) == 0:
            self.player.drawLines()
        

class PLAYER:
    def __init__(self):
        self.player_img = pygame.image.load('graphics\\player.png').convert_alpha()
        self.player1_rect = self.player_img.get_rect()
        self.player2_rect = self.player_img.get_rect()
        self.crosshair_img = pygame.image.load('graphics\\crosshair.png').convert_alpha()
        self.crosshair_rect = self.crosshair_img.get_rect()
    def drawLines(self):

        pygame.draw.line(screen, "red", self.player1_rect.midtop, self.crosshair_rect.center,5)
        pygame.draw.line(screen, "red", self.player2_rect.midtop, self.crosshair_rect.center,5)


main_game = MAIN()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #ends all pygames stuff..
            pygame.quit()
            #actually ends all python processes
            sys.exit()
        
    main_game.draw_elements()
    main_game.update_crosshair_movement()
    if pygame.mouse.get_pressed()[0] == True:
        mouse_pressed = True
        main_game.update_crosshair_lines()
    pygame.display.update()
    clock.tick(60)