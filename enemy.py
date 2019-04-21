"""enemy.py: Asteroids and other enemy Entities"""

from pygame.math import Vector2 as Vector
from pygame.sprite import Group as SpriteGroup

from engine import Entity, COLOR

class Asteroid(Entity):
    """Standard Asteroid Entity"""

    group = SpriteGroup()

    def __init__(self, tier=1, speed=3, angle=0, pos=(0, 0)):
        # Tier determines the size, and how many times it breaks apart
        size = (tier * 10, tier * 10)
        Entity.__init__(self, size, pos)

        self.tier = tier

        self.velocity.from_polar((speed, angle))
        self.angle = angle
        self.position = Vector(pos)

        # The angle spread of the children when the asteroid breaks apart
        self.spread = 20

        self.image.fill(COLOR.WHITE)
        self.test = 120

        Asteroid.group.add(self)

    def hit(self):
        if self.tier > 1:
            # Spawn two new asteroids of a tier lower
            (speed, _) = self.velocity.as_polar()
            angle1 = self.angle - self.spread
            angle2 = self.angle + self.spread
            asteroid1 = Asteroid(self.tier - 1, speed, angle1, self.position)
            asteroid2 = Asteroid(self.tier - 1, speed, angle2, self.position)

        Entity.hit(self)
