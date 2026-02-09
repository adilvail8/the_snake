"""Snake game implementation using Pygame."""
from random import randint

import pygame

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость игры
SPEED = 10
MIN_SPEED = 5
MAX_SPEED = 30
SPEED_STEP = 5

# Экран и таймер
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position):
        """Отрисовать одну ячейку объекта."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовать объект на экране."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Задать случайную позицию яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовать яблоко."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
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
        """Вернуть позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновить направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Переместить змейку."""
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
        """Сбросить состояние змейки."""
        start_position = (
            GRID_WIDTH // 2 * GRID_SIZE,
            GRID_HEIGHT // 2 * GRID_SIZE,
        )
        self.position = start_position
        self.positions = [start_position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовать голову и стереть хвост."""
        # Рисуем голову
        self.draw_cell(self.get_head_position())

        # Затираем последний сегмент
        if self.last:
            rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    def draw_full(self):
        """Отрисовать всю змейку."""
        for position in self.positions:
            self.draw_cell(position)


def update_caption(speed, record):
    """Обновить заголовок окна."""
    caption = (
        f'Змейка | Скорость: {speed} (↑/↓) | '
        f'Рекорд: {record} | ESC - выход'
    )
    pygame.display.set_caption(caption)


def handle_keys(game_object, current_speed):
    """Обработать нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            # Выход по ESC
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            # Управление направлением
            if (event.key == pygame.K_UP
                    and game_object.direction != DOWN):
                game_object.next_direction = UP
            elif (event.key == pygame.K_DOWN
                  and game_object.direction != UP):
                game_object.next_direction = DOWN
            elif (event.key == pygame.K_LEFT
                  and game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif (event.key == pygame.K_RIGHT
                  and game_object.direction != LEFT):
                game_object.next_direction = RIGHT
    return current_speed


def handle_speed_change():
    """Обработать изменение скорости."""
    keys = pygame.key.get_pressed()
    speed_change = 0

    if keys[pygame.K_PAGEUP] or keys[pygame.K_PLUS]:
        speed_change = SPEED_STEP
    elif keys[pygame.K_PAGEDOWN] or keys[pygame.K_MINUS]:
        speed_change = -SPEED_STEP

    return speed_change


def main():
    """Основной игровой цикл."""
    pygame.init()

    snake = Snake()
    apple = Apple()
    current_speed = SPEED
    record_length = 1

    # Первая отрисовка
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake.draw_full()
    apple.draw()
    update_caption(current_speed, record_length)
    pygame.display.update()

    while True:
        clock.tick(current_speed)
        current_speed = handle_keys(snake, current_speed)

        # Изменение скорости
        speed_change = handle_speed_change()
        if speed_change:
            current_speed = max(
                MIN_SPEED,
                min(MAX_SPEED, current_speed + speed_change)
            )
            update_caption(current_speed, record_length)

        snake.update_direction()
        snake.move()

        # Проверка поедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Обновляем рекорд
            if snake.length > record_length:
                record_length = snake.length
                update_caption(current_speed, record_length)

        # Проверка столкновения с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.draw_full()
            apple.draw()
            pygame.display.update()
            continue

        # Отрисовка (только изменения)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
