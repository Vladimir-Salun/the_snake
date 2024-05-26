"""Учебный проект Змейка."""
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION: tuple = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP: tuple = (0, -1)
DOWN: tuple = (0, 1)
LEFT: tuple = (-1, 0)
RIGHT: tuple = (1, 0)

# Цвет объекта по умолчанию
DEFAULT_COLOR: tuple = (255, 255, 255)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: tuple = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: tuple = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: tuple = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: tuple = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс."""

    def __init__(self, position=(0, 0), body_color=DEFAULT_COLOR):
        """Инициализация игрового объекта."""
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position):
        """Метод для отрисовки ячейки."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def erase_cell(self, last):
        """Затирание последнего сегмента."""
        if last:
            last_rect = pygame.Rect(last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def draw(self) -> None:
        """Абстрактный метод."""
        raise NotImplementedError(
            'Метот draw() должен быть переопределен в дочерних классах'
        )


class Snake(GameObject):
    """Дочерний класс, описывающий змейку и её поведение."""

    def __init__(self) -> None:
        """Инициализация змейки."""
        super().__init__(position=(0, 0), body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Обновляет движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        position_x, position_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_x = (position_x + direction_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (position_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        next_position = (new_x, new_y)
        self.positions.insert(0, next_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на игровой поверхности."""
        head = self.get_head_position()
        self.draw_cell(head)
        self.erase_cell(self.last)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Перезапуск игры."""
        self.length = 1
        self.speed = SPEED
        self.position = CENTER_POSITION
        self.positions = [self.position]
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.direction = RIGHT
        self.next_direction = None


class Apple(GameObject):
    """Дочерний класс, описывающий яблоко и действия с ним."""

    def __init__(self, snake_positions=None):
        """Инициализация яблока."""
        super().__init__(position=(0, 0), body_color=APPLE_COLOR)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Устанавливает случайное положение яблока."""
        snake_positions = snake_positions or [CENTER_POSITION]
        self.position = snake_positions[0]
        while self.position in snake_positions:
            posit_x = randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE
            posit_y = randint(0, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE
            self.position = (posit_x, posit_y)

    def draw(self):
        """Отрисовка яблоко."""
        self.draw_cell(self.position)


def handle_keys(game_object) -> None:
    """Обработка действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основной цикл игры."""
    # Инициализация PyGame:
    pygame.init()
    # Экземпляры классов.
    snake = Snake()
    apple = Apple(snake.position)
    # Основную логику игры.
    apple.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        snake.move()
        snake.update_direction()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
            apple.draw()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
