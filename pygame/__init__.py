"""Minimal pygame stub for CI tests."""
import pygame.display
import pygame.draw
import pygame.event
import pygame.rect
import pygame.time

QUIT = 0
KEYDOWN = 1

K_UP = 273
K_DOWN = 274
K_LEFT = 276
K_RIGHT = 275
K_ESCAPE = 27


def init():
    """Initialize pygame (stub)."""
    return None


def quit():
    """Quit pygame (stub)."""
    return None


class Surface:
    """Represent a drawable surface (stub)."""

    def fill(self, color):
        """Fill the surface with a color (stub)."""
        return None


display = pygame.display
draw = pygame.draw
event = pygame.event
time = pygame.time
Rect = pygame.rect.Rect
