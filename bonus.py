import pygame
import time
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

# Fonction pour démarrer un chronomètre de durée définie (en secondes)
def start_timer(duration):
    start_time = time.time()  # Enregistre l'heure de départ
    return start_time, duration

# Fonction pour vérifier si le temps est écoulé
def is_time_up(start_time, duration):
    elapsed_time = time.time() - start_time
    if elapsed_time >= duration:
        return True
    return False

# Fonction pour dessiner le temps restant à l'écran
def draw_timer(screen, font, start_time, duration, x, y):
    remaining_time = max(0, int(duration - (time.time() - start_time)))  # Temps restant
    timer_text = font.render(f'Temps restant: {remaining_time}s', True, (255, 0, 0))
    screen.blit(timer_text, (x, y))
