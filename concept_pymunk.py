import os
import sys
import math
import pygame, pygame.mixer
import random
import pymunk
from pygame.locals import *

# Defining some basic colors
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0
cyan = 0, 255, 255
magenta = 255, 0, 255

colors = [black, red, green, blue, yellow, cyan, magenta]

# Gravity vector
space = pymunk.Space()
space.gravity = (0.0, 300.0)

# Defining the screen size
screen_size = screen_width, screen_height = 600, 400

class MyWall:

    def __init__(self, a = (0,0), b = screen_size, radius = 0 ):
        self.a = a
        self.b = b
        self.radius = radius
        self.body = pymunk.Body()
        self.shape = pymunk.Segment(self.body, a, b, radius)
        self.shape.friction = 100.0
        self.shape.collision_type = 0
        self.shape.elasticity = 0.9
        space.add(self.shape)

    def display(self):
        pygame.draw.line(screen, black, self.a, self.b, 6)


class MyCircle:
    def __init__(self, position, size, color = (255,255,255), width = 0):
        self.position = position
        self.size = size
        self.color = color
        self.width = width
        self.surface_area = 4 * math.pi * (self.size ** 2)
        self.mass = self.surface_area / 10
        self.inertia = pymunk.moment_for_circle(self.mass, 0, self.size)  # 1
        self.body = pymunk.Body(self.mass, self.inertia)  # 2
        self.body.position = position # 3
        self.shape = pymunk.Circle(self.body, self.size )  # 4
        self.shape.friction = 900.0
        self.shape.elasticity = 0.9
        space.add(self.body, self.shape)  # 5

    def display(self):
        p = x1, y1 = int(self.body.position.x), int(self.body.position.y)
        x2 = math.cos(self.body.angle)*self.size + x1
        y2 = math.sin(self.body.angle)*self.size + y1
        pygame.draw.circle(screen, self.color, p, self.size, self.width)
        pygame.draw.line(screen, white, p, (x2,y2), 2)


    def apply_force(self, vector = (0,0), offset  = (0,0)):
        vector.normalize_return_length()
        self.body.apply_force(vector, offset)


class MyHex:
    def __init__(self, position, size, color = (255,255,255)):
        self.size = size
        self.color = color
        self.surface_area = 4 * math.pi * (self.size ** 2)
        self.mass = self.surface_area / 10
        self.points = get_hex_points((0,0), size, 0)
        self.inertia = pymunk.moment_for_poly(self.mass, self.points)  # 1
        self.body = pymunk.Body(self.mass, self.inertia)  # 2
        self.body.position = position
        self.body.angle = 0
        self.shape = pymunk.Poly(self.body, self.points)  # 4
        self.shape.friction = 900.0
        self.shape.elasticity = 0.9
        space.add(self.body, self.shape)  # 5

    def display(self):
        points = self.get_points()
        pygame.draw.polygon(screen, self.color, points, 0)


    def get_points(self):
        shape_points = self.shape.get_points()
        points = range(6)
        for i , (x, y) in enumerate(shape_points):
            points[i] = int(x), int(y)
        self.points = points
        return self.points

    def apply_force(self, vector = (0,0), offset  = (0,0)):
        vector.normalize_return_length()
        self.body.apply_force(vector, offset)


def get_hex_points(position, size, angle):
        sides = 6
        x0, y0 = position
        points = range(1,sides+1)
        for i, value in enumerate(points):
             new_angle = (2 * math.pi * value / sides) + angle
             x = math.cos(new_angle) * size + x0
             y = math.sin(new_angle) * size + y0
             points[i] = x, y
        return points

# Setting the display and getting the Surface object
screen = pygame.display.set_mode(screen_size)
# Getting the Clock object
clock = pygame.time.Clock()
# Setting a title to the window

pygame.display.set_caption('Pymunk Implementation')

number_of_circles = 3
number_of_hexes = 400
my_circles = []

my_borders = [[(0,0), (0, screen_height)],
[(0, screen_height), (screen_width, screen_height)],
[(screen_width, screen_height), (screen_width, 0)],
[(screen_width, 0), (0,0)]]
my_walls = []


for n in range(number_of_circles):
    size = random.randint(10, 20)
    x = random.randint(size, screen_width-size)
    y = random.randint(size, screen_height-size)
    color = random.choice(colors)
    my_circle = MyCircle((x, y), size, color)
    my_circles.append(my_circle)

for n in range(number_of_hexes):
    size = 8
    x = random.randint(size, screen_width-size)
    y = random.randint(size, screen_height-size)
    color = random.choice(colors)
    my_circle = MyHex((x, y), size, color)
    my_circles.append(my_circle)


for border in my_borders:
    a, b = border
    my_wall = MyWall(a, b)
    my_walls.append(my_wall)


# Defining variables for fps and continued running
fps_limit = 60.0
run_me = True
while run_me:
    # Limit the framerate
    dtime_ms = clock.tick(fps_limit)
    dtime = dtime_ms/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_me = False

    screen.lock()
    # Clear the screen
    screen.fill(white)

    space.step(1/fps_limit)

    for my_circle in my_circles:
        my_circle.display()

    for my_wall in my_walls:
        my_wall.display()

    screen.unlock()
    # Display everything in the screen.
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
