"""Учебный проект Змейка."""
from random import randint
from typing import Tuple, List, Optional
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
SPEED: int = 10

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
    """Дочерний класс, описывающий змейку и её поведение."""

    def __init__(self) -> None:
        """Инициализация змейки."""
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), SNAKE_COLOR)
        self.length: int = 1
        self.speed: int = SPEED
        self.positions: List[COORDINATE] = [self.position]
        self.direction: COORDINATE = RIGHT
        self.next_direction: Optional[COORDINATE] = None
        self.last: Optional[COORDINATE] = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple_position) -> COORDINATE:
        """Обновляет позицию змейки."""
        self.update_direction()
        x, y = self.position
        dx, dy = self.direction
        new_x = (x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        next_position = (new_x, new_y)
        if next_position == apple_position:
            self.grow()
        return next_position

    def new_position_snake(self, next_position: COORDINATE) -> None:
        """Устанавливает новую позицию в змейку."""
        self.positions.insert(0, next_position)
        self.position = next_position
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def grow(self) -> None:
        """Увеличивает длину змейки."""
        self.length += 1

    def check_collision(self) -> bool:
        """Проверяет, столкнулась ли змейка со своим телом."""
        head = self.positions[0]
        for segment in self.positions[1:]:
            if head == segment:
                return True
        return False

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
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


class Apple(GameObject):
    """Дочерний класс, описывающий яблоко и действия с ним."""

    def __init__(self, snake_position: List[COORDINATE] = [(0, 0)]) -> None:
        """Инициализация яблока."""
        super().__init__(position=(0, 0), body_color=APPLE_COLOR)
        self.position = self.randomize_position(snake_position)

    def randomize_position(
            self, snake_positions: List[COORDINATE]
    ) -> COORDINATE:
        """Устанавливает случайное положение яблока."""
        while True:
            posit_x = randint(0, GRID_WIDTH - 1)
            posit_y = randint(0, GRID_HEIGHT - 1)
            new_posit = (posit_x * GRID_SIZE, posit_y * GRID_SIZE)
            if new_posit not in snake_positions:
                return new_posit

    def new_position(self, snake_positions: List[COORDINATE]) -> None:
        """Генерирует новую позицию для яблока."""
        self.position = self.randomize_position(snake_positions)

    def draw(self) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object) -> bool:
    """Обработка действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

    return True


def main() -> None:
    """Основной цикл игры."""
    # Инициализация PyGame:
    pg.init()
    # Экземпляры классов.
    snake = Snake()
    apple = Apple(snake.positions)
    running = True
    # Основную логику игры.
    while running:
        clock.tick(snake.speed)
        screen.fill(BOARD_BACKGROUND_COLOR)
        running = handle_keys(snake)
        next_position = snake.move(apple.position)
        if snake.check_collision():
            snake = Snake()
            apple = Apple(snake.positions)
        elif next_position != apple.position:
            snake.new_position_snake(next_position)

        # Обновление позиции яблока, если змейка съела его
        if next_position == apple.position:
            snake.grow()
            apple.new_position(snake.positions)
        snake.draw()
        apple.draw()
        pg.display.update()
    pg.quit()


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
#             elif event.key == pygame.K_LEFT and
#                            game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT
#                           and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
