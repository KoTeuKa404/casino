import pygame
import random
import math
import sys
import os
# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Roulette Game")

# Load assets
inventory = pygame.image.load('img/roulet/table.png')  # Full table layout
pool_mini = pygame.image.load('img/roulet/pool.png')  # Mini roulette track (number layout)
pool = pygame.image.load('img/roulet/pool1.png')  # Field for forming chips
circle_fix = pygame.image.load('img/roulet/own.png')  # Circle overlay on the wheel
circle_spin = pygame.image.load('img/roulet/boo.png')  # Spinning circle overlay

# Initialize player chips (inventory)
player_chips = [
    {'color': 'blue', 'pos': (80, 630), 'dragging': False},
    {'color': 'gray', 'pos': (80, 720), 'dragging': False},
    {'color': 'green', 'pos': (170, 630), 'dragging': False},
    {'color': 'pink', 'pos': (170, 720), 'dragging': False},
    {'color': 'red', 'pos': (280, 630), 'dragging': False},
    {'color': 'black', 'pos': (280, 720), 'dragging': False},
]

# Set the background color (Dark Green)
DARK_GREEN = (24, 72, 4)
bets = []  # To store chips placed as bets
result_message = ""  # Display win or loss message

# Resizing images
inventory = pygame.transform.scale(inventory, (400, 200))
circle_fix = pygame.transform.scale(circle_fix, (500, 500))

# Set up rects for positioning elements
pool_rect = pool.get_rect(topleft=(500, 0))
circle_rect_fix = circle_fix.get_rect(topleft=(-10, -11))
mini_rect = pool_mini.get_rect(topleft=(600, 450))
table_rect = inventory.get_rect(topleft=(50, 600))
circle_rect = circle_spin.get_rect(topleft=(50, 50))

# Roulette wheel and ball settings
circle_angle = 0
spin_speed = 0
spinning = False
ball_speed = 10
ball_angle = 0
ball_distance_from_center = 160
ball_radius = 10  # Define ball radius
ball_stopped = False  # Flag to track if the ball has stopped

ball_center_x, ball_center_y = circle_rect.center

wheel_numbers = [14, 2, 0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 
                 1, '00', 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35]

number_colors = {
    1: 'red', 2: 'black', 3: 'red', 4: 'black', 5: 'red', 6: 'black', 7: 'red', 8: 'black',
    9: 'red', 10: 'black', 11: 'black', 12: 'red', 13: 'black', 14: 'red', 15: 'black',
    16: 'red', 17: 'black', 18: 'red', 19: 'red', 20: 'black', 21: 'red', 22: 'black',
    23: 'red', 24: 'black', 25: 'red', 26: 'black', 27: 'red', 28: 'black', 29: 'black',
    30: 'red', 31: 'black', 32: 'red', 33: 'black', 34: 'red', 35: 'black', 36: 'red',
    0: 'green', '00': 'green'
}

font = pygame.font.SysFont(None, 24)
result_font = pygame.font.SysFont(None, 36)

music_folder = "music/radio"  # Папка з музикою
music_files = [os.path.join(music_folder, file) for file in os.listdir(music_folder) if file.endswith(".ogg")]

def play_random_music(volume=0.5):
    if music_files:
        random_music = random.choice(music_files)
        pygame.mixer.music.load(random_music)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()

# Викликаємо цю функцію для початку гри
play_random_music()
play_random_music()

def rotate_circle(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=circle_rect.center)
    return rotated_image, new_rect

def draw_numbers_on_wheel(angle_offset, ball_pos_x, ball_pos_y):
    radius = 160  
    min_distance = float('inf')  
    closest_number = None 

    correction_angle = math.radians(-90)  # Adjust for correct number rotation alignment

    for i, number in enumerate(wheel_numbers):
        angle = math.radians(i * (360 / len(wheel_numbers))) - angle_offset + correction_angle
        x = ball_center_x + radius * math.cos(angle)
        y = ball_center_y + radius * math.sin(angle)

        distance_to_ball = math.sqrt((x - ball_pos_x) ** 2 + (y - ball_pos_y) ** 2)

        if distance_to_ball < min_distance:
            min_distance = distance_to_ball
            closest_number = number

    return closest_number
dragging_chip = None
def handle_chip_dragging(mouse_x, mouse_y, event_type):
    global dragging_chip
    if event_type == pygame.MOUSEBUTTONDOWN:
        for chip in player_chips:
            chip_rect = pygame.Rect(chip['pos'][0], chip['pos'][1], 50, 50)
            if chip_rect.collidepoint(mouse_x, mouse_y):
                chip['dragging'] = True
                dragging_chip = chip
                break
    elif event_type == pygame.MOUSEBUTTONUP and dragging_chip:
        if pool_rect.collidepoint(mouse_x, mouse_y):
            bets.append({'chip': dragging_chip.copy(), 'position': (mouse_x, mouse_y)})
            player_chips.remove(dragging_chip)  
        dragging_chip['dragging'] = False
        dragging_chip = None
    elif event_type == pygame.MOUSEMOTION and dragging_chip and dragging_chip['dragging']:
        dragging_chip['pos'] = (mouse_x, mouse_y)

def check_bets(closest_number):
    global result_message
    winning_bets = []

    result_color = number_colors[closest_number]  # Колір виграшного числа

    for bet in bets:
        bet_position = bet['position']

        # Перевірка, чи потрапляє ставка в область червоного чи чорного
        if 830 <= bet_position[0] <= 950 and 340 <= bet_position[1] <= 400 and result_color == 'red':
            winning_bets.append(bet)
        elif 955 <= bet_position[0] <= 1075 and 340 <= bet_position[1] <= 400 and result_color == 'black':
            winning_bets.append(bet)

        # Перевірка ставок на нулі
        elif 500 <= bet_position[0] <= 570 and 140 <= bet_position[1] <= 260 and closest_number == 0:
            winning_bets.append(bet)
        elif 500 <= bet_position[0] <= 570 and 0 <= bet_position[1] <= 135 and closest_number == '00':
            winning_bets.append(bet)

        # Перевірка ставок на конкретні числа
        if 580 <= bet_position[0] <= 635 and 0 <= bet_position[1] <= 85 and closest_number == 3:
            winning_bets.append(bet)
        elif 580 <= bet_position[0] <= 635 and 90 <= bet_position[1] <= 180 and closest_number == 2:
            winning_bets.append(bet)
        elif 580 <= bet_position[0] <= 635 and 185 <= bet_position[1] <= 265 and closest_number == 1:
            winning_bets.append(bet)
            
        elif 640 <= bet_position[0] <= 695 and 0 <= bet_position[1] <= 85 and closest_number == 6:
            winning_bets.append(bet)
        elif 640 <= bet_position[0] <= 695 and 90 <= bet_position[1] <= 180 and closest_number == 5:
            winning_bets.append(bet)
        elif 640 <= bet_position[0] <= 695 and 185 <= bet_position[1] <= 265 and closest_number == 4:
            winning_bets.append(bet)

        elif 700 <= bet_position[0] <= 755 and 0 <= bet_position[1] <= 85 and closest_number == 9:
            winning_bets.append(bet)
        elif 700 <= bet_position[0] <= 755 and 90 <= bet_position[1] <= 180 and closest_number == 8:
            winning_bets.append(bet)
        elif 700 <= bet_position[0] <= 755 and 185 <= bet_position[1] <= 265 and closest_number == 7:
            winning_bets.append(bet)

        elif 765 <= bet_position[0] <= 815 and 0 <= bet_position[1] <= 85 and closest_number == 12:
            winning_bets.append(bet)
        elif 765 <= bet_position[0] <= 815 and 90 <= bet_position[1] <= 180 and closest_number == 11:
            winning_bets.append(bet)
        elif 765 <= bet_position[0] <= 815 and 185 <= bet_position[1] <= 265 and closest_number == 10:
            winning_bets.append(bet)

        elif 830 <= bet_position[0] <= 875 and 0 <= bet_position[1] <= 85 and closest_number == 15:
            winning_bets.append(bet)
        elif 830 <= bet_position[0] <= 875 and 90 <= bet_position[1] <= 180 and closest_number == 14:
            winning_bets.append(bet)
        elif 830 <= bet_position[0] <= 875 and 185 <= bet_position[1] <= 265 and closest_number == 13:
            winning_bets.append(bet)

        elif 880 <= bet_position[0] <= 935 and 0 <= bet_position[1] <= 85 and closest_number == 18:
            winning_bets.append(bet)
        elif 880 <= bet_position[0] <= 935 and 90 <= bet_position[1] <= 180 and closest_number == 17:
            winning_bets.append(bet)
        elif 880 <= bet_position[0] <= 935 and 185 <= bet_position[1] <= 265 and closest_number == 16:
            winning_bets.append(bet)

        elif 955 <= bet_position[0] <= 995 and 0 <= bet_position[1] <= 85 and closest_number == 21:
            winning_bets.append(bet)
        elif 955 <= bet_position[0] <= 995 and 90 <= bet_position[1] <= 180 and closest_number == 20:
            winning_bets.append(bet)
        elif 955 <= bet_position[0] <= 995 and 185 <= bet_position[1] <= 265 and closest_number == 19:
            winning_bets.append(bet)

        elif 1020 <= bet_position[0] <= 1075 and 0 <= bet_position[1] <= 85 and closest_number == 24:
            winning_bets.append(bet)
        elif 1020 <= bet_position[0] <= 1075 and 90 <= bet_position[1] <= 180 and closest_number == 23:
            winning_bets.append(bet)
        elif 1020 <= bet_position[0] <= 1075 and 185 <= bet_position[1] <= 265 and closest_number == 22:
            winning_bets.append(bet)

        elif 1080 <= bet_position[0] <= 1135 and 0 <= bet_position[1] <= 85 and closest_number == 27:
            winning_bets.append(bet)
        elif 1080 <= bet_position[0] <= 1135 and 90 <= bet_position[1] <= 180 and closest_number == 26:
            winning_bets.append(bet)
        elif 1080 <= bet_position[0] <= 1135 and 185 <= bet_position[1] <= 265 and closest_number == 25:
            winning_bets.append(bet)

        elif 1140 <= bet_position[0] <= 1200 and 0 <= bet_position[1] <= 85 and closest_number == 30:
            winning_bets.append(bet)
        elif 1140 <= bet_position[0] <= 1200 and 90 <= bet_position[1] <= 180 and closest_number == 29:
            winning_bets.append(bet)
        elif 1140 <= bet_position[0] <= 1200 and 185 <= bet_position[1] <= 265 and closest_number == 28:
            winning_bets.append(bet)

        elif 1205 <= bet_position[0] <= 1260 and 0 <= bet_position[1] <= 85 and closest_number == 33:
            winning_bets.append(bet)
        elif 1205 <= bet_position[0] <= 1260 and 90 <= bet_position[1] <= 180 and closest_number == 32:
            winning_bets.append(bet)
        elif 1205 <= bet_position[0] <= 1260 and 185 <= bet_position[1] <= 265 and closest_number == 31:
            winning_bets.append(bet)

        elif 1265 <= bet_position[0] <= 1325 and 0 <= bet_position[1] <= 85 and closest_number == 36:
            winning_bets.append(bet)
        elif 1265 <= bet_position[0] <= 1325 and 90 <= bet_position[1] <= 180 and closest_number == 35:
            winning_bets.append(bet)
        elif 1265 <= bet_position[0] <= 1325 and 185 <= bet_position[1] <= 265 and closest_number == 34:
            winning_bets.append(bet)

    if winning_bets:
        result_message = f"You won {len(winning_bets) * 2} Chip(s)!"  
        for bet in winning_bets:
            new_chip = bet['chip'].copy()  
            player_chips.append(new_chip)
            player_chips.append(new_chip.copy())  
    else:
        result_message = "You lost!"

    bets.clear()  

def update_yellow_square(result_number):
    # відображення числа яке випало на рулетці
    bet_positions = {
        27: (620, 450), 10: (663, 450), 25: (705, 450), 29: (747, 450), 12: (789, 450),
        8: (831, 450), 19: (873, 450), 31: (915, 450), 18: (957, 450), 6: (999, 450),
        21: (1041, 450), 33: (1083, 450), 16: (1125, 450), 4: (1167, 450), 23: (1209, 450),
        35: (1251, 450), 14: (1291, 450), 2: (1315, 475), 0: (1315, 515), 28: (1293, 542),
        9: (1251, 542), 26: (1209, 542), 30: (1167, 542), 11: (1125, 542), 7: (1083, 542),
        20: (1041, 542), 32: (999, 542), 17: (957, 542), 5: (915, 542), 22: (873, 542),
        34: (831, 542), 15: (789, 542), 3: (747, 542), 24: (705, 542), 36: (663, 542),
        13: (621, 542), 1: (597, 515), "00": (597, 474)
    }
    return bet_positions.get(result_number, (100, 100))

def roulette_game(screen_width, screen_height):
    running = True
    clock = pygame.time.Clock()
    dragging_chip = None
    spinning = False  # Ініціалізація змінної spinning
    ball_speed = 0
    circle_angle = 0  # Ініціалізація змінної circle_angle
    ball_angle = 0  # Ініціалізація змінної ball_angle
    ball_stopped = False  # Ініціалізація змінної ball_stopped
    play_random_music()

    while running:
        screen.fill(DARK_GREEN)
        screen_width, screen_height = screen.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            mouse_x, mouse_y = pygame.mouse.get_pos()
            handle_chip_dragging(mouse_x, mouse_y, event.type)

            if event.type == pygame.MOUSEBUTTONDOWN and not spinning:
                if 180 <= event.pos[0] <= 260 and 180 <= event.pos[1] <= 260:
                    spin_speed = random.randint(5, 20)
                    spinning = True
                    ball_speed = 10
                    ball_stopped = False

        if spinning:
            circle_angle += spin_speed
            ball_angle += ball_speed / ball_distance_from_center
            spin_speed *= 0.99
            if spin_speed < 0.5:
                spinning = False

        if not spinning and ball_speed > 0:
            ball_angle += ball_speed / ball_distance_from_center
            ball_speed *= 0.98
            if ball_speed < 0.1:
                ball_speed = 0
                ball_stopped = True  

        rotated_circle_spin, rotated_circle_spin_rect = rotate_circle(circle_spin, circle_angle)
        ball_pos_x = ball_center_x + ball_distance_from_center * math.cos(ball_angle)
        ball_pos_y = ball_center_y + ball_distance_from_center * math.sin(ball_angle)

        screen.blit(inventory, table_rect)
        screen.blit(pool, pool_rect)
        screen.blit(circle_fix, circle_rect_fix)
        screen.blit(pool_mini, mini_rect)
        screen.blit(rotated_circle_spin, rotated_circle_spin_rect)
        pygame.draw.circle(screen, (255, 255, 255), (int(ball_pos_x), int(ball_pos_y)), ball_radius)

        closest_number = draw_numbers_on_wheel(math.radians(circle_angle), ball_pos_x, ball_pos_y)
        yellow_square_pos = update_yellow_square(closest_number)
        pygame.draw.rect(screen, (255, 255, 0), (*yellow_square_pos, 50, 50), 5)

        if ball_stopped:
            check_bets(closest_number)
            ball_stopped = False

        if result_message:
            result_text = result_font.render(result_message, True, (255, 255, 255))
            screen.blit(result_text, (600, 50))

        for chip in player_chips:
            chip_texture = pygame.image.load(f'img/roulet/{chip["color"]}.png')
            chip_texture = pygame.transform.scale(chip_texture, (50, 50))
            screen.blit(chip_texture, chip['pos'])

        for bet in bets:
            chip_texture = pygame.image.load(f'img/roulet/{bet["chip"]["color"]}.png')
            chip_texture = pygame.transform.scale(chip_texture, (50, 50))
            screen.blit(chip_texture, bet['position'])

        exit_button_width, exit_button_height = 70, 40
        exit_button_x = screen_width - exit_button_width - 10
        exit_button_y = screen_height - exit_button_height - 10
        pygame.draw.rect(screen, (255, 0, 0), (exit_button_x, exit_button_y, exit_button_width, exit_button_height))
        font = pygame.font.SysFont(None, 36)
        exit_text = font.render('EXIT', True, (255, 255, 255))
        screen.blit(exit_text, (exit_button_x + 5, exit_button_y + 5))

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if exit_button_x <= mouse_pos[0] <= exit_button_x + exit_button_width and exit_button_y <= mouse_pos[1] <= exit_button_y + exit_button_height:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    play_random_music()
    roulette_game(1400, 800)  # Передаємо розмір вікна
