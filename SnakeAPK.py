import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.core.window import Window
import random

kivy.require('1.11.1')

# Khởi tạo màu sắc
GREEN = (0, 1, 0, 1)
RED = (1, 0, 0, 1)

# Khởi tạo kích thước cửa sổ
cell_size = 20
grid_width = Window.width // cell_size
grid_height = Window.height // cell_size

# Khởi tạo tốc độ di chuyển của rắn
snake_speed = 0.1

class SnakeGame(App):
    def build(self):
        self.game_over = False
        self.snake_head = [grid_width // 2, grid_height // 2]
        self.snake_body = [[grid_width // 2, grid_height // 2], [grid_width // 2, grid_height // 2], [grid_width // 2, grid_height // 2]]
        self.direction = "right"
        self.food_pos = self.generate_food()
        self.score = 0

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.create_canvas())
        layout.add_widget(Button(text="Start", on_press=self.start_game))
        return layout

    def create_canvas(self):
        self.canvas_widget = Widget()
        with self.canvas_widget.canvas:
            self.rectangles = []

        Clock.schedule_interval(self.update, snake_speed)
        return self.canvas_widget

    def draw_snake(self):
        for rect in self.rectangles:
            self.canvas_widget.canvas.remove(rect)

        self.rectangles.clear()

        for body_part in self.snake_body:
            x, y = body_part[0] * cell_size, body_part[1] * cell_size
            rectangle = Rectangle(pos=(x, y), size=(cell_size, cell_size))
            self.rectangles.append(rectangle)
            self.canvas_widget.canvas.add(rectangle)

    def generate_food(self):
        # Tạo vị trí ngẫu nhiên cho mồi
        food_pos = [random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)]
        while food_pos in self.snake_body:
            food_pos = [random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)]
        return food_pos

    def start_game(self, instance):
        self.game_over = False
        self.snake_head = [grid_width // 2, grid_height // 2]
        self.snake_body = [[grid_width // 2, grid_height // 2], [grid_width // 2, grid_height // 2], [grid_width // 2, grid_height // 2]]
        self.direction = "right"
        self.food_pos = self.generate_food()
        self.score = 0
        Clock.schedule_interval(self.update, snake_speed)

    def update(self, dt):
        if not self.game_over:
            if self.direction == "right":
                self.snake_head[0] += 1
            elif self.direction == "left":
                self.snake_head[0] -= 1
            elif self.direction == "up":
                self.snake_head[1] += 1
            elif self.direction == "down":
                self.snake_head[1] -= 1

            if self.snake_head[0] < 0 or self.snake_head[0] >= grid_width or self.snake_head[1] < 0 or self.snake_head[1] >= grid_height or self.snake_head in self.snake_body[1:]:
                self.game_over = True

            self.snake_body.insert(0, list(self.snake_head))

            if self.snake_head == self.food_pos:
                self.score += 1
                self.food_pos = self.generate_food()
            else:
                self.snake_body.pop()

            self.draw_snake()

    def on_key_down(self, key, modifiers):
        if key[1] == 'left' and self.direction != "right":
            self.direction = "left"
        elif key[1] == 'right' and self.direction != "left":
            self.direction = "right"
        elif key[1] == 'up' and self.direction != "down":
            self.direction = "up"
        elif key[1] == 'down' and self.direction != "up":
            self.direction = "down"

    def on_stop(self):
        Clock.unschedule(self.update)

if __name__ == '__main__':
    SnakeGame().run()
