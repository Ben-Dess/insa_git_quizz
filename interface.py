import pygame
import sys
from quiz import main as quiz_main, get_questions_from_db, get_reponse_by_id
import random
from bonus import curseur
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
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quiz Game")

# Charger le fond d'écran
background = pygame.image.load('images/fond.jpg')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Définir le curseur 
cursor = curseur('images/curseur.png')

# Définir la police
font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 50)
input_font = pygame.font.Font(None, 48)  # Augmenter la taille de la police pour les réponses

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def draw_button(text, font, color, rect, surface):
    pygame.draw.rect(surface, color, rect, border_radius=10)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def main_menu():
    click = False
    while True:
        screen.blit(background, (0, 0))
        
        # Centrer le titre
        draw_text('Quiz Game', font, BLACK, screen, SCREEN_WIDTH // 2, 100)
        
        mx, my = pygame.mouse.get_pos()

        # Placer les boutons côte à côte
        button_width = 300
        button_height = 100
        button_spacing = 50
        button_1 = pygame.Rect((SCREEN_WIDTH // 2) - button_width - (button_spacing // 2), 400, button_width, button_height)
        button_2 = pygame.Rect((SCREEN_WIDTH // 2) + (button_spacing // 2), 400, button_width, button_height)

        if button_1.collidepoint((mx, my)):
            if click:
                normal_mode()
        if button_2.collidepoint((mx, my)):
            if click:
                ranked_mode()

        draw_button('Normal Mode', button_font, BLUE, button_1, screen)
        draw_button('Ranked Mode', button_font, RED, button_2, screen)

        draw_text('Scoreboard (on verra plus tard)', button_font, GREY, screen, SCREEN_WIDTH // 2, 600)
        cursor.draw(screen)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def end_screen(score, serie):
    running = True
    while running:
        screen.blit(background, (0, 0))
        draw_text(f'Fin du quiz!\nVotre score final est: {score},\nEt votre meilleure série de bonnes réponses est: {serie}', font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)

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
    # Lancer le quiz en mode normal
    quiz_main()

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
    running = True

    while running:
        screen.blit(background, (0, 0))
        
        draw_text(f'Score: {score}', font, BLACK, screen, SCREEN_WIDTH // 2, 50)

        if current_question_index >= len(questions):
            end_screen(score, streakBest)  # Toutes les questions ont été posées, aller à l'écran de fin
            return  # Sort de ranked_mode() une fois l'écran de fin terminé

        current_question = questions[current_question_index]
        draw_text(current_question.question, font, BLACK, screen, SCREEN_WIDTH // 2, 200)

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
                    if quit_button.collidepoint(event.pos):
                        running = False
                    if validate_button.collidepoint(event.pos):
                        correct_reponse = get_reponse_by_id(current_question, current_question.idBonneRep)
                        if input_text == correct_reponse.reponse:
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

        pygame.display.update()


if __name__ == "__main__":
    main_menu()