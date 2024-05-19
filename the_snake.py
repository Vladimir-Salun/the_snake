from random import choice, randrange

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

DEFAULT_COLOR = (100, 100, 100)
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

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
        self, position=(SCREEN_WIDTH // 2,
                        SCREEN_HEIGHT // 2),
        body_color=DEFAULT_COLOR
    ):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, surface, x, y):
        """Отрисовывает ячейку
        на указанной поверхности с заданными координатами.
        """
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def clear_cell(self, surface, x, y):
        """Очищает ячейку на указанной поверхности
        с заданными координатами.
        """
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)

    def draw(self):
        """
        Абстрактный метод, который
        переопределяется в дочерних классах
        """
        pass


class Snake(GameObject):
    """Дочерний класс, представляющий змейку."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        """Перемещает змейку на один шаг в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_x = (head_x + dx) % GRID_WIDTH
        new_head_y = (head_y + dy) % GRID_HEIGHT
        new_head = (new_head_x, new_head_y)

        # Проверка столкновения с телом змейки, исключая голову
        if new_head in self.positions[1:]:
            self.reset()
        elif new_head == (
            apple.position[0] // GRID_SIZE,
            apple.position[1] // GRID_SIZE
        ):
            self.last = None
            self.length += 1
            apple.randomize_position()
            self.positions.insert(0, new_head)
        else:
            self.last = self.positions.pop()
            self.positions.insert(0, new_head)

    def draw(self, surface):
        """Отрисовывает змейку на указанной поверхности."""
        for position in self.positions[:-1]:
            self.draw_cell(surface, position[0], position[1])

        """Отрисовка головы змейки."""

        head_x, head_y = self.positions[0]
        self.draw_cell(surface, head_x, head_y)

        if self.last:
            self.clear_cell(surface, self.last[0], self.last[1])

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки к начальному."""
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

        # Заполнение фона
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс Apple, наследуется от класса GameObject"""

    def __init__(self):
        """иницилизация яблока"""
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """устанавливает случайное положение яблока"""
        posit_x = randrange(0, SCREEN_WIDTH, 20)
        posit_y = randrange(0, SCREEN_HEIGHT, 20)
        self.position = posit_x, posit_y
        return (posit_x, posit_y)

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    # Инициализация PyGame
    pygame.init()

    # Создание экрана
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Создание экземпляров классов
    snake = Snake()
    apple = Apple()

    # Создание объекта Clock
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
