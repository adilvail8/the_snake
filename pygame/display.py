"""Minimal pygame.display stub for CI tests."""


def set_mode(size):
    """Create and return a dummy surface."""
    from pygame import Surface

    return Surface()


def set_caption(title):
    """Set window caption (stub)."""
    return None


def update():
    """Update the display (stub)."""
    return None


def flip():
    """Flip the display buffers (stub)."""
    return None
