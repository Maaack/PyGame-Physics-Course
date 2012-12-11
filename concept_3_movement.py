import os, sys,  math
import pygame, pygame.mixer
import random
import euclid # From http://code.google.com/p/pyeuclid/
from pygame.locals import *

# Defining some basic colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

colors = [black, red, green, blue]

initial_velocity = 20

# Defining the screen size
screen_size = screen_width, screen_height = 600, 400

class MyCircle:
    def __init__(self, position, size, color = (255,255,255), velocity = euclid.Vector2(0,0), width = 1):
        self.position = position
        self.size = size
        self.color = color
        self.width = width
        self.velocity = velocity

    def display(self):
        rx, ry = int(self.position.x), int(self.position.y)
        pygame.draw.circle(screen, self.color, (rx, ry), self.size, self.width)

    def move(self):
        self.position += self.velocity * dtime

    def change_velocity(self, velocity):
        self.velocity = velocity

def get_random_velocity():
    new_angle = random.uniform(0, math.pi*2)
    new_x = math.sin(new_angle)
    new_y = math.cos(new_angle)
    new_vector = euclid.Vector2(new_x, new_y)
    new_vector.normalize()
    new_vector *= initial_velocity # pixels per second
    return new_vector


# Setting the display and getting the Surface object
screen = pygame.display.set_mode(screen_size)
# Getting the Clock object
clock = pygame.time.Clock()
# Setting a title to the window
pygame.display.set_caption('Vectors and Motion!')

number_of_circles = 10
my_circles = []

for n in range(number_of_circles):
    size = random.randint(10, 20)
    x = random.randint(size, screen_width-size)
    y = random.randint(size, screen_height-size)
    color = random.choice(colors)
    velocity = get_random_velocity()
    my_circle = MyCircle(euclid.Vector2(x, y), size, color, velocity)
    my_circles.append(my_circle)

direction_tick = 0.0

# Defining variables for fps and continued running
fps_limit = 60
run_me = True
while run_me:

    # Get any user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_me = False

    # Limit the framerate
    dtime_ms = clock.tick(fps_limit)
    dtime = dtime_ms/1000.0

    # Make a random circle change direction every second
    direction_tick += dtime
    if (direction_tick > 1.0):
        direction_tick = 0.0
        random_circle = random.choice(my_circles)
        new_velocity = get_random_velocity()
        random_circle.change_velocity(new_velocity)

    # Clear the screen
    screen.lock()
    screen.fill(white)

    for my_circle in my_circles:
        my_circle.move()
        my_circle.display()

    screen.unlock()
    # Display everything in the screen.
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
