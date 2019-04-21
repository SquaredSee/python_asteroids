"""engine.py: Basic Entity movement and global constants"""

import sys
from os.path import join
from types import SimpleNamespace

from pygame import Surface
from pygame.math import Vector2 as Vector
from pygame.sprite import Sprite, Group as SpriteGroup
from pygame.transform import rotate

FPS = 60
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# if sys has _MEIPASS, this is a pyinstaller build so modify data paths
if hasattr(sys, '_MEIPASS'):
    DATA_PATH = join(sys._MEIPASS, 'data')
else:
    DATA_PATH = join('.', 'data')

FONT_PATH = join(DATA_PATH, 'PressStart2P-Regular.ttf')

# Use a SimpleNamespace to allow for COLOR.NAME accessing
COLOR = SimpleNamespace(
    BLACK=(0, 0, 0),
    WHITE=(255, 255, 255)
)


class Entity(Sprite):
    """Base class for all moving Entities"""

    # Keep a group of all entities for the purpose of updating and drawing
    group = SpriteGroup()

    def __init__(self, size=(1, 1), pos=(0, 0)):
        Sprite.__init__(self)

        # Radius attribute for collision detection, circle centered on pos
        self.radius = size[0] / 2

        self.image = Surface(size).convert()
        self.image.set_colorkey(COLOR.BLACK)  # set black as transparency color

        self.orig_img = self.image  # Keep an original copy for rotation purposes

        self.rect = self.image.get_rect(center=pos)

        self.position = Vector(pos)
        self.velocity = Vector(0, 0)
        self.angle = 0
        self.rotation_speed = 0
        self.max_velocity = 10

        Entity.group.add(self)

    def calc_position(self):
        """Calculates the next position based on velocity"""
        if self.velocity.length() > self.max_velocity:
            # Scale velocity to max
            self.velocity.scale_to_length(self.max_velocity)
        return self.position + self.velocity

    def calc_rotation(self):
        """Calculates the next angle in the rotation"""
        return self.angle + self.rotation_speed

    def hit(self):
        """Removes the Entity from sprite groups and deletes it"""
        self.kill()
        del self

    def move(self, pos=Vector(0, 0)):
        """Moves the position to the Vector2 given"""
        # Wrap around the screen
        if pos.x > SCREEN_WIDTH:
            pos.x = 0
        elif pos.x < 0:
            pos.x = SCREEN_WIDTH
        if pos.y > SCREEN_HEIGHT:
            pos.y = 0
        elif pos.y < 0:
            pos.y = SCREEN_HEIGHT
        self.position = pos
        # Set the center of the rect to the position
        self.rect.center = self.position

    def rotate(self, angle=0):
        """Rotates the angle and the sprite image"""
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
