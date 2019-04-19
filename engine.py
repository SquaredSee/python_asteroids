"""engine.py: Basic Entity movement and other physics calculations"""

from pygame import Surface
from pygame.math import Vector2 as Vector
from pygame.sprite import Sprite
from pygame.transform import rotate

FPS = 60

# Direction unit vectors
UP = Vector(0, 1)
DOWN = Vector(0, -1)
LEFT = Vector(-1, 0)
RIGHT = Vector(1, 0)


class Entity(Sprite):
    """Base class for all moving Entities"""

    def __init__(self, size=(1, 1), pos=(0, 0)):
        Sprite.__init__(self)

        self.image = Surface(size).convert()
        # self.image.fill(COLOR.WHITE)
        self.orig_img = self.image
        self.rect = self.image.get_rect(center=pos)

        self.position = Vector(pos)
        self.velocity = Vector(0, 0)
        self.angle = 0
        self.rotation_speed = 0
        self.slow_speed = 1
        self.max_velocity = 10

    def calc_position(self):
        """Calculates the next position based on velocity"""
        if self.velocity.length() > self.max_velocity:
            # Scale velocity to max
            self.velocity.scale_to_length(self.max_velocity)
        return self.position + self.velocity

    def calc_rotation(self):
        """Calculates the next angle in the rotation"""
        return self.angle + self.rotation_speed

    def move(self, pos=Vector(0, 0)):
        """Moves the position to the Vector2 given"""
        self.position = pos
        # Set the center of the rect to the position
        self.rect.center = self.position

    def rotate(self, angle=0):
        """Rotates the acceleration vector and the sprite image"""
        # Normalize angle into 360 deg
        if angle > 360:
            angle -= 360
        elif angle < 360:
            angle += 360

        self.angle = angle
        self.image = rotate(self.orig_img, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        """Called every tick to update the state of the Entity"""
        self.rotate(self.calc_rotation())
        self.move(self.calc_position())
