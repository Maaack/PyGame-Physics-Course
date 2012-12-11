#!/usr/bin/env python
# MyCircle Class
# Experimenting with circles that rotate so that
# I may eventually get to hexagons.

class MyCircle:
    def __init__(self, position, size, color = (255,255,255), width = 1):
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

    def vector_and_accel(self, time):
        vector = self.vector + self.accel * time
        return vector

    def position_and_vector(self, time):
        x = self.x + (self.vector.x * time) + 0.5*(self.accel.x * (time ** 2))
        y = self.y + (self.vector.y * time) + 0.5*(self.accel.y * (time ** 2))
        return x, y

    def move(self):
        self.x, self.y = self.position_and_vector(dtime)
        self.vector = self.vector_and_accel(dtime)
        self.bounce()
        return x, y

    # Just for debugging
    def __str__(self):
        return "( " + str(self.x) + ", " + str(self.y) + " ), " + str(self.size) + ", ( " + str(self.vector.x) + ", " + str(self.vector.y) + " ) "

    def update_vector(self, vector):
        self.vector = vector
