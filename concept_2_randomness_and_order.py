import os, sys,  math
import pygame, pygame.mixer
import random
from pygame.locals import *

# Defining some basic colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

colors = [black, red, green, blue]

# Defining the screen size
screen_size = screen_width, screen_height = 600, 400

class MyCircle:
    def __init__(self, (x, y), size, color = (255,255,255), width = 1):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.width = width

    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.width)


# Setting the display and getting the Surface object
screen = pygame.display.set_mode(screen_size)
# Getting the Clock object
clock = pygame.time.Clock()
# Setting a title to the window

pygame.display.set_caption('Concept 2 - Randomness and Order')

number_of_circles = 10
my_circles = []

for n in range(number_of_circles):
    size = random.randint(10, 20)
    x = random.randint(size, screen_width-size)
    y = random.randint(size, screen_height-size)
    color = random.choice(colors)
    my_circles.append(MyCircle((x, y), size, color))


# Defining variables for fps and continued running
fps_limit = 60
run_me = True
while run_me:

    # Get any user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_me = False

    # Limit the framerate
    clock.tick(fps_limit)

    # Clear the screen
    screen.lock()
    screen.fill(white)
    for my_circle in my_circles:
        my_circle.display()

    screen.unlock()
    # Display everything in the screen.
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
