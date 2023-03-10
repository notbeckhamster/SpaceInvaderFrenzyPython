import pygame, sys, random
from pygame.math import Vector2

#Starts pygame
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()


width = 600
length = 800
#Sets window size and creates display window object
screen = pygame.display.set_mode((width,length))
#Creates clock object
clock = pygame.time.Clock()
#custom event
SCREEN_UPDATE = pygame.USEREVENT
#Trigger screen update every 150 ms
pygame.time.set_timer(SCREEN_UPDATE, 150)
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
    def draw_elements(self):
        self.draw_background()
        
    def draw_background(self):
        screen.fill(self.bg_color_black)
        screen.blit(self.player.player_img, self.player.player1_rect)
        screen.blit(self.player.player_img, self.player.player2_rect)
        screen.blit(self.player.crosshair_img, self.player.crosshair_rect)
        self.player.drawLines()
    def update_crosshair_movement(self):
        self.player.crosshair_rect.center = pygame.mouse.get_pos()

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
        #if event.type == SCREEN_UPDATE:
            #main_game.update()
        
    
    main_game.update_crosshair_movement()
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)