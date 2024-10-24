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

# Fonctions permettant d'insérer de nouvelles données à la base de données

def insert_response(conn, response_text):
    """Insère une nouvelle réponse dans la table Reponses si elle n'existe pas déjà."""
    cur = conn.cursor()
    cur.execute("SELECT idReponse FROM Reponses WHERE title = ?", (response_text,))
    result = cur.fetchone()
    
    if result:
        print(f"La réponse '{response_text}' existe déjà avec l'ID {result[0]}.")
        return result[0]
    else:
        sql = '''INSERT INTO Reponses (title) VALUES (?)'''
        print(f"Exécution de la requête : {sql} avec les valeurs : ({response_text},)")
        cur.execute(sql, (response_text,))
        conn.commit()
        print(f"Insertion de la réponse '{response_text}' réussie avec l'ID {cur.lastrowid}.")
        return cur.lastrowid

def insert_question(conn, question_text, correct_response_id, difficulty):
    """Insère une nouvelle question dans la table Question avec l'ID de la bonne réponse."""
    sql = '''INSERT INTO Question (idBonneRep, title, diff) VALUES (?, ?, ?)'''
    cur = conn.cursor()
    print(f"Exécution de la requête : {sql} avec les valeurs : ({correct_response_id}, {question_text}, {difficulty})")
    cur.execute(sql, (correct_response_id, question_text, difficulty))
    conn.commit()
    print(f"Insertion de la question '{question_text}' réussie avec l'ID {cur.lastrowid}.")
    return cur.lastrowid

def insert_question_response(conn, question_id, response_id):
    """Insère un lien entre la question et une réponse dans la table QuestionReponses."""
    sql = '''INSERT INTO QuestionReponses (idQuestion, idReponse) VALUES (?, ?)'''
    cur = conn.cursor()
    print(f"Exécution de la requête : {sql} avec les valeurs : ({question_id}, {response_id})")
    cur.execute(sql, (question_id, response_id))
    conn.commit()
    print(f"Liaison entre la question ID {question_id} et la réponse ID {response_id} réussie.")

def insert_theme_question(conn, question_id, theme_id):
    """Insère un lien entre une question et un thème dans la table ThemeQuestion."""
    sql = '''INSERT INTO ThemeQuestion (idQuestion, idTheme) VALUES (?, ?)'''
    cur = conn.cursor()
    print(f"Exécution de la requête : {sql} avec les valeurs : ({question_id}, {theme_id})")
    cur.execute(sql, (question_id, theme_id))
    conn.commit()
    print(f"Liaison entre la question ID {question_id} et le thème ID {theme_id} réussie.")


# Fonctions permettant de récupérer les thèmes et les difficultés des tables Thematique et Question
def get_theme_form():
    conn = sqlite3.connect("questions.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT nomTheme FROM Thematique")
    themes = cursor.fetchall()
    conn.close()
    return [theme[0] for theme in themes]  

def get_difficulties_form():
    conn = sqlite3.connect("questions.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT diff FROM Question")
    difficulties = cursor.fetchall()
    conn.close()
    
    # Mapping des valeurs numériques 
    difficulty_map = {
        0: "0",
        1: "1",
        2: "2",
        3: "3"
    }
    
    # Convertir les valeurs numériques en labels
    return [difficulty_map.get(difficulty[0], "Inconnue") for difficulty in difficulties]
