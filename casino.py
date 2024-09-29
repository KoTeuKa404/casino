import pygame
import sys
import slots   
import tiles   
import poker
import match_3  

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  
pygame.display.set_caption("Casino Games")

font = pygame.font.Font(None, 36)

background = pygame.image.load('img/background.png')  
background = pygame.transform.scale(background, (screen_width, screen_height))   

slot_image = pygame.image.load('img/game1.png')  
slot_image = pygame.transform.scale(slot_image, (150, 150))  

poker_image = pygame.image.load('img/poker.png') 
poker_image = pygame.transform.scale(poker_image, (150, 150))

tiles_image = pygame.image.load('img/tiles.png')  
tiles_image = pygame.transform.scale(tiles_image, (150, 150))

match_3_image = pygame.image.load('img/match_3.png')
match_3_image = pygame.transform.scale(match_3_image, (150, 150))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

class CasinoGame:
    def __init__(self):
        self.running = True

    def game_loop(self):
        global screen, screen_width, screen_height, background  
        offset = 200  

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                
                if event.type == pygame.VIDEORESIZE:
                    screen_width, screen_height = event.w, event.h
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                  
                    background = pygame.transform.scale(pygame.image.load('img/background.png'), (screen_width, screen_height))

           
            screen.blit(background, (0, 0))   
            draw_text("Casino Games", font, BLACK, screen, screen_width // 2, 50)

          
            pygame.draw.rect(screen, BLACK, (200 + offset, 80, 150, 150), 2)   
            pygame.draw.rect(screen, BLACK, (450 + offset, 80, 150, 150), 2)  
            pygame.draw.rect(screen, BLACK, (200 + offset, 280, 150, 150), 2)  
            pygame.draw.rect(screen, BLACK, (450 + offset, 280, 150, 150), 2)  

            screen.blit(slot_image, (450 + offset, 80))
            screen.blit(poker_image, (200 + offset, 80))
            screen.blit(tiles_image, (200 + offset, 280))  
            screen.blit(match_3_image, (450 + offset, 280))  

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            
            if 200 + offset < mouse[0] < 350 + offset and 230 < mouse[1] < 280:
                pygame.draw.rect(screen, BLUE, (200 + offset, 230, 150, 50))
                if click[0] == 1:
                    self.running = False  
                    poker.poker_game() 
            else:
                pygame.draw.rect(screen, GREEN, (200 + offset, 230, 150, 50))

            draw_text("Poker", font, WHITE, screen, 275 + offset, 255)

          
            if 450 + offset < mouse[0] < 600 + offset and 230 < mouse[1] < 280:
                pygame.draw.rect(screen, BLUE, (450 + offset, 230, 150, 50))
                if click[0] == 1:
                    self.running = False 
                    slots.slots_game()   
            else:
                pygame.draw.rect(screen, GREEN, (450 + offset, 230, 150, 50))

            draw_text("Slots", font, WHITE, screen, 525 + offset, 255)

           
            if 200 + offset < mouse[0] < 350 + offset and 430 < mouse[1] < 480:
                pygame.draw.rect(screen, BLUE, (200 + offset, 430, 150, 50))
                if click[0] == 1:
                    self.running = False  
                    tiles.tiles_game()  
            else:
                pygame.draw.rect(screen, GREEN, (200 + offset, 430, 150, 50))

            draw_text("Tiles", font, WHITE, screen, 275 + offset, 455)

           
            if 450 + offset < mouse[0] < 600 + offset and 430 < mouse[1] < 480:
                pygame.draw.rect(screen, BLUE, (450 + offset, 430, 150, 50))
                if click[0] == 1:
                    self.running = False  
                    match_3.match_3_game()  
            else:
                pygame.draw.rect(screen, GREEN, (450 + offset, 430, 150, 50))

            draw_text("Match-3", font, WHITE, screen, 525 + offset, 455)

            pygame.display.update()



if __name__ == "__main__":
    game = CasinoGame()
    game.game_loop()
