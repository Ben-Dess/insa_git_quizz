# Example file showing a circle moving on screen
import pygame
import gestion_questions
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

questions = gestion_questions.get_questions()
reponses = questions[0].getanswers()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    background = pygame.Color("#efe7d9")
    screen.fill(background)
    font = pygame.font.Font('freesansbold.ttf', 32)
    # create a rectangular object for the
    # text surface object

    text = font.render(questions[0].question, True, "black")
    textRect = text.get_rect()
    textRect.center = (600, 200)
    screen.blit(text, textRect)
    offset= 0
    for reponse in reponses :
        text = font.render(reponse['response'], True, "black")
        textRect = text.get_rect()
        textRect.center = (400 , 400+offset)
        offset+=100
        screen.blit(text, textRect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()