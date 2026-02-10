"""Minimal pygame.display stub for CI tests."""


from pygame import Surface


def set_mode(size):
    """Create and return a dummy surface."""
    return Surface()


def set_caption(title):
    """Set window caption (stub)."""
