# Bibliotheken importieren
import pygame
import sys
import random

# Pygame initialisieren
pygame.init()
clock = pygame.time.Clock()

# Bildschirmgrößen definieren
screen_width, screen_height = 800, 700
game_field_height = 600

# Bildschirm erstellen und Titel setzen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('1vs1 Fußballspiel | by Ismail')

# Farben definieren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)

# Sound initialisieren und laden
pygame.mixer.init()
kick_sound = pygame.mixer.Sound('fussball_assets/kick.wav')
goal_sound = pygame.mixer.Sound('fussball_assets/goal.wav')
goal_sound2 = pygame.mixer.Sound('fussball_assets/goal2.wav')
goal_sound3 = pygame.mixer.Sound('fussball_assets/goal3.wav')
victory_sound = pygame.mixer.Sound('fussball_assets/victory.wav')

# Hintergrundmusik laden und abspielen
pygame.mixer.music.load('fussball_assets/background.wav')
pygame.mixer.music.play(-1)  # Endlosschleife
pygame.mixer.music.set_volume(0.1)
volume = 0.1  # Anfangslautstärke

# Hintergrundbilder laden und anpassen
background_images = []
for i in range(1, 4):
    bg = pygame.image.load(f'fussball_assets/background{i}.jpg')
    bg = pygame.transform.scale(bg, (screen_width, game_field_height))
    background_images.append(bg)

# Menü-Hintergrund laden
menu_background = pygame.image.load('fussball_assets/menu_background.jpg')
menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))

# Spielerbilder laden und skalieren
player_images = []
player_size = 50
for i in range(1, 8):
    img = pygame.image.load(f'fussball_assets/player{i}.png')
    img = pygame.transform.scale(img, (player_size, player_size))
    player_images.append(img)

# Teamlogos laden und skalieren
logo1 = pygame.image.load('fussball_assets/logo_team1.png')
logo1 = pygame.transform.scale(logo1, (40, 40))
logo2 = pygame.image.load('fussball_assets/logo_team2.png')
logo2 = pygame.transform.scale(logo2, (40, 40))

# Startmenü zur Moduswahl
def start_menu():
    font = pygame.font.Font(None, 50)
    options = ['Singleplayer', 'Multiplayer']
    option_rects = []

    while True:
        screen.blit(menu_background, (0, 0))
        option_rects.clear()

        for i, option in enumerate(options):
            text_surf = font.render(f'{i+1}. {option}', True, BLACK)
            x = screen_width // 2 - text_surf.get_width() // 2
            y = 250 + i * 70
            rect = pygame.Rect(x - 10, y - 5, text_surf.get_width() + 20, text_surf.get_height() + 10)
            option_rects.append(rect)
            screen.blit(text_surf, (x, y))

        # Hover-Effekt
        mouse_pos = pygame.mouse.get_pos()
        for rect in option_rects:
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, BLACK, rect, 2)

        pygame.display.flip()

        # Events abfragen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(event.pos):
                        return 'singleplayer' if i == 0 else 'multiplayer'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'singleplayer'
                elif event.key == pygame.K_2:
                    return 'multiplayer'


# Schwierigkeit auswählen
def choose_difficulty():
    font = pygame.font.Font(None, 50)
    options = ['Normal', 'Schwer']
    option_rects = []

    while True:
        screen.blit(menu_background, (0, 0))
        option_rects.clear()

        for i, option in enumerate(options):
            text_surf = font.render(f'{i+1}. {option}', True, BLACK)
            x = screen_width // 2 - text_surf.get_width() // 2
            y = 280 + i * 60
            rect = pygame.Rect(x - 10, y - 5, text_surf.get_width() + 20, text_surf.get_height() + 10)
            option_rects.append(rect)
            screen.blit(text_surf, (x, y))

        # Hover-Effekt
        mouse_pos = pygame.mouse.get_pos()
        for rect in option_rects:
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, BLACK, rect, 2)

        pygame.display.flip()

        # Eingaben abfragen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(event.pos):
                        return 'normal' if i == 0 else 'hard'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'normal'
                elif event.key == pygame.K_2:
                    return 'hard'


# Namen der Spieler eingeben
def get_player_names(singleplayer=False):
    input_active1 = True
    input_active2 = not singleplayer
    player1_name, player2_name = '', 'KI'  # Bei Singleplayer ist Spieler 2 die KI
    font = pygame.font.Font(None, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if input_active1:
                    if event.key == pygame.K_RETURN and player1_name:
                        input_active1 = False
                        if not singleplayer:
                            input_active2 = True
                        else:
                            return player1_name, player2_name
                    elif event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    else:
                        player1_name += event.unicode
                elif input_active2:
                    if event.key == pygame.K_RETURN and player2_name:
                        return player1_name, player2_name
                    elif event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    else:
                        player2_name += event.unicode

        # Anzeige auf dem Bildschirm
        screen.fill(RED if input_active1 else BLUE)
        prompt = 'Name Spieler 1 (Rot):' if input_active1 else 'Name Spieler 2 (Blau):'
        prompt_text = font.render(prompt, True, WHITE)
        input_text = font.render(player1_name if input_active1 else player2_name, True, WHITE)
        screen.blit(prompt_text, (screen_width // 2 - prompt_text.get_width() // 2, 200))
        screen.blit(input_text, (screen_width // 2 - input_text.get_width() // 2, 300))
        pygame.display.flip()
        clock.tick(30)


# Hintergrund auswählen
def choose_background():
    index = 0
    font = pygame.font.Font(None, 50)
    while True:
        screen.blit(background_images[index], (0, 100))
        text = font.render(f'Spielfeld {index+1}', True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, 650))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    index = (index + 1) % len(background_images)
                elif event.key == pygame.K_LEFT:
                    index = (index - 1) % len(background_images)
                elif event.key == pygame.K_RETURN:
                    return background_images[index]


# Spieler auswählen (jeweils ein Bild)
def choose_players():
    index1, index2 = 0, 1
    font = pygame.font.Font(None, 40)
    large_player_size = 150
    large_player_images = [pygame.transform.scale(img, (large_player_size, large_player_size)) for img in player_images]

    while True:
        screen.fill(WHITE)
        text1 = font.render('Wähle Spieler 1 (A/D) & Spieler 2 (PfeilLinks/PfeilRechts)', True, BLACK)
        text2 = font.render('Drücke ENTER zum Bestätigen', True, BLACK)
        screen.blit(text1, (screen_width // 2 - text1.get_width() // 2, 40))
        screen.blit(text2, (screen_width // 2 - text2.get_width() // 2, 80))
        screen.blit(large_player_images[index1], (250, 250))
        screen.blit(large_player_images[index2], (500, 250))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    index1 = (index1 - 1) % len(player_images)
                elif event.key == pygame.K_d:
                    index1 = (index1 + 1) % len(player_images)
                elif event.key == pygame.K_LEFT:
                    index2 = (index2 - 1) % len(player_images)
                elif event.key == pygame.K_RIGHT:
                    index2 = (index2 + 1) % len(player_images)
                elif event.key == pygame.K_RETURN:
                    return player_images[index1], player_images[index2]


# Spiel ausführen
def play_game():
    global volume

    player1_image, player2_image = (player_images[0], player_images[0]) if mode == 'singleplayer' else choose_players()

    # Positionen setzen
    player1 = pygame.Rect(700, 250 + 100, player_size, player_size)
    player2 = pygame.Rect(100, 250 + 100, player_size, player_size)
    ball = pygame.Rect(400, 300 + 100, 30, 30)
    ball_speed = [random.choice([-5, 5]), random.choice([-5, 5])]
    score_red = 0
    score_blue = 0

    # Tore
    goal_left = pygame.Rect(0, 250 + 100, 10, 100)
    goal_right = pygame.Rect(screen_width - 10, 250 + 100, 10, 100)

    message = ''
    message_timer = 0
    winning_score = 3
    start_time = pygame.time.get_ticks()

    running = True
    while running:
        # Events abfragen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Lautstärke einstellen
                if event.key in (pygame.K_PLUS, pygame.K_KP_PLUS):
                    volume = min(1.0, volume + 0.05)
                    pygame.mixer.music.set_volume(volume)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    volume = max(0.0, volume - 0.05)
                    pygame.mixer.music.set_volume(volume)

        keys = pygame.key.get_pressed()

        # Steuerung Spieler 1
        if keys[pygame.K_UP] and player1.top > 100:
            player1.y -= 5
        if keys[pygame.K_DOWN] and player1.bottom < screen_height:
            player1.y += 5
        if keys[pygame.K_LEFT] and player1.left > 0:
            player1.x -= 5
        if keys[pygame.K_RIGHT] and player1.right < screen_width:
            player1.x += 5

        # Spieler 2 manuell oder automatisch (KI)
        if mode == 'multiplayer':
            if keys[pygame.K_w] and player2.top > 100:
                player2.y -= 5
            if keys[pygame.K_s] and player2.bottom < screen_height:
                player2.y += 5
            if keys[pygame.K_a] and player2.left > 0:
                player2.x -= 5
            if keys[pygame.K_d] and player2.right < screen_width:
                player2.x += 5
        else:
            speed = 4 if difficulty == 'normal' else 6
            if ball.centery > player2.centery:
                player2.y += speed
            elif ball.centery < player2.centery:
                player2.y -= speed
            player2.clamp_ip(pygame.Rect(0, 100, screen_width, game_field_height))

        # Ballbewegung & Kollision
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        if ball.top <= 100 or ball.bottom >= screen_height:
            ball_speed[1] = -ball_speed[1]

        if ball.colliderect(player1) or ball.colliderect(player2):
            kick_sound.play()
            ball_speed[0] = -ball_speed[0]

        # Tore zählen
        if ball.colliderect(goal_left):
            score_red += 1
            goal_sound.play()
            ball.center = (screen_width // 2, game_field_height // 2 + 100)
            ball_speed = [random.choice([-5, 5]), random.choice([-5, 5])]
            message = f'{player1_name} hat ein Tor geschossen!'
            message_timer = pygame.time.get_ticks()

        if ball.colliderect(goal_right):
            score_blue += 1
            goal_sound2.play()
            ball.center = (screen_width // 2, game_field_height // 2 + 100)
            ball_speed = [random.choice([-5, 5]), random.choice([-5, 5])]
            message = f'{player2_name} hat ein Tor geschossen!'
            message_timer = pygame.time.get_ticks()

        # Ball nicht hinter Tor lassen
        if ball.left < 0:
            ball.left = 0
            ball_speed[0] = -ball_speed[0]
        if ball.right > screen_width:
            ball.right = screen_width
            ball_speed[0] = -ball_speed[0]

        # Siegbedingung prüfen
        if score_blue >= winning_score:
            victory_sound.play()
            message = f'{player2_name} hat gewonnen!'
            show_message(message)
            running = False
        elif score_red >= winning_score:
            victory_sound.play()
            message = f'{player1_name} hat gewonnen!'
            show_message(message)
            running = False

        # Spielzeit anzeigen
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = f'{minutes:02}:{seconds:02}'

        # UI anzeigen
        screen.fill(BLACK)
        pygame.draw.rect(screen, GRAY, (0, 0, screen_width, 100))
        screen.blit(logo2, (10, 30))
        screen.blit(logo1, (screen_width - 50, 30))

        name_font = pygame.font.Font(None, 36)
        score_font = pygame.font.Font(None, 50)
        timer_font = pygame.font.Font(None, 36)
        message_font = pygame.font.Font(None, 40)

        name1_surf = name_font.render(player2_name, True, BLUE)
        name2_surf = name_font.render(player1_name, True, RED)
        screen.blit(name1_surf, (60, 35))
        screen.blit(name2_surf, (screen_width - 150, 35))

        score_text = score_font.render(f'{score_blue} : {score_red}', True, WHITE)
        score_x = screen_width // 2 - score_text.get_width() // 2
        score_y = 20
        screen.blit(score_text, (score_x, score_y))

        timer_surf = timer_font.render(timer_text, True, WHITE)
        timer_x = screen_width // 2 - timer_surf.get_width() // 2
        timer_y = score_y + score_text.get_height() + 5
        screen.blit(timer_surf, (timer_x, timer_y))

        # Lautstärkebalken anzeigen
        volume_bar_pos = (score_x + score_text.get_width() + 20, 35)
        volume_bar_size = (100, 20)
        volume_rect = pygame.Rect(volume_bar_pos, volume_bar_size)
        pygame.draw.rect(screen, BLACK, volume_rect)
        fill_width = int(volume * volume_bar_size[0])
        fill_rect = pygame.Rect(volume_bar_pos, (fill_width, volume_bar_size[1]))
        pygame.draw.rect(screen, BLUE, fill_rect)
        vol_percent = int(volume * 100)
        vol_text = name_font.render(f'Vol: {vol_percent}%', True, WHITE)
        screen.blit(vol_text, (volume_bar_pos[0], volume_bar_pos[1] - 25))

        # Spielfeld und Objekte zeichnen
        screen.blit(background, (0, 100))
        screen.blit(player1_image, player1.topleft)
        screen.blit(player2_image, player2.topleft)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.rect(screen, WHITE, goal_left)
        pygame.draw.rect(screen, WHITE, goal_right)

        # Tormeldung anzeigen
        if message and pygame.time.get_ticks() - message_timer < 2000:
            msg_surface = message_font.render(message, True, RED)
            screen.blit(msg_surface, (screen_width // 2 - msg_surface.get_width() // 2, 150))
        else:
            message = ''

        pygame.display.flip()
        clock.tick(60)


# Nachricht für eine bestimmte Zeit anzeigen
def show_message(text, duration=3000):
    font = pygame.font.Font(None, 70)
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        msg_surface = font.render(text, True, WHITE)
        screen.blit(msg_surface, (screen_width // 2 - msg_surface.get_width() // 2,
                                  screen_height // 2 - msg_surface.get_height() // 2))
        pygame.display.flip()
        clock.tick(60)


# Hauptprogramm
while True:
    mode = start_menu()
    if mode == 'singleplayer':
        difficulty = choose_difficulty()
    else:
        difficulty = None
    player1_name, player2_name = get_player_names(singleplayer=(mode == 'singleplayer'))
    background = choose_background()
    play_game()