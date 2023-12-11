import pygame
import random

# Khởi tạo màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Khởi tạo kích thước cửa sổ
window_width = 800
window_height = 600

# Khởi tạo kích thước ô và số lượng ô
cell_size = 20
grid_width = window_width // cell_size
grid_height = window_height // cell_size

# Khởi tạo tốc độ di chuyển của rắn
snake_speed = 10

class SnakeGame:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()

        self.font_style = pygame.font.SysFont(None, 50)
        self.score_font = pygame.font.SysFont(None, 35)

        self.reset()

    def reset(self):
        self.game_over = False

        # Khởi tạo vị trí ban đầu của rắn và mồi
        self.snake_head = [grid_width // 2, grid_height // 2]
        self.snake_body = [[grid_width // 2, grid_height // 2], [grid_width // 2, grid_height // 2], [grid_width // 2, grid_height // 2]]
        self.direction = "RIGHT"

        self.food_pos = self.generate_food()

        self.score = 0

    def generate_food(self):
        # Tạo vị trí ngẫu nhiên cho mồi
        food_pos = [random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)]
        while food_pos in self.snake_body:
            food_pos = [random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)]
        return food_pos

    def show_score(self):
        score_text = self.score_font.render("Score: " + str(self.score), True, WHITE)
        self.window.blit(score_text, [10, 10])

    def game_over_message(self):
        game_over_text = self.font_style.render("May choi ngu vl", True, WHITE)
        self.window.blit(game_over_text, [window_width // 2 - 100, window_height // 2 - 50])

    def draw_snake(self):
        for body_part in self.snake_body:
            pygame.draw.rect(self.window, GREEN, (body_part[0] * cell_size, body_part[1] * cell_size, cell_size, cell_size))

    def play(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.direction = "RIGHT"
                    elif event.key == pygame.K_UP and self.direction != "DOWN":
                        self.direction = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.direction = "DOWN"

            # Di chuyển rắn
            if self.direction == "LEFT":
                self.snake_head[0] -= 1
            elif self.direction == "RIGHT":
                self.snake_head[0] += 1
            elif self.direction == "UP":
                self.snake_head[1] -= 1
            elif self.direction == "DOWN":
                self.snake_head[1] += 1

            # Kiểm tra va chạm với tường hoặc với cơ thể của rắn
            if self.snake_head[0] < 0 or self.snake_head[0] >= grid_width or self.snake_head[1] < 0 or self.snake_head[1] >= grid_height or self.snake_head in self.snake_body[1:]:
                self.game_over = True

            self.snake_body.insert(0, list(self.snake_head))

            # Kiểm tra va chạm với mồi
            if self.snake_head == self.food_pos:
                self.score += 1
                self.food_pos = self.generate_food()
            else:
                self.snake_body.pop()

            self.window.fill(BLACK)

            self.draw_snake()
            pygame.draw.rect(self.window, RED, (self.food_pos[0] * cell_size, self.food_pos[1] * cell_size, cell_size, cell_size))

            self.show_score()

            pygame.display.update()

            self.clock.tick(snake_speed)

        self.game_over_message()

        pygame.display.update()

        # Chờ người chơi nhấn phím để chơi lại
        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.reset()
                        self.play()

# Khởi tạo game và chạy
game = SnakeGame()
game.play()