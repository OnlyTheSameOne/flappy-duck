import pygame
import os

class Duck:
    def __init__(self, x, y):
        # Hier kommt später das Laden, die Physik- und Animations-Initialisierung rein

        # Pfad zum assets/images
        images_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
        # Sprite-Sheet
        sheet_path = os.path.join(images_dir, "duck_jump_v1.png")
        sheet = pygame.image.load(sheet_path).convert_alpha()

        # Berechne Frame-Größe (4 Frames nebeneinander)
        frame_count = 4
        sheet_w, sheet_h = sheet.get_size()
        frame_w = sheet_w // frame_count
        frame_h = sheet_h

        # Die Ente Hochskallieren
        target_width  = 96   # px breit
        target_height = 100  # px hoch
        
        # Flag für die Animation (Konrollpunkt)
        self.animating = False

        """ --- Animation: Alle 4 Frames aus dem Sheet herausschneiden und skalieren ---"""
        self.frames = []                    # Liste für alle Einzelbilder

        for i in range(frame_count):        # frame_count ist 4
            rect = pygame.Rect(i * frame_w, 0, frame_w, frame_h)
            frame_surf = sheet.subsurface(rect).copy()
            # Auf Zielgröße (100×80 o.ä.) skalieren und Alpha beibehalten
            frame_surf = pygame.transform.scale(frame_surf, (target_width, target_height)).convert_alpha()
            self.frames.append(frame_surf)
        
        # Starte mit dem ersten Frame
        self.current_frame  = 0
        self.image          = self.frames[self.current_frame]

        # Passe das Kollisions-Rechteck an das aktuelle Bild an und zentriere es auf (x, y)
        self.rect           = self.image.get_rect(center=(x, y))

        # Werte für die Hitbox-Verkleinerung
        self.hitbox_shrink_w = 0.65 # 50% schmaler
        self.hitbox_shrink_h = 0.65  # 50% kürzer

        # Rechteck fürs Kollisionssystem kleiner machen
        self.hitbox = self.rect.inflate(
            -self.rect.width  * self.hitbox_shrink_w,
            -self.rect.height * self.hitbox_shrink_h
        )

        """--------------------------------------------------------------------------"""

        # Physik-Parameter
        self.velocity_y    = 0
        self.gravity       = 0.25
        self.flap_strength = -6

        self.x = x
        self.y = y

        """--- Timer für den Frame-Wechsel initalisiern ---"""
        self.last_anim_time = pygame.time.get_ticks() # Zeitpunkt des letzten Wechsels
        self.anim_speed = 100 # ms pro Frame (also die dauere eines frames)
        """-------------------------------------------------"""

    def flap(self):
        # Später: Impuls nach oben setzen

        """
        Wird aufgerufen, wenn der Spieler flattert (z. B. Leertaste).
        Setzt self.velocity_y auf den negativen Flap-Impuls, sodass die Ente
        nach oben geschnellt wird.
        """

        self.velocity_y = self.flap_strength

        # Animation starten
        self.animating = True

    def update(self):
        # Schwerkraft anwenden: velocity_y um gravity erhöhen
        self.velocity_y += self.gravity

        # Vertikale Position um velocity_y verschieben
        self.y += self.velocity_y

        # Das Rechteck mit neuer Mittelpunkts-Y aktualisieren
        self.rect.centery = self.y

        # Nur animieren, wenn gerade geflattert wird:
        if self.animating:
            # Frame wechsel, wenn genug Zeit vergangen ist
            now = pygame.time.get_ticks()
            if now - self.last_anim_time > self.anim_speed:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image         = self.frames[self.current_frame]
                self.last_anim_time = now

            # Wenn die Ente den Scheitelpunkt erreicht (velocity_y ≥ 0),
            # beende die Flatter-Animation und setze Bild auf Frame 0
            if self.velocity_y >= 0:
                self.animating     = False
                self.current_frame = 0
                self.image         = self.frames[0]
        else:
            # Idle: immer nur das erste Frame anzeigen
            self.image = self.frames[0]

        # Hitbox immer an rect-Mitte anpassen
        self.hitbox.center = self.rect.center

    def draw(self, surface):
        # Später: Aktuelles Bild auf die gegebene Surface blitten

        # <Blit das aktuelle Frame-Surface an die Stelle, die self.rect vorgibt
        surface.blit(self.image, self.rect)
        # Debug-Hitbox anzeigen (gelber Rahmen)
        #pygame.draw.rect(surface, (255, 255, 0), self.hitbox, 2)
