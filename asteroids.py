#!/usr/bin/env python3

"""asteroids.py: A Python implementation of the Asteroids arcade game written in pygame."""

from random import randrange

from pygame import Surface, display, init
from pygame.event import get as get_events
from pygame.font import Font
from pygame.key import get_pressed
from pygame.locals import HWSURFACE, QUIT, K_RETURN
from pygame.sprite import collide_circle, groupcollide, spritecollide
from pygame.time import Clock

from enemy import Asteroid
from engine import Entity, COLOR, FPS, FONT_PATH, FONT_SIZE, \
    SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_SIZE, SCREEN_CENTER
from player import Player


def main():
    init()

    clock = Clock()

    screen = display.set_mode(SCREEN_SIZE, HWSURFACE)
    display.set_caption('Python Asteroids')

    # Define the background for drawing
    background = Surface(screen.get_size())
    background = background.convert()
    background.fill(COLOR.BLACK)

    font = Font(FONT_PATH, FONT_SIZE)

    def game_loop():
        """Internal game loop function that has access to clock, screen, etc."""
        player = Player()
        asteroid_cooldown = 0
        while player:
            for event in get_events():
                if event.type == QUIT:
                    raise SystemExit('Thanks for playing!')

            laser_collide = groupcollide(player.lasers, Asteroid.group, True, True, collide_circle)

            player_collide = spritecollide(player, Asteroid.group, True, collide_circle)
            if player_collide:
                player.kill()
                player = None

            if asteroid_cooldown <= 0:
                # Spawn a new asteroid at a random point on the
                # border of the screen, at a random angle and speed
                x = 0
                y = 0
                side = randrange(1, 4)
                if side == 1:
                    x = 0
                    y = randrange(0, SCREEN_HEIGHT)
                if side == 2:
                    x = randrange(0, SCREEN_WIDTH)
                    y = 0
                if side == 3:
                    x = SCREEN_WIDTH
                    y = randrange(0, SCREEN_HEIGHT)
                if side == 4:
                    x = randrange(0, SCREEN_WIDTH)
                    y = SCREEN_HEIGHT

                angle = randrange(0, 360)
                speed = randrange(1, 5)

                asteroid = Asteroid(3, speed, angle, pos=(x, y))
                asteroid_cooldown = 450

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

            asteroid_cooldown -= 1

            # Advance the clock
            clock.tick(FPS)

    def start_loop():
        (w, h) = SCREEN_CENTER
        textpos2 = (w, h + FONT_SIZE + 20)

        text1 = font.render('ASTEROIDS', 1, COLOR.WHITE)
        text2 = font.render('Press Enter', 1, COLOR.WHITE)

        textpos1 = text1.get_rect(center=SCREEN_CENTER)
        textpos2 = text2.get_rect(center=textpos2)

        waiting = True
        while waiting:
            for event in get_events():
                if event.type == QUIT:
                    raise SystemExit('Thanks for playing!')

            keys = get_pressed()
            if keys[K_RETURN]:
                return

            screen.blit(background, (0, 0))

            screen.blit(text1, textpos1)
            screen.blit(text2, textpos2)

            display.update()

            clock.tick(FPS)

    def end_loop():
        (w, h) = SCREEN_CENTER
        textpos2 = (w, h + FONT_SIZE + 20)

        text1 = font.render('Play Again?', 1, COLOR.WHITE)
        text2 = font.render('Press Enter', 1, COLOR.WHITE)

        textpos1 = text1.get_rect(center=SCREEN_CENTER)
        textpos2 = text2.get_rect(center=textpos2)

        waiting = True
        while waiting:
            for event in get_events():
                if event.type == QUIT:
                    raise SystemExit('Thanks for playing!')

            keys = get_pressed()
            if keys[K_RETURN]:
                return True

            screen.blit(background, (0, 0))

            screen.blit(text1, textpos1)
            screen.blit(text2, textpos2)

            display.update()

            clock.tick(FPS)

        return False

    play = True
    while play:
        start_loop()
        game_loop()
        play = end_loop()
        Entity.group.empty()
        Asteroid.group.empty()
        Asteroid.number_destroyed = 0


if __name__ == '__main__':
    main()
