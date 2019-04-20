#!/usr/bin/env python3

"""asteroids.py: A Python implementation of the Asteroids arcade game written in pygame."""

import pygame
from pygame.locals import *

from engine import Entity, COLOR, FPS, SCREEN_SIZE
from player import Player


if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Python Asteroids')

    # Define the background for drawing
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(COLOR.BLACK)

    player = Player()

    # Event loop .
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit('Thanks for playing!')

        # Draw the background to the screen
        screen.blit(background, (0, 0))

        # Update all entities and draw them
        Entity.group.update()
        Entity.group.draw(screen)

        # Display what has been drawn
        pygame.display.update()

        # Advance the clock
        clock.tick(FPS)
