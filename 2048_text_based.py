#!/usr/bin/python3

"""
Clone of 2048 game.
"""

import random

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# User inputs
MOVE_INPUTS = {'W': UP,
                'A': LEFT,
                'S': DOWN,
                'D': RIGHT}

# Offsets for computing tile indices in each direction.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        Initialize the TwentyFortyEight board
        """

        self._grid_height = grid_height
        self._grid_width = grid_width
        self._grid = [[(row,col) for col in range(self.get_grid_width())]
                      for row in range(self.get_grid_height())]

        self._initial = {UP: [(0,col) for col in range(self.get_grid_width())],
                        DOWN: [(self.get_grid_height()-1,col) for col in range(self.get_grid_width())],
                        LEFT: [(row,0) for row in range(self.get_grid_height())],
                        RIGHT: [(row,self.get_grid_width()-1) for row in range(self.get_grid_height())]}

        self.reset()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        width = len(str(max([cell for row in self._grid for cell in row])))
        return '\n'.join(['  '.join([str(cell).ljust(width,' ') for cell in row]) for row in self._grid])

    def get_grid_height(self):
        """
        Get the height of the board.
        """

        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """

        return self._grid_width

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """

        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """

        return self._grid[row][col]

    def is_full(self):
        """
        Helper function for new_tile()
        Returns False if there are any empty tiles
        Otherwise, returns True if no tiles are empty
        """

        if any([any([self.get_tile(row,col) == 0 for col in range(self.get_grid_width())])
                                                 for row in range(self.get_grid_height())]):
            return False
        else:
            return True

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """

        # If grid has no empty cells, returns False and exits mehtod
        if self.is_full():
            return False

        # Selects random indices until empty cell found
        while True:
            row = random.randrange(self.get_grid_height())
            col = random.randrange(self.get_grid_width())
            if self._grid[row][col] == 0:
                break

        # Sets cell value to 2 %90 of the time, 4 10% of the time
        if random.randrange(10) < 9:
            self._grid[row][col] = 2
        else:
            self._grid[row][col] = 4

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """

        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                self.set_tile(row,col,0)

        for dummy_num in range(2):
            self.new_tile()

    def get_line(self, start_cell, direction):
        """
        Helper function for move()
        Returns list of cell values given starting cell and direction
        """

        if direction == UP or direction == DOWN:
            steps = self._grid_height
        elif direction == LEFT or direction == RIGHT:
            steps = self._grid_width

        line = []
        for step in range(steps):
            row = start_cell[0] + step * OFFSETS[direction][0]
            col = start_cell[1] + step * OFFSETS[direction][1]
            line.append(self.get_tile(row,col))
        return line

    def set_line(self, start_cell, direction, line):
        """
        Helper function for move()
        Sets cell values for starting cell and direction given line as list
        """

        for step in range(len(line)):
            row = start_cell[0] + step * OFFSETS[direction][0]
            col = start_cell[1] + step * OFFSETS[direction][1]
            self.set_tile(row,col,line[step])

    def shift(self, line):
        """
        Helper function for merge() that shifts non-zero numbers to side
        """

        temp = [0 for dummy_placeholder in range(len(line))]

        index = 0
        for number in line:
            if number > 0:
                temp[index] = number
                index += 1

        return temp

    def merge(self, line):
        """
        Helper function for move() that merges a single row or column in 2048
        """

        temp = self.shift(line)

        for index in range(len(temp)-1):
            if temp[index] > 0 and temp[index] == temp[index+1]:
                temp[index] *=2
                temp[index+1] = 0

        result = self.shift(temp)

        return result

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """

        changes = []

        for start_cell in self._initial[direction]:
            line_temp = self.get_line(start_cell, direction)
            line_new = self.merge(line_temp)
            if line_temp != line_new:
                self.set_line(start_cell, direction, line_new)
                changes.append(True)

        if any(changes):
            self.new_tile()

def process_user_input(board,user_input):
    """
    Takes input from user
    """

    if user_input not in ['W','A','S','D']:
        if user_input == 'N':
            print("\nNew Game:")
            board.reset()
            return board
        elif user_input == 'Q':
            quit()
        else:
            user_input = input("\nInvalid input, please enter one of the letters of WASD: ").upper()
            board = process_user_input(board,user_input)
            return board
    else:
        board.move(MOVE_INPUTS[user_input])
        return board


print("\nWelcome to 2048!")
print("\n(At any time, type N to start a New Game or Q to Quit)")

board = TwentyFortyEight(4, 4)

while True:
    print("\n" + str(board))
    user_input = input("\nEnter move (WASD): ").upper()
    board = process_user_input(board,user_input)
