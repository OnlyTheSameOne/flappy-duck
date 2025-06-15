import pygame        # Importiert die Pygame-Bibliothek, um später Surfaces laden und zeichnen zu können
import os            # Importiert das OS-Modul, um plattformunabhängig mit Dateipfaden zu arbeiten

class Background:
    def __init__(self, screen):
        # Konstruktor der Background-Klasse
        # Hier bekommt die Klasse eine Referenz auf das Pygame-Fenster (Surface) übergeben,
        # sodass wir in späteren Methoden direkt auf 'self.screen' zeichnen können.
        self.screen = screen

        # Ein sie Fenstermße auslesne füre die göße des Composite zu nutzen
        self.width = screen.get_width()
        self.height = screen.get_height() 

        # Mit den Fenstermaßen ein Surface erstellen das alle hintergund Bündelt
        self.composite = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA).convert_alpha()

        # Startpunkt für die verschiebung des Hintergundbilds
        self.x_offset = 0

        # Geschwindgkeit der (FPS), mit dem der Hintergrund nach links rutscht
        self.scroll_speed = 1


        # Erstelle den Pfad zum Ordner "assets/images"
        # - __file__ ist der Pfad dieser Datei (background.py)
        # - os.path.dirname(__file__) liefert den Ordner, in dem diese Datei liegt (also 'src')
        # - ".." geht eine Ebene nach oben in den Projekt-Root, dann weiter in 'assets/images'
        images_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "images")

        # Liste der vier Hintergrund-Dateinamen in der gewünschten Reihenfolge
        # Diese Reihenfolge bestimmt später, wie die Bilder vertikal gestapelt werden:
        # a.png ganz oben, dann b.png, c.png und zum Schluss d.png
        file_names = ["a.png", "b.png", "c.png", "d.png"]

        # An diesen Werten sollen die Bilder skalliert werdem
        target_width = 720
        target_height = 1080

        self.parts = [] #Liste für dei Geladenen Hintergund-Abschnitte

        for name in file_names:
            full_path = os.path.join(images_dir, name)
            image_surface = pygame.image.load(full_path).convert_alpha()
            
            # Skaliere das 576×324-Bild auf 720×1080
            scaled = pygame.transform.scale(image_surface, (target_width, target_height))
            self.composite.blit(scaled, (0, 0))

             # Debug: Größe des gerade geladenen Bildes ausgeben:
            print(f"Loaded '{name}' → width={image_surface.get_width()} px, height={image_surface.get_height()} px")

    def draw(self):
        """
        Zeichnet den zusammengesetzten Hintergrund (self.composite) in einer Endlosschleife,
        sodass er kontinuierlich nach links scrollt.
        """

        # Zeichne das Composite-Bild an der aktuellen X-Position (self.x_offset).
        # Wenn self.x_offset positiv ist, rückt das Bild nach rechts; wenn negativ, nach links.
        self.screen.blit(self.composite, (self.x_offset, 0))

        # Zeichne dieselbe Composite-Bild-Kopie direkt rechts daneben,
        # damit beim Scrollen keine Lücke entsteht, wenn die erste Kopie aus dem Fenster verschwindet.
        # self.x_offset + self.width ist genau die Breite des Fensters weiter rechts.
        self.screen.blit(self.composite, (self.x_offset + self.width, 0))

        # Verschiebe das Bild um 'scroll_speed' Pixel nach links.
        # (scroll_speed wurde im __init__ festgelegt, z.B. 1 px pro Frame)
        self.x_offset -= self.scroll_speed

        # Sobald das Bild komplett aus dem Fenster links herausgerutscht ist
        # (d.h. self.x_offset ≤ -self.width), setzen wir den Offset auf 0 zurück,
        # um nahtlos von vorne zu beginnen.
        if self.x_offset <= -self.width:
            self.x_offset = 0


