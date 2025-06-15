import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        # Basispfad zu den Sounds
        base_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")

        # Hintergrundmusik
        self.music_path = os.path.join(base_path, "ingame_music.mp3")

        # Effekt-Sounds
        self.flap_sound = pygame.mixer.Sound(os.path.join(base_path, "Jump_sound.mp3"))
        self.flap_sound.set_volume(0.12)

    def play_music(self):
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.set_volume(0.112)
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_flap(self):
        self.flap_sound.play()
