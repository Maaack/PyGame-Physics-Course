import os, sys, math, pygame, pygame.mixer
from pygame.locals import *

# Defining some basic colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

# Defining the screen size
screen_size = screen_width, screen_height = 600, 400

# Setting the display and getting the Surface object
screen = pygame.display.set_mode(screen_size)
# Getting the Clock object
clock = pygame.time.Clock()
# Setting a title to the window
pygame.display.set_caption('Your Game Title!')

# Defining variables for fps and continued running
fps_limit = 60
run_me = True
while run_me:
    # Limit the framerate
    clock.tick(fps_limit)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_me = False

    # Clear the screen
    screen.fill(white)

    # Display everything in the screen.
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
