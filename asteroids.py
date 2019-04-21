#!/usr/bin/env python3

"""asteroids.py: A Python implementation of the Asteroids arcade game written in pygame."""

from pygame import Surface, display, init
from pygame.event import get as get_events
from pygame.font import Font
from pygame.locals import HWSURFACE, QUIT
from pygame.sprite import collide_circle, groupcollide, spritecollide
from pygame.time import Clock

from enemy import Asteroid
from engine import Entity, COLOR, FPS, SCREEN_SIZE, FONT_PATH
from player import Player


if __name__ == '__main__':
    init()

    clock = Clock()

    screen = display.set_mode(SCREEN_SIZE, HWSURFACE)
    display.set_caption('Python Asteroids')

    # Define the background for drawing
    background = Surface(screen.get_size())
    background = background.convert()
    background.fill(COLOR.BLACK)

    font = Font(FONT_PATH, 36)

    player = Player()

    test = Asteroid(3, angle=190)

    # Event loop
    while True:
        for event in get_events():
            if event.type == QUIT:
                raise SystemExit('Thanks for playing!')

        laser_collisions = groupcollide(player.lasers, Asteroid.group, False, False, collide_circle)
        for laser, asteroids in laser_collisions.items():
            for asteroid in asteroids:
                asteroid.hit()
            laser.hit()

        player_collisions = spritecollide(player, Asteroid.group, False, collide_circle)
        if player_collisions:
            for asteroid in player_collisions:
                asteroid.hit()
            player.hit()

        # Draw the background to the screen
        screen.blit(background, (0, 0))

        # Draw score in top left
        text = font.render(str(Asteroid.number_destroyed), 1, COLOR.WHITE)
        screen.blit(text, (10, 10))

        # Update all entities and draw them
        Entity.group.update()
        Entity.group.draw(screen)

        # Display what has been drawn
        display.update()

        # Advance the clock
        clock.tick(FPS)
