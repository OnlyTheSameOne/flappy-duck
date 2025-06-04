import pygame        # Importiert die Pygame-Bibliothek, um später Surfaces laden und zeichnen zu können
import os            # Importiert das OS-Modul, um plattformunabhängig mit Dateipfaden zu arbeiten

class Background:
    def __init__(self, screen):
        # Konstruktor der Background-Klasse
        # Hier bekommt die Klasse eine Referenz auf das Pygame-Fenster (Surface) übergeben,
        # sodass wir in späteren Methoden direkt auf 'self.screen' zeichnen können.
        self.screen = screen

        # Erstelle den Pfad zum Ordner "assets/images"
        # - __file__ ist der Pfad dieser Datei (background.py)
        # - os.path.dirname(__file__) liefert den Ordner, in dem diese Datei liegt (also 'src')
        # - ".." geht eine Ebene nach oben in den Projekt-Root, dann weiter in 'assets/images'
        images_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "images")

        # Liste der vier Hintergrund-Dateinamen in der gewünschten Reihenfolge
        # Diese Reihenfolge bestimmt später, wie die Bilder vertikal gestapelt werden:
        # a.png ganz oben, dann b.png, c.png und zum Schluss d.png
        file_names = ["a.png", "b.png", "c.png", "d.png"]
