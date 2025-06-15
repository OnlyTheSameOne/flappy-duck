import pygame
import sys
from src.game import Game
import TestFinal

pygame.init()
screen = pygame.display.set_mode((720, 1080))
pygame.display.set_caption("Spielauswahl")
font = pygame.font.SysFont(None, 48)

while True:
    screen.fill((0, 0, 0))
    flappy_text = font.render("Flappy Duck starten", True, (255, 255, 255))
    fussball_text = font.render("Fußballspiel starten", True, (255, 255, 255))

    flappy_rect = flappy_text.get_rect(center=(360, 400))
    fussball_rect = fussball_text.get_rect(center=(360, 500))

    screen.blit(flappy_text, flappy_rect)
    screen.blit(fussball_text, fussball_rect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if flappy_rect.collidepoint(event.pos):
                Game().run()
            elif fussball_rect.collidepoint(event.pos):
                TestFinal.start_fussballspiel()