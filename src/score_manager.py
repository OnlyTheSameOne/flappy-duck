import pygame

class ScoreManager:
    def __init__(self, screen_width):
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 60, bold=True)
        self.color = (255, 255, 255)  # weiß
        self.screen_width = screen_width

    def draw(self, surface):
        """Zeigt den aktuellen Score zentriert oben auf dem Bildschirm."""
        text_surf = self.font.render(str(self.score), True, self.color)
        text_rect = text_surf.get_rect(center=(self.screen_width // 2, 80))
        surface.blit(text_surf, text_rect)

    def increase(self):
        """Erhöht den Score um 1 Punkt."""
        self.score += 1

    def reset(self):
        """Setzt den Score auf 0 zurück (z. B. bei Restart)."""
        self.score = 0
