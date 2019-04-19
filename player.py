"""player.py"""

import pygame
# from pygame.locals import *
from pygame.math import Vector2 as Vector

from engine import Entity, COLOR

class Player(Entity):
    """Entity for the player, controls all movement and shooting"""

    def __init__(self, pos):
        Entity.__init__(self, (18, 18), pos)

        # Acceleration vector that will be rotated and added to velocity
        self.acceleration = Vector(0, -0.2)

        # controls how quickly the ship slows down
        self.slow_speed = 0.1

        # controls how quickly the ship rotates and slows its rotation
        self.rotate_increment = 0.5
        self.slow_rotation = self.rotate_increment / 2

        # Draws an arrow facing in the direction of angle to serve as the ship
        size = self.image.get_size()
        arrow_points = [
            (0, size[1] - 1),  # bottom left
            ((size[0] - 1) / 2, 0),  # top middle
            (size[0] - 1, size[1] - 1)  # bottom right
        ]
        pygame.draw.lines(self.image, COLOR.WHITE, False, arrow_points, 1)

    def calc_rotation(self):
        """Calculates the next angle in the rotation"""
        # Slow the rotation
        if self.rotation_speed > 0:
            self.rotation_speed -= self.slow_rotation
        elif self.rotation_speed < 0:
            self.rotation_speed += self.slow_rotation
        return Entity.calc_rotation(self)

    def calc_position(self):
        # simulate friction to slow the ship
        friction = self.velocity.length() - self.slow_speed
        if friction <= 0:
            friction = 0
        try:
            self.velocity.scale_to_length(friction)
        except ValueError as _:
            # Fixes vector scaling issues
            self.velocity = Vector()
        return Entity.calc_position(self)

    def rotate(self, angle=0):
        self.acceleration.rotate_ip(self.rotation_speed)
        Entity.rotate(self, angle)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rotation_speed -= self.rotate_increment
        if keys[pygame.K_RIGHT]:
            self.rotation_speed += self.rotate_increment
        if keys[pygame.K_UP]:
            self.velocity += self.acceleration

        Entity.update(self)
