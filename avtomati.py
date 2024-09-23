import pygame
import sys
import random

pygame.init()

width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Автомат")

clock = pygame.time.Clock()
red= (208,84,87)
white = (255, 255, 255)
number_color = (255, 0, 0)  
background_image = pygame.image.load("game1.jpg")
background_image = pygame.transform.scale(background_image, (width, height))

font = pygame.font.Font(None, 36)

def display_numbers():
    numbers = [str(random.randint(0, 9)) for _ in range(3)]
    text = font.render(" ".join(numbers), True, number_color)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)

def draw_button():
    button_rect = pygame.Rect(width // 2 + 83, height - 243, 15, 15)
    pygame.draw.rect(screen, red, button_rect)
    font_button = pygame.font.Font(None, 30)
    text_button = font_button.render("", True, white)
    text_rect_button = text_button.get_rect(center=button_rect.center)
    screen.blit(text_button, text_rect_button)
    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                button_rect = pygame.Rect(width // 2 - 50, height - 80, 100, 50)
                if button_rect.collidepoint(event.pos):
                    screen.blit(background_image, (0, 0))
                    display_numbers()

    screen.fill(white)
    screen.blit(background_image, (0, 0))
    draw_button()
    '''КОМЕНТАР'''
    pygame.display.flip()
    clock.tick(40)

pygame.quit()
sys.exit()

