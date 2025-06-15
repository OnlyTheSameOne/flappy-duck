import pygame
import sys
import subprocess

# Fenster & Setup
pygame.init()
screen_width, screen_height = 720, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SPIELSTARTER")

# Hintergrundfarbe
BACKGROUND_COLOR = (180, 220, 255)

# Buttons definieren
font = pygame.font.SysFont("Arial", 48, bold=True)
flappy_button = pygame.Rect(210, 450, 300, 80)
soccer_button = pygame.Rect(210, 580, 300, 80)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BACKGROUND_COLOR)

    # Flappy Duck Button
    pygame.draw.rect(screen, (255, 255, 255), flappy_button)
    pygame.draw.rect(screen, (0, 0, 0), flappy_button, 4)
    flappy_text = font.render("Flappy Duck", True, (0, 0, 0))
    screen.blit(flappy_text, (flappy_button.x + 40, flappy_button.y + 15))

    # Fußballspiel Button
    pygame.draw.rect(screen, (255, 255, 255), soccer_button)
    pygame.draw.rect(screen, (0, 0, 0), soccer_button, 4)
    soccer_text = font.render("Fußballspiel", True, (0, 0, 0))
    screen.blit(soccer_text, (soccer_button.x + 30, soccer_button.y + 15))

    pygame.display.update()
    clock.tick(60)

    # Events abfragen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if flappy_button.collidepoint(event.pos):
                pygame.quit()
                subprocess.call(["python", "src/game.py"])  
                sys.exit()
            elif soccer_button.collidepoint(event.pos):
                pygame.quit()
                subprocess.call(["python", "TestFinal.py"])
                sys.exit()
