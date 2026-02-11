"""Simple Snake game."""

from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10
SPEED_CHANGE = 2
MIN_SPEED = 5
MAX_SPEED = 30

# Центр игрового поля
CENTER_POSITION = (
    GRID_WIDTH // 2 * GRID_SIZE,
    GRID_HEIGHT // 2 * GRID_SIZE,
)

# Начальная позиция объектов
INITIAL_POSITION = (0, 0)

# Все возможные ячейки на поле
ALL_CELLS = set(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)
)

# Управление
KEYS_TO_DIRECTIONS = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
    # WASD для левшей
    pygame.K_w: UP,
    pygame.K_s: DOWN,
    pygame.K_a: LEFT,
    pygame.K_d: RIGHT,
}

OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None):
        """Инициализация базового объекта."""
        self.position = INITIAL_POSITION
        self.body_color = body_color

    def draw_cell(self, position, color=None):
        """Отрисовка одной ячейки."""
        color = color or self.body_color
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        if color != BORDER_COLOR:
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовка объекта - должна быть реализована в наследниках."""
        raise NotImplementedError(
            f'Метод draw должен быть реализован в дочернем классе '
            f'{self.__class__.__name__}'
        )


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, occupied_positions, body_color=APPLE_COLOR):
        """Инициализация яблока."""
        super().__init__(body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Устанавливает случайную позицию яблока."""
        self.position = choice(tuple(ALL_CELLS - set(occupied_positions)))

    def draw(self):
        """Отрисовка яблока."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация змейки."""
        super().__init__(body_color)
        self.reset()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, direction):
        """Обновляет направление движения змейки."""
        if direction != OPPOSITE_DIRECTIONS[self.direction]:
            self.direction = direction

    def move(self):
        """Двигает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction

        self.positions.insert(
            0,
            (
                (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
                (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT,
            ),
        )

        self.last = self.positions.pop() if len(
            self.positions
        ) > self.length else None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [CENTER_POSITION]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self):
        """Отрисовка змейки."""
        self.draw_cell(self.get_head_position())
        self.draw_cell(self.last, BOARD_BACKGROUND_COLOR) if self.last else 0


def handle_keys(snake, speed):
    """Обработка действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            # Speed control
            if event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                speed = min(speed + SPEED_CHANGE, MAX_SPEED)
            elif event.key in (pygame.K_MINUS, pygame.K_UNDERSCORE):
                speed = max(speed - SPEED_CHANGE, MIN_SPEED)

            # Direction control
            snake.update_direction(
                KEYS_TO_DIRECTIONS.get(event.key, snake.direction)
            )

    return speed


def update_caption(speed, record):
    """Обновление заголовка окна с информацией об игре."""
    caption = (
        f'Змейка - Скорость: {speed} | '
        f'Рекорд: {record} | '
        f'ESC: выход | +/-: скорость'
    )
    if caption != pygame.display.get_caption()[0]:
        pygame.display.set_caption(caption)


def main():
    """Основная функция игры."""
    pygame.init()

    snake = Snake()
    apple = Apple(snake.positions)

    speed = SPEED
    record = 1

    while True:
        clock.tick(speed)
        speed = handle_keys(snake, speed)

        snake.move()

        head = snake.get_head_position()

        if head == apple.position:
            snake.length += 1
            record = max(record, snake.length)
            apple.randomize_position(snake.positions)
        elif head in snake.positions[4:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pygame.display.update()
        update_caption(speed, record)


if __name__ == '__main__':
    main()
