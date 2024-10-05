import pygame
import random
import sys

 
pygame.init()

 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

 
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tiles Game")

 
tile_size = 100

 
rows = 5
cols = 5
mines = 4   

 
grid = [[0 for _ in range(cols)] for _ in range(rows)]

 
mine_positions = random.sample(range(rows * cols), mines)
for pos in mine_positions:
    grid[pos // cols][pos % cols] = 'M'

 
font = pygame.font.Font(None, 36)

 
points = 0
game_over = False

 
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


def tiles_game():
    global points, game_over

    running = True
    revealed = [[False for _ in range(cols)] for _ in range(rows)]

    while running:
        screen.fill(WHITE)

       
        for row in range(rows):
            for col in range(cols):
                x = col * tile_size
                y = row * tile_size
                if revealed[row][col]:
                    if grid[row][col] == 'M':
                        pygame.draw.rect(screen, RED, (x, y, tile_size, tile_size))
                        draw_text("M", font, BLACK, screen, x + tile_size // 2, y + tile_size // 2)
                    else:
                        pygame.draw.rect(screen, GREEN, (x, y, tile_size, tile_size))
                else:
                    pygame.draw.rect(screen, GRAY, (x, y, tile_size, tile_size))

                pygame.draw.rect(screen, BLACK, (x, y, tile_size, tile_size), 2)

  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False   
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // tile_size
                row = mouse_pos[1] // tile_size

                if not revealed[row][col]:
                    revealed[row][col] = True
                    if grid[row][col] == 'M':
                        game_over = True
                    else:
                        points += 1

         
        draw_text(f"Очки: {points}", font, BLACK, screen, screen_width // 2, screen_height - 30)

         
        if game_over:
            draw_text("Гра закінчена! ви втратили всі очки!", font, RED, screen, screen_width // 2, screen_height // 2)

        pygame.display.update()

if __name__ == "__main__":
    tiles_game()
