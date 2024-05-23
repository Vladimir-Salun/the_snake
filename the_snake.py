"""Учебный проект Змейка."""
from random import randint
import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = SCREEN_WIDTH // 2 - GRID_SIZE, SCREEN_HEIGHT // 2 - GRID_SIZE
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет объекта по умолчанию
DEFAULT_COLOR = (255, 255, 255)
# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

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

    def __init__(self):
        """Инициализация игрового объекта."""
        self.position = CENTER_POSITION
        self.body_color = DEFAULT_COLOR

    @staticmethod
    def draw_cell(position, body_color) -> None:
        """Метод для отрисовки ячейки."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self) -> None:
        """Абстрактный метод."""
        raise NotImplementedError(
            'Метот draw() должен быть переопределен в дочерних классах'
        )


class Snake(GameObject):
    """Дочерний класс, описывающий змейку и её поведение."""

    position = CENTER_POSITION

    def __init__(self) -> None:
        """Инициализация змейки."""
        self.reset()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> tuple:
        """Устанавливает новую позицию в змейку."""
        return self.positions[0]

    def move(self) -> None:
        """Обновляет позицию змейки."""
        position_x, position_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_x = (position_x + direction_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (position_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        next_position = (new_x, new_y)
        if next_position in self.positions:
            self.reset()
        self.positions.insert(0, next_position)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Перезапуск игры."""
        self.length = 1
        self.speed = SPEED
        self.positions = [CENTER_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.body_color = SNAKE_COLOR

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions:
            self.draw_cell(position, self.body_color)


class Apple(GameObject):
    """Дочерний класс, описывающий яблоко и действия с ним."""

    def __init__(self):
        """Инициализация яблока."""
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(
            self, random_positions=CENTER_POSITION
    ):
        """Устанавливает случайное положение яблока."""
        while True:
            posit_x = randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE
            posit_y = randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE
            new_posit = (posit_x, posit_y)
            if new_posit in random_positions:
                self.position = new_posit
                continue
            else:
                return new_posit

    def draw(self):
        """Отрисовка яблоко."""
        self.draw_cell(self.position, self.body_color)


def handle_keys(game_object):
    """Обработка действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основной цикл игры."""
    # Инициализация PyGame:
    pg.init()
    # Экземпляры классов.
    snake = Snake()
    apple = Apple()

    # Основную логику игры.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        snake.move()
        snake.update_direction()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position(snake.positions)
        pg.display.update()


if __name__ == '__main__':
    main()
