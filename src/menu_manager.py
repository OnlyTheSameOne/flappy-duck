import pygame
import os
from src.buttons import Button

class MenuManager:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = 720
        self.screen_height = 1080

        # Alle Layer (a bis d) als Gesamtbild zusammensetzen
        self.background = self.build_overlay_background(["a.png", "b.png", "c.png", "d.png"])

        # Pfad zu den Bildern
        img_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
        start_img = pygame.image.load(os.path.join(img_dir, "Start1.png")).convert_alpha()
        quit_img  = pygame.image.load(os.path.join(img_dir, "Quit1.png")).convert_alpha()

        # Buttons bisschen größer machen
        self.scale = 2.2
        button_width  = int(start_img.get_width() * self.scale)
        button_height = int(start_img.get_height() * self.scale)

        # Buttons mittig platzieren
        x_center = (self.screen_width - button_width) // 2
        start_y = self.screen_height // 2 + 50   # etwas tiefer setzen
        quit_y  = start_y + button_height + 15   # kleiner Abstand zwischen Start & Quit

        self.start_button = Button(x_center, start_y, start_img, self.scale)
        self.quit_button  = Button(x_center, quit_y,  quit_img,  self.scale)

        # Überschrift vorbereiten – groß und fett (weiße Schrift mit Schatten)
        self.title_font = pygame.font.SysFont("Arial", 80, bold=True)
        self.title_text = self.title_font.render("FLAPPY DUCK", True, (255, 255, 255))
        self.title_shadow = self.title_font.render("FLAPPY DUCK", True, (0, 0, 0))

        # Position vom Titel berechnen (oberhalb der Buttons)
        title_y = start_y - button_height - 60
        self.title_rect_shadow = self.title_shadow.get_rect(center=(self.screen_width // 2, title_y + 4))
        self.title_rect        = self.title_text.get_rect(center=(self.screen_width // 2, title_y))

    def build_overlay_background(self, filenames):
        # Lädt mehrere transparente PNGs und legt sie exakt übereinander (wie Ebenen)
        img_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
        base = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)

        for name in filenames:
            path = os.path.join(img_dir, name)
            layer = pygame.image.load(path).convert_alpha()
            layer_scaled = pygame.transform.scale(layer, (self.screen_width, self.screen_height))
            base.blit(layer_scaled, (0, 0))  # einfach alle Layer draufklatschen

        return base

    def run_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Hintergrundbild anzeigen
            self.screen.blit(self.background, (0, 0))

            # Titel anzeigen (erst Schatten, dann Text – für 3D-Effekt)
            self.screen.blit(self.title_shadow, self.title_rect_shadow)
            self.screen.blit(self.title_text, self.title_rect)

            # Buttons anzeigen & Reaktion prüfen
            if self.start_button.draw(self.screen):
                return True  # Spiel starten
            if self.quit_button.draw(self.screen):
                pygame.quit()
                exit()  # Spiel beenden

            pygame.display.update()
