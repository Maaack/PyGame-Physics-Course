import os, sys,  math
import pygame, pygame.mixer
from pygame.locals import *

# Defining some basic colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

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

pygame.display.set_caption('Concept 1 - First Object')

my_circle = MyCircle((100, 100), 10, red)
my_circle_2 = MyCircle((200,200), 30, blue)
my_circle_3 = MyCircle((300,150), 40, green, 4)
my_circle_4 = MyCircle((450,250), 120, black, 0)

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
    screen.fill(white)

    my_circle.display()
    my_circle_2.display()
    my_circle_3.display()
    my_circle_4.display()

    # Display everything in the screen.
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
