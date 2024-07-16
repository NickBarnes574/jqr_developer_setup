# main_window.py

import curses
from config import (
    MAIN_WINDOW_HEIGHT,
    MAIN_WINDOW_WIDTH,
    MAIN_WINDOW_POS_Y,
    MAIN_WINDOW_POS_X,
)


class MainWindow:
    """Class to handle the main window display."""

    def __init__(self, primary_filename: str, secondary_filename: str):
        self.height = MAIN_WINDOW_HEIGHT
        self.width = MAIN_WINDOW_WIDTH
        self.y_pos = MAIN_WINDOW_POS_Y
        self.x_pos = MAIN_WINDOW_POS_X
        self.primary_filename = primary_filename
        self.secondary_filename = secondary_filename
        self.window = curses.newwin(self.height, self.width, self.y_pos, self.x_pos)

    def display(self):
        self.window.clear()
        self.window.box()
        primary_filename_lines = ""
        secondary_filename_lines = ""
        with open(self.primary_filename, "r") as file:
            primary_filename_lines = file.readlines()

        # Display the primary file contents
        primary_filename_y_pos = 1
        for line in primary_filename_lines:
            self.window.addstr(
                primary_filename_y_pos, 2, line.rstrip(), curses.color_pair(1)
            )
            primary_filename_y_pos += 1

        with open(self.secondary_filename, "r") as file:
            secondary_filename_lines = file.readlines()

        # Display the secondary file contents
        secondary_filename_y_pos = len(primary_filename_lines) + 1
        for line in secondary_filename_lines:
            self.window.addstr(secondary_filename_y_pos, 2, line.rstrip())
            secondary_filename_y_pos += 1
        self.window.refresh()
