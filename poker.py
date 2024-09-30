import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()  

CARD_WIDTH, CARD_HEIGHT = 100, 150
CARD_SPACING = 25
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Poker Game 1-on-1")

font = pygame.font.Font(None, 36)
winner_font = pygame.font.Font(None, 60)

SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

player_chips = 1000
ai_chips = 1000
pot = 0
current_bet = 0
community_cards = []
hands = {}
game_phase = 'pre-flop'
winner_text = ""
small_blind = 50
big_blind = 100
bet_phase = "initial"
raise_amount = 100  # Сума підвищення ставки

card_images = {}
for suit in SUITS:
    for rank in RANKS:
        card_images[f"{rank}_of_{suit}"] = pygame.image.load(f"img/card/{rank}_of_{suit}.png")

card_back_image = pygame.image.load("img/card/back.png")

music_folder = "music/radio" 
music_files = [os.path.join(music_folder, file) for file in os.listdir(music_folder) if file.endswith(".ogg")]

def play_random_music(volume=0.5):
    if music_files:
        random_music = random.choice(music_files)
        pygame.mixer.music.load(random_music)
        pygame.mixer.music.play()

def create_deck():
    deck = [{'rank': rank, 'suit': suit} for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck

def deal_cards(deck):
    return {'Player': [deck.pop(), deck.pop()], 'AI': [deck.pop(), deck.pop()]}

def draw_card(card, x, y):
    card_key = f"{card['rank']}_of_{card['suit']}"
    scaled_card = pygame.transform.scale(card_images[card_key], (CARD_WIDTH, CARD_HEIGHT))
    screen.blit(scaled_card, (x, y))

def draw_community_cards(cards):
    community_card_y = SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2
    for i, card in enumerate(cards):
        x_position = 450 + (CARD_WIDTH + CARD_SPACING + 20) * i
        draw_card(card, x_position, community_card_y)

def draw_player_hands(hands):
    player_hand_y = SCREEN_HEIGHT - CARD_HEIGHT - 150
    for i, card in enumerate(hands['Player']):
        x_position = 100 + (CARD_WIDTH + CARD_SPACING + 20) * i
        draw_card(card, x_position, player_hand_y)

def draw_ai_hands(ai_hand, reveal=False):
    ai_hand_y = 100
    for i, card in enumerate(ai_hand):
        x_position = 100 + (CARD_WIDTH + CARD_SPACING + 20) * i
        if reveal:
            draw_card(card, x_position, ai_hand_y)
        else:
            scaled_back = pygame.transform.scale(card_back_image, (CARD_WIDTH, CARD_HEIGHT))
            screen.blit(scaled_back, (x_position, ai_hand_y))

def create_button(x, y, w, h, text):
    pygame.draw.rect(screen, BLUE, (x, y, w, h))
    text_surf = font.render(text, True, WHITE)
    screen.blit(text_surf, (x + w // 4, y + h // 4))

def determine_winner(player_hand, ai_hand, community_cards):
    player_score = sum([RANKS.index(card['rank']) for card in player_hand + community_cards])
    ai_score = sum([RANKS.index(card['rank']) for card in ai_hand + community_cards])
    
    if player_score > ai_score:
        return "Player Wins!"
    elif ai_score > player_score:
        return "AI Wins!"
    else:
        return "It's a Draw!"

def poker_game():
    global player_chips, ai_chips, pot, current_bet, community_cards, hands, game_phase, SCREEN_WIDTH, SCREEN_HEIGHT, screen, winner_text, bet_phase, raise_amount

    deck = create_deck()
    hands = deal_cards(deck)
    community_cards = [deck.pop() for _ in range(5)]
    showdown = False

    running = True
    num_community_cards = 0
    call_phase = False  # Додаємо фазу Call для контролю ставок без відкриття карт
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.size
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Bet
                if 50 <= mouse_x <= 200 and SCREEN_HEIGHT - 100 <= mouse_y <= SCREEN_HEIGHT - 50:
                    if player_chips >= big_blind and bet_phase == "initial":
                        current_bet = big_blind
                        player_chips -= current_bet
                        pot += current_bet
                        bet_phase = "flop"
                        num_community_cards = 3  
                        call_phase = False  # Після ставки call неактивний

                # Call (просто збільшення поту)
                elif 250 <= mouse_x <= 400 and SCREEN_HEIGHT - 100 <= mouse_y <= SCREEN_HEIGHT - 50:
                    if player_chips >= current_bet:
                        player_chips -= current_bet
                        pot += current_bet
                        call_phase = True

                # Raise (підвищує ставку і відкриває наступну карту)
                elif 450 <= mouse_x <= 600 and SCREEN_HEIGHT - 100 <= mouse_y <= SCREEN_HEIGHT - 50:
                    if player_chips >= current_bet + raise_amount:
                        pot += raise_amount
                        call_phase = False
                        if num_community_cards < 5:
                            num_community_cards += 1  
                        if num_community_cards == 5:
                            showdown = True

                # Fold
                elif 650 <= mouse_x <= 800 and SCREEN_HEIGHT - 100 <= mouse_y <= SCREEN_HEIGHT - 50:
                    ai_chips += pot 
                    pot = 0
                    deck = create_deck()
                    hands = deal_cards(deck)
                    community_cards = [deck.pop() for _ in range(5)]
                    current_bet = 0
                    num_community_cards = 0
                    showdown = False
                    bet_phase = "initial"
                    call_phase = False

        screen.fill(GREEN)
        draw_player_hands(hands)
        draw_community_cards(community_cards[:num_community_cards])

        if showdown:
            draw_ai_hands(hands['AI'], reveal=True)  
            winner_text = determine_winner(hands['Player'], hands['AI'], community_cards)
            print(winner_text)

            if winner_text == "Player Wins!":
                player_chips += pot  # Гравець забирає всі чипи з поту
                ai_chips -= pot  # AI втрачає чипи з поту
            elif winner_text == "AI Wins!":
                ai_chips += pot  # AI забирає всі чипи з поту
                player_chips -= pot  # Гравець втрачає чипи з поту
            else:
                # Нічия - повертаємо чипи обом гравцям
                player_chips += pot // 2
                ai_chips += pot // 2

            pot = 0

            text_surf = winner_font.render(winner_text, True, WHITE)
            screen.blit(text_surf, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 180))

            pygame.display.update()
            pygame.time.wait(3000)  

            deck = create_deck()
            hands = deal_cards(deck)
            community_cards = [deck.pop() for _ in range(5)]
            num_community_cards = 0
            showdown = False
        else:
            draw_ai_hands(hands['AI']) 

        create_button(50, SCREEN_HEIGHT - 100, 150, 50, "Bet")
        create_button(250, SCREEN_HEIGHT - 100, 150, 50, "Call")
        create_button(450, SCREEN_HEIGHT - 100, 150, 50, "Raise")
        create_button(650, SCREEN_HEIGHT - 100, 150, 50, "Fold")

        text_surf = font.render(f"Player Chips: {player_chips}   Pot: {pot}   AI Chips: {ai_chips}", True, WHITE)
        screen.blit(text_surf, (SCREEN_WIDTH // 2 - 300, 50))

        pygame.display.update()

        if not pygame.mixer.music.get_busy():
            play_random_music()


if __name__ == "__main__":
    play_random_music()  
    poker_game()
