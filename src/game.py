import pygame
import sys
import random

from background import Background
from duck import Duck
from pipe import Pipe
from sound_manager import SoundManager
from score_manager import ScoreManager
from menu_manager import MenuManager



class Game:
    def __init__(self):
        pygame.init()

        self.screen_width = 720     # Bildschirmbreite in px
        self.screen_height = 1080    # Bildschirmhöhe in px

        # Fenster fürs Spiel erzeugen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Clock für FPS (frames per second)
        self.clock = pygame.time.Clock() 

        # Hintergrund initialisieren
        self.background = Background(self.screen)

        # Ente positionieren
        self.duck = Duck(100, self.screen_height // 2)

        # Spielstatus
        self.running = True

        # Pipe-Verwaltung
        self.pipes = []
        self.pipe_timer = 0
        self.pipe_interval = 150  # Alle 90 Frames neue Pipe (~1,5 Sek bei 60 FPS)
        
        # Music und  Sound
        self.sound = SoundManager()
        self.sound.play_music()
        
        #Punkte System:
        self.score_manager = ScoreManager(self.screen_width)



    def run(self):
        while self.running:

            # ---------- Ereignisse (Tasteneingaben etc.) ----------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.duck.flap()
                    self.sound.play_flap() 

            # ---------- Hintergrund ----------
            self.background.draw()

            # ---------- Ente ----------
            self.duck.update()
            self.duck.draw(self.screen)

            # ----------- Bildschirmgrenzen prüfen ----------
            if self.duck.rect.top <= 0:
                self.running = False  # Ente fliegt zu hoch

            if self.duck.rect.bottom >= self.screen_height:
                self.running = False  # Ente fällt unten raus

            # ---------- Neue Pipes erzeugen ----------
            self.pipe_timer += 1
            if self.pipe_timer >= self.pipe_interval:
                new_pipe = Pipe(self.screen_width, self.screen_height)
                self.pipes.append(new_pipe)
                self.pipe_timer = 0

            # ---------- Pipes aktualisieren, zeichnen und prüfen ----------
            for pipe in self.pipes:
                pipe.update()
                pipe.draw(self.screen)
                # pipe.draw_debug_rects(self.screen)  # Debug: Kollision anzeigen

                if pipe.check_collision(self.duck.hitbox): 
                    self.running = False  # Game Over
                
                if not hasattr(pipe, "passed"):
                    pipe.passed = False

                if not pipe.passed and pipe.x + pipe.pipe_width < self.duck.rect.left:
                    pipe.passed = True
                    self.score_manager.increase()
 

            # ---------- Alte Pipes entfernen ----------
            self.pipes = [p for p in self.pipes if p.x + p.pipe_width > 0]

            # ---------- Socre Anzeigen ----------
            self.score_manager.draw(self.screen)

            # ---------- Anzeige aktualisieren ----------
            pygame.display.update()
            self.clock.tick(60)

        # ---------- Spiel beenden ----------
        pygame.quit()
        sys.exit()


# ---------- Spiel starten ----------
if __name__ == "__main__":
    pygame.init()
    screen_width = 720
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Menü starten
    from menu_manager import MenuManager
    menu = MenuManager(screen)
    start_game = menu.run_menu()

    if start_game:
        # Hauptspiel starten
        from game import Game
        game = Game()
        game.run()
