from random import choice, randint

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


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        self.position = (0, 0)
        self.body_color = DEFAULT_COLOR

    def draw(self, surface):
        """
        Абстрактный метод,
        который предназначен для переопределения в дочерних классах.
        """
        pass


class Snake(GameObject):
    """Дочерний класс, представляющий змейку."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        """Перемещает змейку на один шаг в текущем направлении."""
        head_x, head_y = self.positions[0]
        new_head_x = (head_x + self.direction[0]) % GRID_WIDTH
        new_head_y = (head_y + self.direction[1]) % GRID_HEIGHT
        new_head = (new_head_x, new_head_y)

        apple_x, apple_y = apple.position

        if new_head in self.positions[2:]:
            self.reset()
        elif new_head == (apple_x // GRID_SIZE, apple_y // GRID_SIZE):
            self.last = None
            self.length += 1
            apple.randomize_position()
            self.positions.insert(0, new_head)
        else:
            self.last = self.positions.pop()
            self.positions.insert(0, new_head)

            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на указанной поверхности."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        """Отрисовка головы змейки."""

        head_rect = pygame.Rect(
            self.positions[0][0] * GRID_SIZE,
            self.positions[0][1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                self.last[0] * GRID_SIZE,
                self.last[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

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


class Apple(GameObject):
    """Дочерний класс, представляющий яблоко."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

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

    # Создание экземпляров классов
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
