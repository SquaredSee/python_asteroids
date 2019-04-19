#!/usr/bin/env python3

"""asteroids.py: A Python implementation of the Asteroids arcade game written in pygame."""

import pygame
from pygame.locals import *

from util import COLOR
from engine import FPS, Entity, UP, DOWN, LEFT, RIGHT
# from player import Player

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
    char = Entity((18, 18), (250, 250))
    entities.add(char)
    x = 50
    y = 50

    # Event loop .
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit('Thanks for playing!')

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            char.velocity += LEFT
        if keys[pygame.K_RIGHT]:
            char.velocity += RIGHT
        if keys[pygame.K_UP]:
            char.velocity += DOWN
        if keys[pygame.K_DOWN]:
            char.velocity += UP

        screen.blit(background, (0, 0))
        entities.update()
        entities.draw(screen)
        pygame.display.update()

        clock.tick(FPS)
