# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0


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
    text = font.render('QUESTION', True, "black")
    textRect = text.get_rect()
    textRect.center = (400, 400// 2)
    screen.blit(text, textRect)
    text = font.render('REPONSES', True, "black")
    textRect = text.get_rect()
    textRect.center = (400 , 400)
    screen.blit(text, textRect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()