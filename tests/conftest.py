<<<<<<< HEAD
"""Conftest module for the_snake tests."""
=======
>>>>>>> b1059f8 (update)
import os
import sys
from multiprocessing import Process
from pathlib import Path
from typing import Any

<<<<<<< HEAD
=======
from pygame.time import Clock
>>>>>>> b1059f8 (update)
import pytest
import pytest_timeout

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))

# Hide the pygame screen
os.environ['SDL_VIDEODRIVER'] = 'dummy'

TIMEOUT_ASSERT_MSG = (
    'Проект работает некорректно, проверка прервана.\n'
    'Вероятные причины ошибки:\n'
    '1. Исполняемый код (например, вызов функции `main()`) оказался в '
<<<<<<< HEAD
    'глобальной зоне видимости. Как исправить: вызов функции `main` '
    'поместите внутрь конструкции `if __name__ == "__main__":`.\n'
    '2. В цикле `while True` внутри функции `main` отсутствует вызов '
    'метода `tick` объекта `clock`. Не изменяйте прекод в этой части.'
=======
    'глобальной зоне видимости. Как исправить: вызов функции `main` поместите '
    'внутрь конструкции `if __name__ == "__main__":`.\n'
    '2. В цикле `while True` внутри функции `main` отсутствует вызов метода '
    '`tick` объекта `clock`. Не изменяйте прекод в этой части.'
>>>>>>> b1059f8 (update)
)


def import_the_snake():
<<<<<<< HEAD
    """Import the_snake module."""
    import the_snake
    _ = the_snake  # noqa
=======
    import the_snake  # noqa
>>>>>>> b1059f8 (update)


@pytest.fixture(scope='session')
def snake_import_test():
<<<<<<< HEAD
    """Test if the_snake module can be imported without hanging."""
=======
>>>>>>> b1059f8 (update)
    check_import_process = Process(target=import_the_snake)
    check_import_process.start()
    pid = check_import_process.pid
    check_import_process.join(timeout=1)
    if check_import_process.is_alive():
        os.kill(pid, 9)
        raise AssertionError(TIMEOUT_ASSERT_MSG)


@pytest.fixture(scope='session')
def _the_snake(snake_import_test):
<<<<<<< HEAD
    """Import and validate the_snake module."""
=======
>>>>>>> b1059f8 (update)
    try:
        import the_snake
    except ImportError as error:
        raise AssertionError(
            'При импорте модуль `the_snake` произошла ошибка:\n'
            f'{type(error).__name__}: {error}'
        )
    for class_name in ('GameObject', 'Snake', 'Apple'):
        assert hasattr(the_snake, class_name), (
<<<<<<< HEAD
            f'Убедитесь, что в модуле `the_snake` определен класс '
            f'`{class_name}`.'
=======
            f'Убедитесь, что в модуле `the_snake` определен класс `{class_name}`.'
>>>>>>> b1059f8 (update)
        )
    return the_snake


def write_timeout_reasons(text, stream=None):
    """Write possible reasons of tests timeout to stream.

    The function to replace pytest_timeout traceback output with possible
    reasons of tests timeout.
    Appears only when `thread` method is used.
    """
    if stream is None:
        stream = sys.stderr
    text = TIMEOUT_ASSERT_MSG
    stream.write(text)


pytest_timeout.write = write_timeout_reasons


def _create_game_object(class_name, module):
<<<<<<< HEAD
    """Create game object instance."""
=======
>>>>>>> b1059f8 (update)
    try:
        return getattr(module, class_name)()
    except TypeError as error:
        raise AssertionError(
<<<<<<< HEAD
            f'При создании объекта класса `{class_name}` произошла '
            f'ошибка:\n'
=======
            f'При создании объекта класса `{class_name}` произошла ошибка:\n'
>>>>>>> b1059f8 (update)
            f'`{type(error).__name__}: {error}`\n'
            f'Если в конструктор класса `{class_name}` помимо параметра '
            '`self` передаются какие-то ещё параметры - убедитесь, что для '
            'них установлены значения по умолчанию. Например:\n'
            '`def __init__(self, <параметр>=<значение_по_умолчанию>):`'
        )


@pytest.fixture
def game_object(_the_snake):
<<<<<<< HEAD
    """Create GameObject instance."""
=======
>>>>>>> b1059f8 (update)
    return _create_game_object('GameObject', _the_snake)


@pytest.fixture
def snake(_the_snake):
<<<<<<< HEAD
    """Create Snake instance."""
=======
>>>>>>> b1059f8 (update)
    return _create_game_object('Snake', _the_snake)


@pytest.fixture
def apple(_the_snake):
<<<<<<< HEAD
    """Create Apple instance."""
=======
>>>>>>> b1059f8 (update)
    return _create_game_object('Apple', _the_snake)


class StopInfiniteLoop(Exception):
<<<<<<< HEAD
    """Exception to break infinite loops in tests."""

=======
>>>>>>> b1059f8 (update)
    pass


def loop_breaker_decorator(func):
<<<<<<< HEAD
    """Decorator to break infinite loops after 2 calls."""
=======
>>>>>>> b1059f8 (update)
    call_counter = 0

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        nonlocal call_counter
        call_counter += 1
        if call_counter > 1:
            raise StopInfiniteLoop
        return result
    return wrapper


@pytest.fixture
def modified_clock(_the_snake):
<<<<<<< HEAD
    """Modify clock to break infinite loops."""
    from pygame.time import Clock

=======
>>>>>>> b1059f8 (update)
    class _Clock:
        def __init__(self, clock_obj: Clock) -> None:
            self.clock = clock_obj

        @loop_breaker_decorator
        def tick(self, *args, **kwargs):
            return self.clock.tick(*args, **kwargs)

        def __getattribute__(self, name: str) -> Any:
            if name in ['tick', 'clock']:
                return super().__getattribute__(name)
            return self.clock.__getattribute__(name)

    original_clock = _the_snake.clock
    modified_clock_obj = _Clock(original_clock)
    _the_snake.clock = modified_clock_obj
    yield
    _the_snake.clock = original_clock
