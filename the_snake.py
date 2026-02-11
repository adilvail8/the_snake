"""Simple Snake game."""

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

SPEED = 10
SPEED_CHANGE = 2
MIN_SPEED = 5
MAX_SPEED = 30

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
clock = pygame.time.Clock()


class GameObject:
    """Base game object."""

    def __init__(self, body_color=None):
        """Initialize object."""
        self.position = (0, 0)
        self.body_color = body_color

    def draw_cell(self, position, color=None):
        """Draw one cell with object's color."""
        if color is None:
            color = self.body_color
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)

    def draw(self):
        """Draw object - must be implemented in child classes."""
        raise NotImplementedError


class Apple(GameObject):
    """Apple object."""

    def __init__(self):
        """Create apple."""
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Place apple randomly."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Draw apple with border."""
        self.draw_cell(self.position)
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Snake object."""

    def __init__(self):
        """Create snake."""
        super().__init__(SNAKE_COLOR)
        start_position = (
            GRID_WIDTH // 2 * GRID_SIZE,
            GRID_HEIGHT // 2 * GRID_SIZE,
        )
        self.positions = [start_position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Return head position."""
        return self.positions[0]

    def update_direction(self):
        """Update direction."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Move snake."""
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
        """Reset snake."""
        self.__init__()

    def draw(self):
        """Draw only changed cells: new head and old tail."""
        self.draw_cell(self.get_head_position())

        if self.last is not None:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)


def handle_keys(snake, speed):
    """Handle keyboard and return new speed."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

            # Speed control
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                speed = min(speed + SPEED_CHANGE, MAX_SPEED)
            elif event.key == pygame.K_MINUS:
                speed = max(speed - SPEED_CHANGE, MIN_SPEED)

            # Direction control
            direction = KEY_TO_DIRECTION.get(event.key)
            if direction is not None:
                if direction != OPPOSITE_DIRECTION[snake.direction]:
                    snake.next_direction = direction

    return speed


def update_caption(speed, record):
    """Update window caption with game info."""
    caption = (
        f'Змейка - Скорость: {speed} | '
        f'Рекорд: {record} | '
        f'ESC: выход | +/-: скорость'
    )
    pygame.display.set_caption(caption)


def place_apple(apple, snake):
    """Place apple not on snake."""
    apple.randomize_position()
    while apple.position in snake.positions:
        apple.randomize_position()


def main():
    """Run game."""
    pygame.init()

    snake = Snake()
    apple = Apple()
    place_apple(apple, snake)

    speed = SPEED
    record = 1

    screen.fill(BOARD_BACKGROUND_COLOR)
    apple.draw()
    snake.draw()
    update_caption(speed, record)
    pygame.display.update()

    while True:
        clock.tick(speed)
        speed = handle_keys(snake, speed)

        snake.update_direction()
        snake.move()

        head = snake.get_head_position()

        if head == apple.position:
            snake.length += 1
            record = max(record, snake.length)
            update_caption(speed, record)
            place_apple(apple, snake)
            apple.draw()

        if head in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            place_apple(apple, snake)
            apple.draw()
            update_caption(speed, record)

        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
