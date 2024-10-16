# Example file showing a circle moving on screen

import pygame
import pygame_widgets
from pygame_widgets.button import Button
import gestion_questions
# pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
dt = 0

questions = gestion_questions.get_questions()
answers = questions[0].getanswers()


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
    buttons = []

    for answer in answers :
        size = len(answer['response'])
        buttons.append(Button(
            # Mandatory Parameters
            screen,  # Surface to place button on
            400,  # X-coordinate of top left corner
            300+ offset,  # Y-coordinate of top left corner
            size*40,  # Width
            50,  # Height

            # Optional Parameters
            text=answer['response'],  # Text to display
            textColour= 'white',
            fontSize=40,  # Size of font
            margin=20,  # Minimum distance between text/image and edge of button
            inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
            hoverColour=(150, 0, 0),  # Colour of button when being hovered over
            pressedColour=(0, 200, 20),  # Colour of button when being clicked
            radius=20,  # Radius of border corners (leave empty for not curved)
            onClick=lambda: print('Click')  # Function to call when clicked on
        ))
        offset+=100
    # flip() the display to put your work on screen

    buttonQuit = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        900,  # X-coordinate of top left corner
        700,  # Y-coordinate of top left corner
        size * 40,  # Width
        50,  # Height

        # Optional Parameters
        text="EXIT",  # Text to display
        textColour='white',
        fontSize=40,  # Size of font
        margin=20,  # Minimum distance between text/image and edge of button
        inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
        hoverColour=(150, 0, 0),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20),  # Colour of button when being clicked
        radius=20,  # Radius of border corners (leave empty for not curved)
        onClick=lambda: pygame.quit()  # Function to call when clicked on
    )
    events = pygame.event.get()
    pygame_widgets.update(events)
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()