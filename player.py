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
        self.max_acceleration = 2

        self.vel_slow = 2
        self.accel_slow = 0.1

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
            self.rotation_speed -= .5
        elif self.rotation_speed < 0:
            self.rotation_speed += .5
        return Entity.calc_rotation(self)

    def rotate(self, angle=0):
        self.acceleration.rotate_ip(self.rotation_speed)
        Entity.rotate(self, angle)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rotation_speed -= 1
        if keys[pygame.K_RIGHT]:
            self.rotation_speed += 1
        if keys[pygame.K_UP]:
            self.velocity += self.acceleration
        if keys[pygame.K_DOWN]:
            pass
            # new_velocity = self.velocity - self.acceleration
            # (_, angle) = new_velocity.as_polar()
            # if abs(self.angle - angle) > 175:
            #     new_velocity.scale_to_length(0)
            # self.velocity = new_velocity

        Entity.update(self)
