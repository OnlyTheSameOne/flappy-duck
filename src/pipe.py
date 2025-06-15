import pygame      # Für Grafik, Surface, Rect usw.
import os          # Um Bildpfade sicher zu laden
import random      # Für zufällige Position der Lücke



class Pipe:
    def __init__(self, x, screen_height):
        """
        Konstruktor für ein einzelnes Hindernis-Rohrpaar (oben + unten).
        Parameter:
        - x: Die Startposition der Pipe auf der X-Achse (normal rechts außerhalb des Screens)
        - screen_height: Höhe des Fensters, wird benötigt zur Berechnung der Lücke
        """
        self.x = x                      # Aktuelle X-Position der Pipe
        self.screen_height = screen_height
        self.speed = 4                 # Bewegungsgeschwindigkeit (nach links)

        self.pipe_width = 96           # Zielbreite der Pipe
        self.pipe_height = 64          # Höhe eines Segment-Teils
        self.gap_size = 150       # Abstand zwischen oberem und unterem Rohr (Spiel-Lücke)

        # Die Y-Position der Lücke zufällig setzen, aber mit Sicherheitsabstand oben/unten
        self.gap_y = random.randint(100, self.screen_height - 100 - self.gap_size)
        
        self.load_images()  # Bilder vorbereiten

    def load_images(self):
        """
        Lädt die Rohrbilder (Segment + Kopf oben/unten)
        und skaliert sie auf die gewünschte Breite/Höhe.
        """

        # Pfad zum Ordner assets/images
        base_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images")

        # Bildpfade aufbauen
        segment_path    = os.path.join(base_path, "pipe_segment.png")
        head_up_path    = os.path.join(base_path, "pipe_head_up.png")
        head_down_path  = os.path.join(base_path, "pipehead_down.png")

        # Bilder laden mit Transparenz
        self.segment_img   = pygame.image.load(segment_path).convert_alpha()
        self.head_up_img   = pygame.image.load(head_up_path).convert_alpha()
        self.head_down_img = pygame.image.load(head_down_path).convert_alpha()

        # Bilder auf Zielgröße skalieren
        size = (self.pipe_width, self.pipe_height)
        self.segment_img   = pygame.transform.scale(self.segment_img, size)
        self.head_up_img   = pygame.transform.scale(self.head_up_img, size)
        self.head_down_img = pygame.transform.scale(self.head_down_img, size)

    def update(self):
        """
        Bewegt die Pipe nach links und berechnet die aktuellen Kollisionsflächen
        für obere und untere Rohrteile (inkl. Kopf). Die Größe der Hitboxen kann
        über Padding-Werte justiert werden, um das Spielgefühl fein abzustimmen.
        """

        # Die Pipe scrollt nach links über den Bildschirm
        self.x -= self.speed

        # Kollision-Verkleinerung (Padding): Je höher die Werte, desto fairer wird die Hitbox
        collision_padding_x = 5   # reduziert die Breite links/rechts der Hitbox
        collision_padding_y = 5  # reduziert die Höhe oben/unten der Hitbox

        # Alte Rechtecke leeren, damit wir aktuelle berechnen können
        self.top_rects = []
        self.bottom_rects = []

        # ----------- Obere Segmente (bis kurz vor der Lücke) -----------
        y = 0
        while y + self.pipe_height < self.gap_y:
            rect = pygame.Rect(
                self.x + collision_padding_x,
                y + collision_padding_y,
                self.pipe_width - 2 * collision_padding_x,
                self.pipe_height - 2 * collision_padding_y
            )
            self.top_rects.append(rect)
            y += self.pipe_height

        #  Kopf oben (zeigt nach unten) direkt über der Lücke
        self.top_rects.append(
            pygame.Rect(
                self.x + collision_padding_x,
                self.gap_y - self.pipe_height + collision_padding_y,
                self.pipe_width - 2 * collision_padding_x,
                self.pipe_height - 2 * collision_padding_y
            )
        )

        # ----------- Untere Segmente (beginnt direkt nach der Lücke) -----------
        y = self.gap_y + self.gap_size

        # Kopf unten (zeigt nach oben) direkt unter der Lücke
        self.bottom_rects.append(
            pygame.Rect(
                self.x + collision_padding_x,
                y + collision_padding_y,
                self.pipe_width - 2 * collision_padding_x,
                self.pipe_height - 2 * collision_padding_y
            )
        )

        y += self.pipe_height

        # Untere Segmente (bis ganz zum Bildschirmrand)
        while y + self.pipe_height <= self.screen_height:
            rect = pygame.Rect(
                self.x + collision_padding_x,
                y + collision_padding_y,
                self.pipe_width - 2 * collision_padding_x,
                self.pipe_height - 2 * collision_padding_y
            )
            self.bottom_rects.append(rect)
            y += self.pipe_height



    def draw(self, surface):
        """
        Zeichnet die Pipe mit Segmenten und genau platzierten Köpfen.
        Keine Lücken zwischen Segment und Kopf. Lücke entsteht zwischen den Köpfen.
        """

        # ----------- Obere Seite ------------
        y = 0

        # Segmente bis kurz vor dem Kopf stapeln
        while y + self.pipe_height < self.gap_y - self.pipe_height:
            surface.blit(self.segment_img, (self.x, y))
            y += self.pipe_height

        # Letztes Segment direkt über dem Kopf (wenn nötig)
        if y + self.pipe_height < self.gap_y:
            surface.blit(self.segment_img, (self.x, y))
            y += self.pipe_height

        # Kopfteil oben (zeigt nach unten)
        surface.blit(self.head_down_img, (self.x, self.gap_y - self.pipe_height))

        # ----------- Untere Seite ------------
        y = self.gap_y + self.gap_size

        # Kopfteil unten (zeigt nach oben)
        surface.blit(self.head_up_img, (self.x, y))
        y += self.pipe_height

        # Segmente bis zum Bildschirmende
        while y < self.screen_height:
            surface.blit(self.segment_img, (self.x, y))
            y += self.pipe_height

    def check_collision(self, duck_rect):
        """
        Prüft, ob das Rechteck der Ente mit einem Teil der Rohr-Kollisionen überschneidet.
        Gibt True zurück, wenn es zu einer Kollision kommt (Game Over).
        """
        # Alle Kollisionsrechtecke durchgehen
        for rect in self.top_rects + self.bottom_rects:
            if duck_rect.colliderect(rect):
                return True  # Kollision erkannt

        return False  # Kein Treffer
    

    def draw_debug_rects(self, surface):
        """
        Zeichnet die Kollision-Rechtecke zur visuellen Überprüfung (Debug-Anzeige).
        """
        # Rote Rechtecke: obere Pipe
        for rect in self.top_rects:
            pygame.draw.rect(surface, (255, 0, 0), rect, 2)  # Rot, 2 Pixel dick

        # Grüne Rechtecke: untere Pipe
        for rect in self.bottom_rects:
            pygame.draw.rect(surface, (0, 255, 0), rect, 2)  # Grün, 2 Pixel dick
