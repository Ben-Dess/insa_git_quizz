import pygame
import pygame_widgets
from pygame_widgets.button import ButtonArray
from pygame_widgets.button import Button
import quiz
import random

# Initialisation de Pygame
pygame.init()
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Bouton de sortie
size = len("EXIT")
buttonQuit = Button(
    screen,
    infoObject.current_w - (size * 40) - 10,
    infoObject.current_h - 70,
    size * 40,
    50,
    text="EXIT",
    textColour='white',
    fontSize=40,
    margin=20,
    inactiveColour=(200, 50, 0),
    hoverColour=(150, 0, 0),
    pressedColour=(0, 200, 20),
    radius=20,
    onClick=lambda: pygame.quit()
)

# Variable pour garder une trace de l'état de la question
current_question_index = 0

def answer_check(correct_response, responseText):
    return str(correct_response.reponse) == responseText

def create_question(correct_response, reponses):
    global buttonArray
    buttonArray = ButtonArray(
        screen,
        infoObject.current_w / 3,
        infoObject.current_h / 2,
        500,
        200,
        (2, 2),
        border=20,
        texts=[str(r.reponse) for r in reponses],
        colour=pygame.Color("#efe7d9"),
        onClicks=[
            lambda response=r.reponse: handle_answer(correct_response, response) for r in reponses
        ]
    )

def handle_answer(correct_response, response):
    global current_question_index
    if answer_check(correct_response, response):
        print("Bonne réponse")
    else:
        print("Mauvaise réponse")
    # Passe à la question suivante
    current_question_index += 1

def game():
    global current_question_index
    questions = quiz.get_questions_from_db("questions.sqlite")
    random.shuffle(questions)
    questions = questions[:10]

    while current_question_index < len(questions):
        question = questions[current_question_index]
        answers = question.reponses
        correct_response = quiz.get_reponse_by_id(question, question.idBonneRep)
        reponses = answers[:4]

        if correct_response not in reponses:
            reponses[0] = correct_response
        random.shuffle(reponses)

        background = pygame.Color("#efe7d9")
        font = pygame.font.Font('freesansbold.ttf', 32)

        # Affiche la question
        text = font.render(question.question, True, "black")
        textRect = text.get_rect(center=(infoObject.current_w / 2, 200))
        screen.fill(background)
        screen.blit(text, textRect)

        # Crée les boutons
        create_question(correct_response, reponses)

        # Boucle d'événements
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame_widgets.update(pygame.event.get())
            buttonQuit.draw()
            if buttonArray:
                buttonArray.draw()
            pygame.display.flip()

            # Vérifier si une réponse a été traitée
            if current_question_index > len(questions) - 1:
                break  # Sortir de la boucle principale si toutes les questions ont été traitées

# Lancer le jeu
game()
pygame.quit()
