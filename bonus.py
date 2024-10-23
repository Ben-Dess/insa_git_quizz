import pygame
import time
import sqlite3

# Classe créant un curseur personnalisé
class curseur:
    def __init__(self, image_path):
        # Charge l'image du curseur personnalisé
        self.cursor_img = pygame.image.load(image_path).convert_alpha()
        # Désactive le curseur par défaut
        pygame.mouse.set_visible(False)
        
    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.blit(self.cursor_img, (mouse_x, mouse_y))
    def set_visible(self, visible):
        pygame.mouse.set_visible(visible)

# Fonction d'un chronomètre de durée définie (en secondes)
def start_timer(duration):
    start_time = time.time()  # Enregistre l'heure de départ
    return start_time, duration

# Fonction pour vérifier si le temps est écoulé
def is_time_up(start_time, duration):
    elapsed_time = time.time() - start_time
    if elapsed_time >= duration:
        return True
    return False

# Fonction pour afficher le temps restant à l'écran
def draw_timer(screen, font, start_time, duration, x, y):
    remaining_time = max(0, int(duration - (time.time() - start_time)))  # Temps restant
    timer_text = font.render(f'Temps restant: {remaining_time}s', True, (255, 0, 0))
    screen.blit(timer_text, (x, y))

# Fonction permettant d'insérer de nouvelles données à la base de données
def add_question_to_db(question, reponses, theme, difficulty):
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('questions.sqlite')
        cursor = conn.cursor()
        
        # Insertion de la question
        cursor.execute(
            "INSERT INTO questions (question_text, theme, difficulty) VALUES (?, ?, ?)",
            (question, theme, difficulty)
        )
        question_id = cursor.lastrowid  # ID de la question 
        
        # Insertion des réponses
        for i, reponse in enumerate(reponses):
            is_correct = (i == 0)  # Supposons que la première réponse soit la bonne
            cursor.execute(
                "INSERT INTO reponses (question_id, reponse_text, is_correct) VALUES (?, ?, ?)",
                (question_id, reponse, is_correct)
            )
        
        # Validation du formulaire
        conn.commit()
        print("Question et réponses insérées avec succès dans la base de données !")
    
    except sqlite3.Error as e:
        print(f"Erreur lors de l'insertion dans la base de données: {e}")
    
    finally:
        conn.close()  


# Fonctions permettant de récupérer les thèmes et les difficultés des tables Thematique et Question
def get_theme():
    conn = sqlite3.connect("questions.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT nomTheme FROM Thematique")
    themes = cursor.fetchall()
    conn.close()
    return [theme[0] for theme in themes]  

def get_difficulties():
    conn = sqlite3.connect("questions.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT diff FROM Question")
    difficulties = cursor.fetchall()
    conn.close()
    return [difficulty[0] for difficulty in difficulties]  