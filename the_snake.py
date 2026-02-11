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

SPEED = 20

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
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()


class GameObject:
    """Base game object."""

    def __init__(self, position, body_color):
        """Initialize object."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Draw object."""
        raise NotImplementedError

    @staticmethod
    def _rect(position):
        """Return grid rect."""
        return pygame.Rect(position, (GRID_SIZE, GRID_SIZE))

    def _draw_cell(self, position, color):
        """Draw one cell."""
        rect = self._rect(position)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Apple object."""

    def __init__(self):
        """Create apple."""
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Place apple randomly."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Draw apple."""
        self._draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Snake object."""

    def __init__(self):
        """Create snake."""
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
        """Draw changed snake cells."""
        head = self.get_head_position()
        self._draw_cell(head, self.body_color)

        if self.last is not None:
            self._draw_cell(self.last, BOARD_BACKGROUND_COLOR)


def handle_keys(snake):
    """Handle keyboard."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

            direction = KEY_TO_DIRECTION.get(event.key)
            if direction is not None:
                if direction != OPPOSITE_DIRECTION[snake.direction]:
                    snake.next_direction = direction


def _place_apple(apple, snake):
    """Place apple not on snake."""
    apple.randomize_position()
    while apple.position in snake.positions:
        apple.randomize_position()


def main():
    """Run game."""
    pygame.init()

    snake = Snake()
    apple = Apple()
    _place_apple(apple, snake)

    screen.fill(BOARD_BACKGROUND_COLOR)
    apple.draw()
    snake.draw()
    pygame.display.update()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.update_direction()
        snake.move()

        head = snake.get_head_position()

        if head == apple.position:
            snake.length += 1
            _place_apple(apple, snake)
            apple.draw()

        if head in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            _place_apple(apple, snake)
            apple.draw()

        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
