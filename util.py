"""util.py: General utility functions and constants"""

from types import SimpleNamespace
import pygame

# All the r,g,b colors that the game uses
COLOR = SimpleNamespace(
    BLACK=(0, 0, 0),
    WHITE=(255, 255, 255),
    GREY=(50, 50, 50)
)


# def rot_center(surf, angle):
#     """Rotate a Surface, maintaining position."""
#     loc = surf.get_rect().center  #rot_image is not defined
#     rot_surf = pygame.transform.rotate(surf, angle)
#     rot_surf.get_rect().center = loc
#     return rot_surf
