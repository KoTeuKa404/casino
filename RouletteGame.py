import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((1400, 800), pygame.RESIZABLE)
pygame.display.set_caption("Roulette Game")

# Load assets
inventory = pygame.image.load('img/roulet/table.png')  # Full table layout
pool_mini = pygame.image.load('img/roulet/pool.png')  # Mini roulette track (number layout)
pool = pygame.image.load('img/roulet/pool1.png')  # Main roulette wheel
circle_fix = pygame.image.load('img/roulet/own.png')  # Circle overlay on the wheel
circle_spin = pygame.image.load('img/roulet/boo.png')  # Spinning circle overlay

# Set the background color (Dark Green)
DARK_GREEN = (24,72,4)

# Resize the wheel and other images as necessary
inventory = pygame.transform.scale(inventory, (400, 200))  # Resize the mini roulette track to be smaller
circle_fix = pygame.transform.scale(circle_fix, (500, 500))  # Resize the mini roulette track to be smaller

# Wheel and table positioning
pool_rect = pool.get_rect(topleft=(500, 0))  # Колесо позиціонується в верхньому лівому куті
circle_rect_fix = circle_fix.get_rect(topleft=(-11, -14))  # Центруємо коло на колесі
mini_rect = pool_mini.get_rect(topleft=(600, 450))  # Міні-трек (під колесом)
table_rect = inventory.get_rect(topleft=(50, 600))  # Таблиця для ставок з правого боку
circle_rect = circle_spin.get_rect(topleft=(50, 50))  # Центруємо обертальне коло

# Rotation variables
circle_angle = 0
spin_speed = 0
spinning = False

# Ball animation variables
ball_radius = 10
ball_speed = 5  # Speed of the ball
ball_angle = 0  # Current angle of the ball (in radians)
ball_distance_from_center = 160  # Distance of the ball from the center of the wheel (adjustable)

# Set the new center for ball rotation
ball_center_x, ball_center_y = circle_rect.center

# Function to rotate circle_spin
def rotate_circle(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=circle_rect.center)
    return rotated_image, new_rect

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(DARK_GREEN)  # Darker green background for the table

    # Get the size of the screen to calculate button position
    screen_width, screen_height = screen.get_size()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # Check if the user clicks on the start button at (200, 200)
            if 180 <= x <= 260 and 180 <= y <= 260:  # Невидима область для запуску
                if not spinning:  # Start spinning the circle and ball
                    spin_speed = random.randint(5, 20)  # Random spin speed
                    spinning = True

    # Spin the circle if active
    if spinning:
        circle_angle += spin_speed
        ball_angle += ball_speed / ball_distance_from_center  # The ball moves along the wheel's edge
        spin_speed *= 0.99  # Slow down gradually
        if spin_speed < 0.1:
            spinning = False
            spin_speed = 0  # Stop spinning

    # Rotate the circle_spin image
    rotated_circle_spin, rotated_circle_spin_rect = rotate_circle(circle_spin, circle_angle)

    # Calculate ball position based on its angle around the wheel
    ball_pos_x = ball_center_x + ball_distance_from_center * math.cos(ball_angle)
    ball_pos_y = ball_center_y + ball_distance_from_center * math.sin(ball_angle)

    # Draw all elements in correct positions
    screen.blit(inventory, table_rect)  # Draw the table layout with the betting grid
    screen.blit(pool, pool_rect)  # Draw the static roulette wheel

    # First draw the static circle
    screen.blit(circle_fix, circle_rect_fix)  # Draw the static circle overlay
    screen.blit(pool_mini,mini_rect)  # Draw the static circle overlay

    # Then draw the rotating circle over the static one
    screen.blit(rotated_circle_spin, rotated_circle_spin_rect)  # Draw the spinning circle overlay

    # Draw the ball
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_pos_x), int(ball_pos_y)), ball_radius)

    # Draw Exit button in the bottom-right corner
    exit_button_width, exit_button_height = 70, 40
    exit_button_x = screen_width - exit_button_width - 10  # 10 pixels from the right edge
    exit_button_y = screen_height - exit_button_height - 10  # 10 pixels from the bottom edge
    pygame.draw.rect(screen, (255, 0, 0), (exit_button_x, exit_button_y, exit_button_width, exit_button_height))  # Red rectangle for the Exit button
    font = pygame.font.SysFont(None, 36)
    exit_text = font.render('EXIT', True, (255, 255, 255))
    screen.blit(exit_text, (exit_button_x + 5, exit_button_y + 5))

    # Check if exit button is clicked
    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        if exit_button_x <= mouse_pos[0] <= exit_button_x + exit_button_width and exit_button_y <= mouse_pos[1] <= exit_button_y + exit_button_height:
            running = False

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# Quit Pygame
pygame.quit()
