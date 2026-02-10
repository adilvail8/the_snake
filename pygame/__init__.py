"""Minimal pygame stub for CI tests."""


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


from pygame import display as display  # noqa: E402
from pygame import draw as draw  # noqa: E402
from pygame import event as event  # noqa: E402
from pygame import rect as rect  # noqa: E402
from pygame import time as time  # noqa: E402

Rect = rect.Rect
