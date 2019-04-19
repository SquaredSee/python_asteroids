#!/usr/bin/env python3

"""asteroids.py: A Python implementation of the Asteroids arcade game written in pygame."""

import pygame
from pygame.locals import *

from engine import Entity, COLOR, FPS
from player import Player

import logging
log = logging.getLogger('asteroids')


if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Asteroids')

    # Define the background for drawing later
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    entities = pygame.sprite.Group()
    char = Player((250, 250))
    entities.add(char)
    x = 50
    y = 50

    # Event loop .
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit('Thanks for playing!')

        screen.blit(background, (0, 0))
        entities.update()
        entities.draw(screen)
        pygame.display.update()

        clock.tick(FPS)
