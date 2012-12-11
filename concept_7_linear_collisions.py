import os, sys,  math
import pygame, pygame.mixer
import random
import euclid # From http://code.google.com/p/pyeuclid/
import pymunk
from pygame.locals import *

pymunk.Space()

# Defining some basic colors
black = 0, 0, 0
white = 255, 255, 255
red = 255,  0,  0
green = 0,  255,  0
blue = 0,  0 , 255

colors = [black, red, green, blue]

# Gravity vector
gravity = euclid.Vector2(0.0, 40.0)

# Defining the screen size
screen_size = screen_width, screen_height = 600, 400

class MyCircle:
    def __init__(self, (x, y), size, color = (255,255,255), width = 1, vector = euclid.Vector2(0,0), accel = euclid.Vector2(0,0)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.width = width
        self.vector = vector
        self.accel = accel


    def display(self):
        rx, ry = int(self.x), int(self.y)
        pygame.draw.circle(screen, self.color, (rx, ry), self.size, self.width)


    def vector_and_accel(self, time):
        vector = self.vector + self.accel * time
        return vector

    def position_and_vector(self, time):
        x = self.x + (self.vector.x * time) + 0.5*(self.accel.x * (time ** 2))
        y = self.y + (self.vector.y * time) + 0.5*(self.accel.y * (time ** 2))
        return x, y

    # Equation for distance between surfaces.
    # d(t) = |A(t) - B(t)| - (Ra + Rb)
    def surface_distance(self, other, time):
        sum_of_radii = self.size + other.size
        self_vector = self.position_and_vector(time)
        other_vector = other.position_and_vector(time)
        distance_between = abs(self_vector - other_vector)
        return distance_between - sum_of_radii

    def time_of_closest_approach(self, other):
        # Going to be finding time
        time = 0

        # Setting up velocity and position vectors for given time
        radiiAB = self.size + other.size
        positionAB = euclid.Vector2(self.x, self.y) - euclid.Vector2(other.x, other.y)
        velocityAB = self.vector - other.vector

        # d(t) = |A(t) - B(t)| - (Ra + Rb)
        # 0 = math.sqrt(A(t) - B(t))**2 - (Ra + Rb)
        # (Ra + Rb)**2 = (A(t) - B(t))**2
        # (Ra + Rb)**2 = ( ( Pa + Va(t) ) - ( Pb + Vb(t) ) )**2
        #   Pab = Pa - Pb   Vab = Va - Vb
        # (Ra + Rb)**2 = ( Pab + Vab(t) )**2
        # 0 = ( Pab + Vab(t) )**2 - (Ra + Rb)**2
        # 0 = ( Pab + Vab(t) )*( Pab + Vab(t) ) - (Ra + Rb)**2
        # 0 = t**2(Vab * Vab) + 2t(Pab * Vab) + (Pab * Pab) - (Ra + Rb)**2
        # Quadratic formula
        # t = ( -b +- math.sqrt(b**2 - 4ac) ) / 2a
        # Making quadratic variables a, b, c
        # a = Vab * Vab
        # b = 2(Pab * Vab)
        # c = (Pab * Pab) - (Ra + Rb)**2
        # http://twobitcoder.blogspot.com/2010/04/circle-collision-detection.html
        a = velocityAB.dot(velocityAB)
        b = 2 * positionAB.dot(velocityAB)
        c = positionAB.dot(positionAB) - (radiiAB**2)

        # The quadratic discriminant.
        discriminant = b * b - 4 * a * c

        # Case 1:
        # If the discriminant is negative, then there are no real roots, so there is no collision.
        # The time of closest approach is given by the average of the imaginary roots, which is:  t = -b / 2a
        if (discriminant < 0):
            time = -b / (2 * a)
            collision = false
        else:
            # Case 2 and 3:
            # If the discriminant is zero, then there is exactly one real root, meaning that the circles just grazed each other.
            # If the discriminant is positive, then there are two real roots, meaning that the circles penetrate each other.
            # In that case, the smallest of the two roots is the initial time of impact.  We handle these two cases identically.
            time0 = (-b + math.sqrt(float(discriminant))) / (2 * a)
            time1 = (-b - math.sqrt(float(discriminant))) / (2 * a)
            time = math.min(time0, time1)

            # We also have to check if the time to impact is negative.  If it is negative, then that means that the collision
            # occured in the past.
            if (time < 0):
                collision = false
            else:
                collision = true

        # Finally, if the time is negative, then set it to zero, because, again, we want this function to respond only to future events.
        if (time < 0):
            time = 0
        return time, collision

    def move(self):
        self.x, self.y = self.position_and_vector(dtime)
        self.vector = self.vector_and_accel(dtime)
        self.bounce()
        return x, y

    def bounce(self):
        if self.x >= screen_width - self.size:
            self.x = 2*(screen_width - self.size) - self.x
            self.vector = self.vector.reflect(euclid.Vector2(1,0))

        elif self.x <= self.size:
            self.x = 2*self.size - self.x
            self.vector = self.vector.reflect(euclid.Vector2(1,0))

        if self.y >= screen_height - self.size:
            self.y = 2*(screen_height - self.size) - self.y
            self.vector = self.vector.reflect(euclid.Vector2(0,1))

        elif self.y <= self.size:
            self.y = 2*self.size - self.y
            self.vector = self.vector.reflect(euclid.Vector2(0,1))

    # Just for debugging
    def __str__(self):
        return "( " + str(self.x) + ", " + str(self.y) + " ), " + str(self.size) + ", ( " + str(self.vector.x) + ", " + str(self.vector.y) + " ) "

    def update_vector(self, vector):
        self.vector = vector



# Setting the display and getting the Surface object
screen = pygame.display.set_mode(screen_size)
# Getting the Clock object
clock = pygame.time.Clock()
# Setting a title to the window

pygame.display.set_caption('Concept 7 - Predicting Linear Collisions')

number_of_circles = 10
my_circles = []

def apply_random_vector(circle):
    new_angle = random.uniform(0, math.pi*2)
    new_x = math.sin(new_angle)
    new_y = math.cos(new_angle)
    new_vector = euclid.Vector2(new_x, new_y)
    new_vector.normalize()
    new_vector *= 60 # pixels per second
    circle.update_vector(new_vector)

for n in range(number_of_circles):
    size = random.randint(10, 20)
    x = random.randint(size, screen_width-size)
    y = random.randint(size, screen_height-size)
    color = random.choice(colors)
    my_circle = MyCircle((x, y), size, color, 1, euclid.Vector2(0,0), gravity)
    apply_random_vector(my_circle)
    my_circles.append(my_circle)

direction_tick = 0.0

# Defining variables for fps and continued running
fps_limit = 60
run_me = True
while run_me:
    # Limit the framerate
    dtime_ms = clock.tick(fps_limit)
    dtime = dtime_ms/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_me = False


    # Clear the screen
    screen.fill(white)
    for my_circle in my_circles:
        my_circle.move()
        my_circle.display()


    # Display everything in the screen.
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
