# Imports
import random
import time
from tkinter import *

# Variables
current_direction = [0, 20]  # We move Jack to 0px left (or right, it is horizontal movement) and 20px down
jack_still_alive = True


# Game class
class Game:

    def __init__(self):
        self.tk = Tk()  # Interface
        self.canvas = Canvas(self.tk, width=600, height=600)  # Create canvas
        self.tk.resizable(0, 0)  # We can`t change size of window
        self.tk.wm_attributes("-topmost", 1)
        self.tk.update()  # Update
        self.canvas.pack()

    def collided_with_ranges(self):

        cords_of_snakes_head = game.canvas.coords(Jack.snake_rectangles[-1])

        # Check left top x, y and right bottom x, y
        if not 0 < cords_of_snakes_head[0] < 600 \
                or not 0 < cords_of_snakes_head[1] < 600 \
                or not 0 < cords_of_snakes_head[0] + 20 < 600 \
                or not 0 < cords_of_snakes_head[1] + 20 < 600:

            return True

        else:

            return False

    def intersected_with_apple(self):
        # Get cords of apple
        cords_of_apple = game.canvas.coords(self.apple_id)

        apple_top_left_x = cords_of_apple[0]
        apple_top_left_y = cords_of_apple[1]

        # Check four peaks of apple
        if self.apple_point_in_range(apple_top_left_x, apple_top_left_y) or \
                self.apple_point_in_range(apple_top_left_x + 10, apple_top_left_y) or \
                self.apple_point_in_range(apple_top_left_x, apple_top_left_y + 10) or \
                self.apple_point_in_range(apple_top_left_x + 10, apple_top_left_y + 10):
            self.remove_apple()
            Jack.add_element_to_snake()
            self.create_apple()

    def create_apple(self):
        x1 = random.randint(1, 391)  # x1 cord
        x2 = x1 + 10  # Our apple 10*10 px
        y1 = random.randint(1, 391)
        y2 = y1 + 10
        self.apple_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")

    def remove_apple(self):
        self.canvas.delete(self.apple_id)

    def apple_point_in_range(self, apple_point_value_x, apple_point_value_y):

        # Get cords of snake`s head
        cords_of_snakes_head = game.canvas.coords(Jack.snake_rectangles[-1])

        return (cords_of_snakes_head[0] <= apple_point_value_x <= cords_of_snakes_head[2] and
                cords_of_snakes_head[1] <= apple_point_value_y <= cords_of_snakes_head[3])

    def main_loop(self):  # Main cycle of game

        while True:

            if not self.collided_with_ranges():

                Jack.move_snake()  # Move snake
                self.intersected_with_apple()
                game.tk.update()  # Update image on canvas
                time.sleep(0.5)  # Delay to more cosy play

            else:

                game.canvas.create_text(300, 300, text="GAME OVER", fill="red", font=("Century Gothic", 40))
                game.tk.update()


# Snake class
class Snake:
    snake_rectangles = []  # Here would be all snake`s elements, including head

    def __init__(self):
        # Create head and two elements
        self.snake_rectangles.append(
            game.canvas.create_rectangle(200, 200, 220, 220, fill="green"))

        self.add_element_to_snake()
        self.add_element_to_snake()

        # Link keys to functions of direction
        game.canvas.bind_all("<KeyPress-Up>", self.change_direction_up)
        game.canvas.bind_all("<KeyPress-Down>", self.change_direction_down)
        game.canvas.bind_all("<KeyPress-Left>", self.change_direction_left)
        game.canvas.bind_all("<KeyPress-Right>", self.change_direction_right)

    def move_snake(self):
        cords_of_first_snake_element = game.canvas.coords(self.snake_rectangles[-1])  # Get cords of first element
        new_cords_of_first_element = [cords_of_first_snake_element[0] + current_direction[0],
                                      cords_of_first_snake_element[1] + current_direction[1],
                                      cords_of_first_snake_element[2] + current_direction[0],
                                      cords_of_first_snake_element[3] + current_direction[1]]

        game.canvas.coords(self.snake_rectangles[0], new_cords_of_first_element)  # Move last element
        new_first_element = self.snake_rectangles.pop(0)  # Get last element

        self.snake_rectangles.insert(len(self.snake_rectangles), new_first_element)  # And insert it forward

    def add_element_to_snake(self):
        # Save cords of last element of snake
        cords_of_last_element = game.canvas.coords(self.snake_rectangles[0])

        # Make cords for new element
        x1 = cords_of_last_element[0]
        y1 = cords_of_last_element[3]
        x2 = cords_of_last_element[2]
        y2 = y1 + 20

        # Add element
        self.snake_rectangles.insert(0, game.canvas.create_rectangle(x1, y1, x2, y2, fill="green"))

    # Next four functions for changing direction list (created in line 6)
    def change_direction_up(self, event):
        current_direction[0], current_direction[1] = 0, -20

    def change_direction_down(self, event):
        current_direction[0], current_direction[1] = 0, 20

    def change_direction_left(self, event):
        current_direction[0], current_direction[1] = -20, 0

    def change_direction_right(self, event):
        current_direction[0], current_direction[1] = 20, 0


# Initializing objects
game = Game()  # Game object, need for canvas, main loop
Jack = Snake()  # Jack is our snake
game.create_apple()  # Our first apple!

# Executing methods
Jack.move_snake()  # Move Jack first time for good image
game.main_loop()  # Start main cycle of game
