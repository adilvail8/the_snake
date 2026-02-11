"""Snake game for educational project."""

from random import randint

import pygame


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20
MIN_SPEED = 5
MAX_SPEED = 60

KEY_TO_DIRECTION = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

OPPOSITE_DIRECTION = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


def _set_caption(speed, best_length, paused):
    """Update window caption with helpful info."""
    status = 'PAUSE' if paused else 'RUN'
    pygame.display.set_caption(
        'ESC=exit | SPACE=pause | +/- speed | '
        f'speed={speed} | best={best_length} | {status}'
    )


class GameObject:
    """Base class for game objects."""

    def __init__(self, position, body_color):
        """Create an object with position and body color."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Draw the object."""
        raise NotImplementedError

    @staticmethod
    def _cell_rect(position):
        """Return rect for a single grid cell."""
        return pygame.Rect(position, (GRID_SIZE, GRID_SIZE))

    def _draw_cell(self, position, color):
        """Draw one grid cell with border."""
        rect = self._cell_rect(position)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Apple that the snake eats."""

    def __init__(self):
        """Create apple and place it randomly."""
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Place apple in a random cell."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Draw apple."""
        self._draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Snake controlled by player."""

    def __init__(self):
        """Create snake in the center."""
        start_position = (
            GRID_WIDTH // 2 * GRID_SIZE,
            GRID_HEIGHT // 2 * GRID_SIZE,
        )
        super().__init__(start_position, SNAKE_COLOR)
        self.positions = [start_position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Return snake head position."""
        return self.positions[0]

    def update_direction(self):
        """Apply delayed direction change."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Move snake by one cell."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Reset snake to initial state."""
        self.__init__()

    def draw(self):
        """Draw only changed snake cells (head and tail)."""
        head = self.get_head_position()
        self._draw_cell(head, self.body_color)

        if self.last is not None:
            self._draw_cell(self.last, BOARD_BACKGROUND_COLOR)


def _apply_speed_change(current_speed, delta):
    """Change speed with limits."""
    new_speed = current_speed + delta
    if new_speed < MIN_SPEED:
        return MIN_SPEED
    if new_speed > MAX_SPEED:
        return MAX_SPEED
    return new_speed


def handle_keys(snake):
    """Handle input and update snake direction."""
    global _CURRENT_SPEED, _PAUSED

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type != pygame.KEYDOWN:
            continue

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit

        if event.key == pygame.K_SPACE:
            _PAUSED = not _PAUSED
            continue

        if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            _CURRENT_SPEED = _apply_speed_change(_CURRENT_SPEED, -2)
            continue

        if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
            _CURRENT_SPEED = _apply_speed_change(_CURRENT_SPEED, 2)
            continue

        direction = KEY_TO_DIRECTION.get(event.key)
        if direction is None:
            continue

        if direction != OPPOSITE_DIRECTION[snake.direction]:
            snake.next_direction = direction


def _place_apple_not_on_snake(apple, snake):
    """Reposition apple until it is not on the snake."""
    apple.randomize_position()
    while apple.position in snake.positions:
        apple.randomize_position()


def main():
    """Run the game loop."""
    global _CURRENT_SPEED, _PAUSED

    pygame.init()
    _CURRENT_SPEED = SPEED
    _PAUSED = False
    best_length = 1

    snake = Snake()
    apple = Apple()
    _place_apple_not_on_snake(apple, snake)

    screen.fill(BOARD_BACKGROUND_COLOR)
    apple.draw()
    snake.draw()
    pygame.display.update()

    while True:
        clock.tick(_CURRENT_SPEED)
        handle_keys(snake)
        _set_caption(_CURRENT_SPEED, best_length, _PAUSED)

        if _PAUSED:
            continue

        snake.update_direction()
        snake.move()

        head = snake.get_head_position()
        if head == apple.position:
            snake.length += 1
            if snake.length > best_length:
                best_length = snake.length
            _place_apple_not_on_snake(apple, snake)
            apple.draw()

        if head in snake.positions[1:]:
            best_length = max(best_length, snake.length)
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            _place_apple_not_on_snake(apple, snake)
            apple.draw()

        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
