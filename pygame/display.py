"""Minimal pygame.display stub for CI tests."""


from pygame import Surface


def set_mode(size):
    """Return a dummy Surface."""
    return Surface()


def set_caption(title):
    """Stub for pygame.display.set_caption()."""
