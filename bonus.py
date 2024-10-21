import pygame
import sys

class curseur:
    def __init__(self, image_path):
        # Charger l'image du curseur personnalisé
        self.cursor_img = pygame.image.load(image_path).convert_alpha()
        
        # Désactiver le curseur par défaut
        pygame.mouse.set_visible(False)
        
    def draw(self, screen):
        # Récupérer la position actuelle de la souris
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Dessiner l'image du curseur personnalisé à la position de la souris
        screen.blit(self.cursor_img, (mouse_x, mouse_y))

    def set_visible(self, visible):
        # Optionnel : changer la visibilité du curseur système si besoin
        pygame.mouse.set_visible(visible)


