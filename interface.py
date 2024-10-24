import pygame
import sys
from quiz import main as quiz_main, get_questions_from_db, get_reponse_by_id, get_themes, get_difficulties, get_questions_by_theme, get_questions_by_difficulty
import random
from bonus import curseur, start_timer, is_time_up, draw_timer, add_question_to_db

# Initialiser Pygame
pygame.init()

# Initialiser le module mixer de Pygame
pygame.mixer.init()

# Charger et définir l'icône 
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

# Charger et jouer la musique
pygame.mixer.music.load('musique/menu.mp3')
pygame.mixer.music.play(-1)  # -1 pour jouer en boucle
pygame.mixer.music.set_volume(0.1)

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (200, 200, 200)
LIGHT_GREY = (230, 230, 230)
NEON_COLORS = [(57, 255, 20), (255, 20, 147), (0, 255, 255), (255, 255, 0)]

# Définir les dimensions de l'écran

screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
pygame.display.set_caption("Quiz Game")

# Charger le fond d'écran
background = pygame.image.load('images/fond.jpg')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Définir le curseur 
cursor = curseur('images/curseur.png')

# Définir la police
font = pygame.font.Font(None, 50)

button_font = pygame.font.Font(None, 30)
input_font = pygame.font.Font(None, 48)  # Augmenter la taille de la police pour les réponses

# Fonction pour ajouter du texte
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Fonction pour créer un bouton
def draw_button(text, font, color, rect, surface):
    pygame.draw.rect(surface, color, rect, border_radius=10)
    text_surf = font.render(str(text), True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


def get_user_name():
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 50)
    user_name = ''
    while True:
        screen.blit(background, (0, 0))
        draw_text('Entrez votre pseudo:', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        pygame.draw.rect(screen, LIGHT_GREY, input_box, border_radius=10)
        pygame.draw.rect(screen, BLACK, input_box, 2, border_radius=10)
        text_surface = input_font.render(user_name, True, BLACK)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(300, text_surface.get_width() + 10)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return user_name
                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    user_name += event.unicode
import os
#Fonction permettant de lire le fichier contenant le tableau des scores
def read_leaderboard(file_path='leaderboard.txt'):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    leaderboard = []
    for line in lines:
        name, score = line.strip().split(',')
        leaderboard.append((name, int(score)))
    return leaderboard

#Fonction permettant d'écrire à la suite du tableau des scores
def write_leaderboard(leaderboard, file_path='leaderboard.txt'):
    with open(file_path, 'w') as file:
        for name, score in leaderboard:
            file.write(f'{name},{score}\n')

#Fonction permettant de mettre à jour le tableau des scores
def update_leaderboard(name, score, file_path='leaderboard.txt'):
    leaderboard = read_leaderboard(file_path)
    for i, (existing_name, existing_score) in enumerate(leaderboard):
        if existing_name == name:
            if score > existing_score:
                leaderboard[i] = (name, score)
            break
    else:
        leaderboard.append((name, score))
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    leaderboard = leaderboard[:5]  # Garder seulement les 5 meilleurs scores
    write_leaderboard(leaderboard, file_path)

#Fonction permettant l'affichage du tableau des scores
def draw_leaderboard(surface, font, x, y):
    leaderboard = read_leaderboard()
    draw_text('Leaderboard:', font, BLACK, surface, x, y)
    for i, (name, score) in enumerate(leaderboard):
        draw_text(f'{i+1}. {name}: {score}', font, BLACK, surface, x, y + (i + 1) * 30)

#Fonction permettant d'afficher les boutons du menu
def draw_menu_buttons(screen):
    button_width = 300
    button_height = 100
    button_spacing = 50
    button_1 = pygame.Rect((SCREEN_WIDTH // 2) - button_width - (button_spacing // 2), 400, button_width, button_height)
    button_2 = pygame.Rect((SCREEN_WIDTH // 2) + (button_spacing // 2), 400, button_width, button_height)
    quit_button = pygame.Rect(SCREEN_WIDTH - 350, 150, 200, 50)
    mute_button = pygame.Rect(SCREEN_WIDTH - 350, 50, 200, 50)
    add_question_button = pygame.Rect((SCREEN_WIDTH // 2) - (button_width // 2), 550, button_width, button_height)

    draw_button('Mute', button_font, GREY, mute_button, screen)
    draw_button('Quitter', button_font, RED, quit_button, screen)
    draw_button('Normal Mode', button_font, BLUE, button_1, screen)
    draw_button('Ranked Mode', button_font, RED, button_2, screen)
    draw_button('Ajouter une Question', button_font, BLUE, add_question_button, screen)

    return button_1, button_2, quit_button, mute_button, add_question_button

#Fonction permettant de définir les évenements lors d'un clic sur les boutons du menu principal
def handle_menu_events(buttons, click):
    button_1, button_2, quit_button, mute_button, add_question_button = buttons
    mx, my = pygame.mouse.get_pos()

    if button_1.collidepoint((mx, my)) and click:
        normal_mode()
    if button_2.collidepoint((mx, my)) and click:
        ranked_mode()
    if mute_button.collidepoint((mx, my)) and click:
        if pygame.mixer.music.get_volume() > 0:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(0.1)
    if quit_button.collidepoint((mx, my)) and click:
        pygame.quit()
        sys.exit()
    if add_question_button.collidepoint((mx, my)) and click:
        add_question_screen(screen)

#Definition du menu
def main_menu():
    click = False
    while True:
        screen.blit(background, (0, 0))
        draw_text('Quiz Game', font, BLACK, screen, SCREEN_WIDTH // 2, 100)

        buttons = draw_menu_buttons(screen)
        draw_leaderboard(screen, font, SCREEN_WIDTH // 2, 700)
        cursor.draw(screen)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        handle_menu_events(buttons, click)

        pygame.display.update()


#Definition de l'ecran de fin de jeu
def end_screen(score, serie, ranked=False):
    if ranked:
        user_name = get_user_name()
        update_leaderboard(user_name, score)
    running = True
    while running:
        
        screen.blit(background, (0, 0))
        draw_text(f'Fin du quiz! Votre score final est: {score}, Et votre meilleure série de bonnes réponses est: {serie}', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)

        # Préparer le texte du bouton
        button_text = 'Revenir au menu principal'
        
        # Calculer la largeur du texte pour ajuster la taille du bouton
        text_surf = button_font.render(button_text, True, WHITE)
        button_width = text_surf.get_width() + 40  # Ajouter de l'espace autour du texte
        button_height = 50

        # Créer le bouton et le centrer sur l'écran
        quit_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 100, button_width, button_height)
        
        # Dessiner le bouton "Revenir au menu principal"
        draw_button(button_text, button_font, RED, quit_button, screen)

        # Dessiner le curseur
        cursor.draw(screen)

        # Gestion des événements
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Gérer les clics sur le bouton "Quitter"
        if quit_button.collidepoint(pygame.mouse.get_pos()) and click:
            running = False  # Quitte l'écran de fin et retourne au menu principal

        # Mettre à jour l'affichage
        pygame.display.update()

def normal_mode():
    # Jeu en mode normal
    questions = get_questions_from_db("questions.sqlite")
    themes = get_themes(questions)
    difficulties = get_difficulties(questions)

    selected_theme = None
    selected_difficulty = None

    # Fonction pour choisir un thème ou une difficulté
    def choose_theme_or_difficulty():
        click = False
        while True:
            screen.blit(background, (0, 0))
            
            draw_text('Choisissez un thème ou une difficulté', font, BLACK, screen, SCREEN_WIDTH // 2, 100)

            mx, my = pygame.mouse.get_pos()

            # Afficher les thèmes
            theme_buttons = []
            for i, theme in enumerate(themes):
                button_rect = pygame.Rect(100, 200 + i * 60, 300, 50)
                theme_buttons.append((button_rect, theme))
                draw_button(theme, button_font, BLUE, button_rect, screen)

            # Afficher les difficultés
            difficulty_buttons = []
            for i, difficulty in enumerate(difficulties):
                button_rect = pygame.Rect(SCREEN_WIDTH - 400, 200 + i * 60, 300, 50)
                difficulty_buttons.append((button_rect, difficulty))
                draw_button(difficulty, button_font, RED, button_rect, screen)

            # Dessiner le curseur personnalisé
            cursor.draw(screen)

            click = False
            # Gestions des évènements Quitter et Valider
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            for button_rect, theme in theme_buttons:
                if button_rect.collidepoint(mx, my) and click:
                    return 'theme', theme

            for button_rect, difficulty in difficulty_buttons:
                if button_rect.collidepoint(mx, my) and click:
                    return 'difficulty', difficulty

            pygame.display.update()

    choice_type, choice_value = choose_theme_or_difficulty()

    if choice_type == 'theme':
        filtered_questions = get_questions_by_theme(questions, choice_value)
    else:
        filtered_questions = get_questions_by_difficulty(questions, choice_value)

    # Limiter à 10 questions ou moins si pas assez de questions
    filtered_questions = filtered_questions[:10]

    # Lancer le quiz avec les questions filtrées
    run_quiz(filtered_questions)

def run_quiz(questions):
    current_question_index = 0
    score = 0
    streak = 0  # Initialiser le streak
    best_streak = 0  # Initialiser le meilleur streak
    input_text = ''
    show_choices = False
    displayed_reponses = []
    choice_rects = []  # Initialiser choice_rects ici

    running = True
    while running:

        screen.blit(background, (0, 0))
        
        if current_question_index >= len(questions):
            end_screen(score, best_streak, False)  # Toutes les questions ont été posées, aller à l'écran de fin
            return  # Sort de ranked_mode() une fois l'écran de fin terminé

        # Afficher le score actuel
        draw_text(f'Score: {score}', font, BLACK, screen, SCREEN_WIDTH // 2, 50)
        # Afficher le streak actuel
        draw_text(f'Streak: {streak}', font, BLACK, screen, SCREEN_WIDTH // 2, 100)
        # Afficher le meilleur streak
        draw_text(f'Best Streak: {best_streak}', font, BLACK, screen, SCREEN_WIDTH // 2, 150)

        if current_question_index >= len(questions):
            return  # Sort de run_quiz() une fois l'écran de fin terminé

        current_question = questions[current_question_index]
        draw_text(current_question.question, font, BLACK, screen, SCREEN_WIDTH // 2, 200)

        # Afficher la zone de texte pour la réponse si les choix ne sont pas affichés
        if not show_choices:
            input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 50)
            pygame.draw.rect(screen, LIGHT_GREY, input_box, border_radius=10)
            pygame.draw.rect(screen, BLACK, input_box, 2, border_radius=10)
            text_surface = input_font.render(input_text, True, BLACK)
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
            input_box.w = max(300, text_surface.get_width() + 10)

        # Afficher les boutons
        quit_button = pygame.Rect(100, SCREEN_HEIGHT - 100, 200, 50)
        validate_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
        help_button = pygame.Rect(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 100, 200, 50)

        draw_button('Quitter', button_font, RED, quit_button, screen)
        draw_button('Valider', button_font, BLUE, validate_button, screen)
        draw_button('Aide', button_font, GREY, help_button, screen)

        # Afficher les choix si show_choices est True
        if show_choices:
            choice_rects = []
            for i, choice in enumerate(displayed_reponses):
                choice_text = input_font.render(str(choice.reponse), True, BLACK)
                choice_width = max(300, choice_text.get_width() + 40)  # Ajuster la largeur de la case en fonction du texte
                choice_rect = pygame.Rect(SCREEN_WIDTH // 2 - choice_width // 2, 400 + i * 100, choice_width, 80)
                pygame.draw.rect(screen, LIGHT_GREY, choice_rect, border_radius=10)
                pygame.draw.rect(screen, NEON_COLORS[i % len(NEON_COLORS)], choice_rect, 4, border_radius=10)
                screen.blit(choice_text, (choice_rect.x + (choice_rect.width - choice_text.get_width()) // 2, choice_rect.y + (choice_rect.height - choice_text.get_height()) // 2))
                choice_rects.append((choice_rect, choice))

        click = False
        # Gestions des évènements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    # Gestion du bouton quitter
                    if quit_button.collidepoint(event.pos):
                        running = False
                        # Gestion du bouton valider
                    if validate_button.collidepoint(event.pos):
                        correct_reponse = get_reponse_by_id(current_question, current_question.idBonneRep)
                        input_text = str(input_text)
                        correct_reponse.reponse = str(correct_reponse.reponse)
                        if input_text.lower() == correct_reponse.reponse.lower():
                            score += 1*streak
                            streak += 1  # Incrémenter le streak
                            if streak > best_streak:
                                best_streak = streak  # Mettre à jour le meilleur streak
                        else:
                            score -= 1
                            streak = 0  # Réinitialiser le streak en cas de mauvaise réponse
                        if score < 0:
                            score = 0
                        current_question_index += 1
                        input_text = ''
                        show_choices = False
                        displayed_reponses = []
                    # Gestion du bouton aide
                    if help_button.collidepoint(event.pos):
                        if not show_choices:
                            reponses = current_question.reponses
                            random.shuffle(reponses)
                            correct_reponse = get_reponse_by_id(current_question, current_question.idBonneRep)
                            reponses = reponses[:4]
                            if correct_reponse not in reponses:
                                reponses[0] = correct_reponse
                            random.shuffle(reponses)
                            displayed_reponses = reponses
                            show_choices = True
                    for choice_rect, choice in choice_rects:
                        if choice_rect.collidepoint(event.pos):
                            correct_reponse = get_reponse_by_id(current_question, current_question.idBonneRep)
                            if choice == correct_reponse:
                                streak += 1
                                score += 25*streak
                                if streak > streakBest:
                                    streakBest = streak
                            else:
                                streak = 0
                            current_question_index += 1
                            input_text = ''
                            show_choices = False
                            displayed_reponses = []
                            break
            if event.type == pygame.KEYDOWN and not show_choices:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode


        # Dessiner le curseur personnalisé
        cursor.draw(screen)

        pygame.display.update()


# Fonction lançant la version Ranked du quiz
def ranked_mode():
    questions = get_questions_from_db("questions.sqlite")
    random.shuffle(questions)
    current_question_index = 0
    score = 0
    streak = 0
    streakBest = 0
    input_text = ''
    show_choices = False
    displayed_reponses = []
    choice_rects = []

    # Démarrage du chronomètre pour chaque question (10 secondes, commence à 9s et se termine à 0s)
    start_time, duration = start_timer(10)

    running = True

    while running:
        screen.blit(background, (0, 0))
        
        draw_text(f'Score: {score}', font, BLACK, screen, SCREEN_WIDTH // 4, 50)
        draw_text(f'Meilleure série: {streakBest}', font, BLACK, screen, SCREEN_WIDTH // 4, 100)

        if current_question_index >= len(questions):
            end_screen(score, streakBest, True)  # Toutes les questions ont été posées, aller à l'écran de fin
            return  # Sort de ranked_mode() une fois l'écran de fin terminé

        current_question = questions[current_question_index]
        draw_text(current_question.question, font, BLACK, screen, SCREEN_WIDTH // 2, 200)

        # Affichage du chronomètre à l'écran
        draw_timer(screen, font, start_time, duration, SCREEN_WIDTH // 2, 50)

        # Si le temps est écoulé, on passe à la question suivante
        if is_time_up(start_time, duration):
            current_question_index += 1
            start_time, duration = start_timer(10) # Chronomètre réinitialisé
            input_text = ''
            show_choices = False
            displayed_reponses = []
        # Afficher la zone de texte pour la réponse si les choix ne sont pas affichés
        if not show_choices:
            input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 50)
            pygame.draw.rect(screen, LIGHT_GREY, input_box, border_radius=10)
            pygame.draw.rect(screen, BLACK, input_box, 2, border_radius=10)
            text_surface = input_font.render(input_text, True, BLACK)
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
            input_box.w = max(300, text_surface.get_width() + 10)

        quit_button = pygame.Rect(100, SCREEN_HEIGHT - 100, 200, 50)
        validate_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50)
        help_button = pygame.Rect(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 100, 200, 50)

        draw_button('Quitter', button_font, RED, quit_button, screen)
        draw_button('Valider', button_font, BLUE, validate_button, screen)
        draw_button('Aide', button_font, GREY, help_button, screen)

        # Afficher les choix si show_choices est True
        if show_choices:
            choice_rects = []
            for i, choice in enumerate(displayed_reponses):
                choice_text = input_font.render(str(choice.reponse), True, BLACK)
                choice_width = max(300, choice_text.get_width() + 40)
                choice_rect = pygame.Rect(SCREEN_WIDTH // 2 - choice_width // 2, 400 + i * 100, choice_width, 80)
                pygame.draw.rect(screen, LIGHT_GREY, choice_rect, border_radius=10)
                pygame.draw.rect(screen, NEON_COLORS[i % len(NEON_COLORS)], choice_rect, 4, border_radius=10)
                screen.blit(choice_text, (choice_rect.x + (choice_rect.width - choice_text.get_width()) // 2, choice_rect.y + (choice_rect.height - choice_text.get_height()) // 2))
                choice_rects.append((choice_rect, choice))

        cursor.draw(screen)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    # Gestion du bouton quitter
                    if quit_button.collidepoint(event.pos):
                        running = False
                    # Gestion du bouton valider
                    if validate_button.collidepoint(event.pos):
                        correct_reponse = get_reponse_by_id(current_question, current_question.idBonneRep)
                        correct_reponse.reponse = str(correct_reponse.reponse)
                        input_text = str(input_text)
                        
                        if input_text.lower() == correct_reponse.reponse.lower():
                            streak += 1
                            score += 50*streak
                            if streak > streakBest:
                                streakBest = streak
                        else:
                            streak = 0
                        current_question_index += 1
                        input_text = ''
                        show_choices = False
                        displayed_reponses = []
                        start_time, duration = start_timer(10)  # Redémarrer le chronomètre
                    # Gestion du boutton d'aide

                    if help_button.collidepoint(event.pos):
                        if not show_choices:
                            reponses = current_question.reponses
                            random.shuffle(reponses)
                            correct_reponse = get_reponse_by_id(current_question, current_question.idBonneRep)
                            reponses = reponses[:4]
                            if correct_reponse not in reponses:
                                reponses[0] = correct_reponse
                            random.shuffle(reponses)
                            displayed_reponses = reponses
                            show_choices = True
                    for choice_rect, choice in choice_rects:
                        if choice_rect.collidepoint(event.pos):
                            correct_reponse = get_reponse_by_id(current_question, current_question.idBonneRep)
                            if choice == correct_reponse:
                                streak += 1
                                score += 25*streak
                                if streak > streakBest:
                                    streakBest = streak
                            else:
                                streak = 0
                            current_question_index += 1
                            input_text = ''
                            show_choices = False
                            displayed_reponses = []
                            start_time, duration = start_timer(10)  
            if event.type == pygame.KEYDOWN and not show_choices:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        pygame.display.update()
# Fonction permettant au joueur d'ajouter des questions à la base de données
def add_question_screen(screen):
    input_text_question = ''
    input_text_reponses = ['', '', '', '']  # 4 champs de réponse
    current_input_index = 0  # 0 pour question, 1-4 pour les réponses
    theme_selected = None
    difficulty_selected = None
    error_message = ""  # Message d'erreur si le formulaire est incomplet

    themes = get_themes()  # Obtention des thèmes
    difficulties = get_difficulties()  # Obtention des difficultés
    cursor.draw(screen)
    
    running = True
    while running:
        screen.blit(background, (0, 0))
        draw_text('Ajouter une question', font, BLACK, screen, SCREEN_WIDTH // 2, 100)
        # Affichage du champ de saisie pour la question
        draw_text("Question:", font, BLACK, screen, SCREEN_WIDTH // 4, 200)
        input_box_question = pygame.Rect(SCREEN_WIDTH // 2 - 150, 200, 300, 50)
        pygame.draw.rect(screen, LIGHT_GREY, input_box_question, border_radius=10)
        pygame.draw.rect(screen, BLACK, input_box_question, 2, border_radius=10)
        text_surface_question = input_font.render(input_text_question, True, BLACK)
        screen.blit(text_surface_question, (input_box_question.x + 5, input_box_question.y + 5))
        input_box_question.w = max(300, text_surface_question.get_width() + 10)

        # Affichage des champs de réponse
        input_boxes_reponses = []
        for i in range(4):
            draw_text(f"Réponse {i+1}:", font, BLACK, screen, SCREEN_WIDTH // 4, 300 + i * 70)
            input_box_reponse = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300 + i * 70, 300, 50)
            input_boxes_reponses.append(input_box_reponse)  # Sauvegarder chaque boîte de réponse
            pygame.draw.rect(screen, LIGHT_GREY, input_box_reponse, border_radius=10)
            pygame.draw.rect(screen, BLACK, input_box_reponse, 2, border_radius=10)
            text_surface_reponse = input_font.render(input_text_reponses[i], True, BLACK)
            screen.blit(text_surface_reponse, (input_box_reponse.x + 5, input_box_reponse.y + 5))

        # Afficher la sélection du thème
        draw_text("Thème:", font, BLACK, screen, SCREEN_WIDTH // 4, 600)
        theme_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 600, 300, 50)
        pygame.draw.rect(screen, LIGHT_GREY, theme_box, border_radius=10)
        theme_text = input_font.render(theme_selected if theme_selected else "Choisir thème", True, BLACK)
        screen.blit(theme_text, (theme_box.x + 5, theme_box.y + 5))

        # Affichage de la sélection de la difficulté
        draw_text("Difficulté:", font, BLACK, screen, SCREEN_WIDTH // 4, 700)
        difficulty_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 700, 300, 50)
        pygame.draw.rect(screen, LIGHT_GREY, difficulty_box, border_radius=10)
        difficulty_text = input_font.render(difficulty_selected if difficulty_selected else "Choisir difficulté", True, BLACK)
        screen.blit(difficulty_text, (difficulty_box.x + 5, difficulty_box.y + 5))

        # Boutons
        validate_button = pygame.Rect(SCREEN_WIDTH // 5 - 100, 800, 200, 50)
        draw_button("Valider", button_font, BLUE, validate_button, screen)
        quit_button = pygame.Rect(SCREEN_WIDTH // 15 - 100, 800, 200, 50)
        draw_button("Quitter", button_font, RED, quit_button, screen)

        # Affichage du message d'erreur 
        if error_message:
            draw_text(error_message, font, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

        cursor.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if validate_button.collidepoint(event.pos):
                    # Vérification des champs
                    if not input_text_question:
                        error_message = "Le champ de la question est vide !"
                    elif '' in input_text_reponses:
                        error_message = "Tous les champs de réponse doivent être remplis !"
                    elif not theme_selected:
                        error_message = "Veuillez sélectionner un thème !"
                    elif not difficulty_selected:
                        error_message = "Veuillez sélectionner une difficulté !"
                    else:
                        # Soumettre la question à la BDD (si tout est rempli)
                        error_message = ""
                        add_question_to_db(input_text_question, input_text_reponses, theme_selected, difficulty_selected)
                        print("Question soumise avec succès!")
                        running = False
                # Bouton Quitter que permet de revenir en arrière dans le jeu
                if quit_button.collidepoint(event.pos):
                     return
                if theme_box.collidepoint(event.pos):
                    # Sélection d'un thème
                    theme_selected = themes[0]  

                if difficulty_box.collidepoint(event.pos):
                    # Sélection d'une difficulté
                    difficulty_selected = difficulties[0]  

                # Sélection de la zone de texte (question ou réponse)
                if input_box_question.collidepoint(event.pos):
                    current_input_index = 0  # Focaliser sur la question

                # Vérification de chaque zone de réponse
                for i, input_box_reponse in enumerate(input_boxes_reponses):
                    if input_box_reponse.collidepoint(event.pos):
                        current_input_index = i + 1  # Focaliser sur la réponse correspondante

            if event.type == pygame.KEYDOWN:
                # La question
                if current_input_index == 0:  # Champ de question sélectionné
                    if event.key == pygame.K_BACKSPACE:
                        input_text_question = input_text_question[:-1]
                    else:
                        input_text_question += event.unicode

                # Les réponses
                elif 1 <= current_input_index <= 4:  # Champ de réponse sélectionné
                    index_reponse = current_input_index - 1
                    if event.key == pygame.K_BACKSPACE:
                        input_text_reponses[index_reponse] = input_text_reponses[index_reponse][:-1]
                    else:
                        input_text_reponses[index_reponse] += event.unicode


if __name__ == "__main__":
    main_menu()

