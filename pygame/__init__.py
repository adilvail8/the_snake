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


def quit():
    """Quit pygame (stub)."""


class Surface:
    """Represent a drawable surface (stub)."""


class _Display:
    """Provide display-related functions."""

    def set_mode(self, size):
        """Create and return a dummy surface."""
        return Surface()

    def set_caption(self, title):
        """Set window caption (stub)."""


class _Time:
    """Provide time-related functions."""

    from pygame.time import Clock  # type: ignore


class _Event:
    """Provide event-related functions."""

    def get(self):
        """Return an empty list of events."""
        return []


class _Draw:
    """Provide drawing-related functions."""

    def rect(self, surface, color, rect_obj, width=0):
        """Draw a rectangle (stub)."""


class _Rect:
    """Provide rectangle class."""

    from pygame.rect import Rect  # type: ignore


display = _Display()
time = _Time()
event = _Event()
draw = _Draw()
Rect = _Rect.Rect
