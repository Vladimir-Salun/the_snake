from random import choice, randint
from typing import List, Optional, Tuple
from abc import abstractmethod

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE
# Типы данных для направления движения и цветов
COORDINATE = Tuple[int, int]
COLOR = Tuple[int, int, int]
# Направления движения:
UP: COORDINATE = (0, -1)
DOWN: COORDINATE = (0, 1)
LEFT: COORDINATE = (-1, 0)
RIGHT: COORDINATE = (1, 0)

# Цвет объекта по умолчанию
DEFAULT_COLOR: COLOR = (255, 255, 255)
# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс."""

    def __init__(self, position: COORDINATE = (0, 0),
                 body_color: COLOR = DEFAULT_COLOR):
        """Инициализация игрового объекта."""
        self.position = position
        self.body_color = body_color

    @abstractmethod
    def draw(self) -> None:
        """Абстрактный метод."""
        raise NotImplementedError(
            'Метот draw() должен быть переопределен в дочерних классах'
        )


class Snake(GameObject):
    """Дочерний класс,описывающий змейку и её поведение."""

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


# Тут опишите все классы игры.
def handle_keys():
    """Обработка действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
    return True

    # pg.quit()
    # raise SystemExit
    # elif event.type == pg.KEYDOWN:
    #     if event.key == pg.K_UP and game_object.direction != DOWN:
    #         game_object.next_direction = UP
    #     elif event.key == pg.K_DOWN and game_object.direction != UP:
    #         game_object.next_direction = DOWN
    #     elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
    #         game_object.next_direction = LEFT
    #     elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
    #         game_object.next_direction = RIGHT


def main() -> None:
    """Основной цикл игры."""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    running = True
    while running:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        running = handle_keys()
        pg.display.update()
    pg.quit()

    # Тут опишите основную логику игры.


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
