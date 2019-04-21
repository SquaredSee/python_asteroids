"""player.py: Player and related Entities"""

from pygame import K_UP, K_LEFT, K_RIGHT, K_z
from pygame.draw import lines as draw_lines
from pygame.key import get_pressed
from pygame.math import Vector2 as Vector
from pygame.sprite import Group as SpriteGroup

from engine import Entity, COLOR, SCREEN_CENTER


class Laser(Entity):
    """Entity for the projectiles the Player fires"""

    def __init__(self, pos=(0, 0), angle=0):
        Entity.__init__(self, (5, 2), pos)

        # 60 frames = 1 second
        self.lifetime = 60

        self.orig_img.fill(COLOR.WHITE)

        # angle 0 points right, so subtract 90 degrees
        angle = angle - 90
        self.velocity.from_polar((self.max_velocity, angle))
        self.rotate(angle)

    def update(self):
        Entity.update(self)
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()


class Player(Entity):
    """Entity for the player, controls all movement and shooting"""

    def __init__(self, pos=SCREEN_CENTER):
        Entity.__init__(self, (18, 18), pos)

        # Acceleration vector that will be rotated and added to velocity
        self.acceleration = Vector(0, -0.2)

        # controls how quickly the ship slows down
        self.slow_speed = 0.1

        # controls how quickly the ship rotates and slows its rotation
        self.rotate_increment = 0.5
        self.slow_rotation = self.rotate_increment / 2

        # 10 frame cooldown, start at 0
        self.fire_cooldown = 0

        # Group of all lasers for collision purposes
        self.lasers = SpriteGroup()

        # Draws an arrow facing in the direction of angle to serve as the ship
        size = self.image.get_size()
        arrow_points = [
            (0, size[1] - 1),  # bottom left
            ((size[0] - 1) / 2, 0),  # top middle
            (size[0] - 1, size[1] - 1)  # bottom right
        ]
        draw_lines(self.image, COLOR.WHITE, False, arrow_points, 2)

    def fire(self):
        """Fires a Laser Entity in the direction the ship is facing"""
        if self.fire_cooldown:
            self.fire_cooldown -= 1
        else:
            self.lasers.add(Laser(self.position, self.angle))
            self.fire_cooldown = 10

    def kill(self):
        self.lasers.empty()
        Entity.kill(self)

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
        except ValueError:
            # Fixes vector scaling issues
            self.velocity = Vector()
        return Entity.calc_position(self)

    def rotate(self, angle=0):
        self.acceleration.rotate_ip(self.rotation_speed)
        Entity.rotate(self, angle)

    def update(self):
        keys = get_pressed()

        if keys[K_LEFT]:
            self.rotation_speed -= self.rotate_increment
        if keys[K_RIGHT]:
            self.rotation_speed += self.rotate_increment
        if keys[K_UP]:
            self.velocity += self.acceleration
        if keys[K_z]:
            self.fire()

        Entity.update(self)
