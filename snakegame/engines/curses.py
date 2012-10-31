from __future__ import absolute_import

import curses
from functools import wraps
import time

from snakegame import common
from snakegame.engines import Engine

class CursesEngine(Engine):
    def new_game(self, *args):
        super(CursesEngine, self).new_game(*args)

        self.window = curses.initscr()
        curses.start_color()

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

        self.EMPTY_COLOUR = curses.color_pair(0)
        self.APPLE_COLOUR = curses.color_pair(1)
        self.SNAKE_COLOUR = curses.color_pair(4)

    def draw_board(self):
        # Draw grid.
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                char = '.'
                colour = self.EMPTY_COLOUR

                # Draw the things on the square.
                if cell == common.APPLE:
                    char = '@'
                    colour = self.APPLE_COLOUR

                elif cell.isalpha(): # Snake...
#                    colour = self.bots[cell.lower()][1]
                    char = cell
                    colour = self.SNAKE_COLOUR

                self.window.addstr(y, x, char, colour)

    def run(self):
        while self.bots:
            # Clear the screen.
            self.window.erase()

            # Draw the board.
            self.draw_board()

            # Update the display.
            self.window.refresh()
            time.sleep(0.025)

            # Let the snakes move!
            self.update_snakes()

