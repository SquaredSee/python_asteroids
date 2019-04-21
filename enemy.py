"""enemy.py: Asteroids and other enemy Entities"""

from pygame.draw import polygon as draw_polygon
from pygame.math import Vector2 as Vector
from pygame.sprite import Group as SpriteGroup

from engine import Entity, COLOR


class Asteroid(Entity):
    """Standard Asteroid Entity"""

    group = SpriteGroup()

    number_destroyed = 0

    def __init__(self, tier=1, speed=3, angle=0, pos=(0, 0)):
        # Tier determines the size, and how many times it breaks apart
        size = (tier * 15, tier * 15)
        Entity.__init__(self, size, pos)

        self.tier = tier

        self.velocity.from_polar((speed, angle))
        self.angle = angle
        self.position = Vector(pos)

        # The angle spread of the children when the asteroid breaks apart
        self.spread = 20

        first = (size[0] - 1) / 3
        second = first * 2
        third = first * 3
        octagon = [
            (first, 0),  # top 1
            (second, 0),  # top 2
            (third, first),  # right 1
            (third, second),  # right 2
            (second, third),  # bottom 1
            (first, third),  # bottom 2
            (0, second),  # left 1
            (0, first)  # left 2
        ]
        draw_polygon(self.image, COLOR.WHITE, octagon, 2)

        Asteroid.group.add(self)

    def kill(self):
        if self.tier > 1:
            # Spawn two new asteroids of a tier lower
            speed = self.velocity.length()
            new_tier = self.tier - 1
            angle1 = self.angle - self.spread
            angle2 = self.angle + self.spread
            asteroid1 = Asteroid(new_tier, speed, angle1, self.position)
            asteroid2 = Asteroid(new_tier, speed, angle2, self.position)
        Asteroid.number_destroyed += 1
        Entity.kill(self)
