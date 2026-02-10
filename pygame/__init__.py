"""Minimal pygame stub for CI tests."""


# Event types
QUIT = 0
KEYDOWN = 1

# Key codes
K_UP = 273
K_DOWN = 274
K_LEFT = 276
K_RIGHT = 275
K_ESCAPE = 27


def init():
    """Stub for pygame.init()."""


def quit():
    """Stub for pygame.quit()."""


class Surface:
    """Stub for pygame.Surface."""


# --- submodules binding ---


class _Display:
    """Stub for pygame.display module."""

    def set_mode(self, size):
        """Return dummy Surface."""
        return Surface()

    def set_caption(self, title):
        """Stub for set_caption."""


class _Time:
    """Stub for pygame.time module."""

    from pygame.time import Clock  # type: ignore


class _Event:
    """Stub for pygame.event module."""

    def get(self):
        """Return empty event list."""
        return []


class _Draw:
    """Stub for pygame.draw module."""

    def rect(self, surface, color, rect_obj, width=0):
        """Stub for draw.rect."""


class _Rect:
    """Stub for pygame.Rect."""

    from pygame.rect import Rect  # type: ignore


# Public pygame attributes
display = _Display()
time = _Time()
event = _Event()
draw = _Draw()
Rect = _Rect.Rect
