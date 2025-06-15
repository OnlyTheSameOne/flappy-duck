import pygame # Pygame-Bibliothek

#button class
class Button():
#{
	
	def __init__(self, x, y, image, scale): # Parmeter die von der Spiele datei erhjalten werden (alle parameter müsssen gegebn sein, damir die function damit weiter arbeiten kann)
	#{
		width = image.get_width() # Breite des Bildes mit der .get_witdh() Mehtode abfragen und in width abspeichern
		height = image.get_height() # Höhe des Bildes mit der .get_height() Mehtode abfragen und in height abspeichern
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))) # Kleine Mulitplkation umd die Knöpfe auf eine neue Größe zu skalliern
		self.rect = self.image.get_rect() # Kollisons Rechteck auf die Bilder Packen
		self.rect.topleft = (x, y) # Die Koordinaten der Knöpfe auf dem Bildschirm
		self.clicked = False # Wird benötigt um nur einen einzigen Click ausführen zu lassen
    #}
    
	def draw(self, surface): # Der Parameter Surface dient dazu meien screen aus der Pygame Spiele Datei hinzugeben zu können
		#{
		action = False # Dient als Rückgabewert um jeden knopf eine unterschiedliche aufgeb zu geben 

		# Die Mehtode zur bestimmung dert Maus gibt die kordinaten zurück
		pos = pygame.mouse.get_pos()

		# Mit Hielfe der Kollisons erkennung die Position der Maus überprüfewn
		# Ob die Maus auf einen der Boutton drauf ist
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # 0 Steht für Links_Click: Wenn ein Links_click gemacht wurde und self. clicked Falsch ist:
				self.clicked = True # Ermöglicht das wiederholte drücken 
				action = True # Der Rückgabewert wird auf True gesetzt und ins Hauptspiel weitergegebn 

		if pygame.mouse.get_pressed()[0] == 0: # Wenn der Button nicht mehr gedrückt wird, self.clicked = Falsch
			self.clicked = False # Wenn self.clicked wieder Flasch ist, wird der Button quasi zurück gesetzt damit man nochmal frücken kann

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action # Rückgabewert der def draw function
		#}
#}