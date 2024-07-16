# menu.py

import curses
import textwrap
from main_window import MainWindow
from config import (
    MENU_HEIGHT,
    MENU_WIDTH,
    MENU_POS_Y,
    MENU_POS_X,
    DETAILS_HEIGHT,
    DETAILS_WIDTH,
    DETAILS_POS_Y,
    DETAILS_POS_X,
    KEY_RETURN,
)


class MenuOptions:
    """Class to handle menu options."""

    def __init__(self, options: list):
        self.options = options

    def get_options(self) -> list:
        """Return the list of options."""
        return self.options

    def get_num_options(self) -> int:
        """Return the number of options."""
        return len(self.options)


class DetailsWindow:
    """Class to handle the details window display."""

    def __init__(self):
        self.window = curses.newwin(
            DETAILS_HEIGHT, DETAILS_WIDTH, DETAILS_POS_Y, DETAILS_POS_X
        )

    def display_details(self, description: str):
        """Display the details for the highlighted menu option."""
        self.window.clear()
        self._draw_box()
        wrapped_description = textwrap.wrap(description, DETAILS_WIDTH - 3)
        self.window.addstr(1, 2, "Details:")
        y_pos = 3
        for line in wrapped_description:
            self.window.addstr(y_pos, 2, line)
            y_pos += 1
        self.window.refresh()

    def _draw_box(self):
        """Helper method to draw a box with a title line."""
        _, width = self.window.getmaxyx()
        self.window.box()
        self.window.addch(2, 0, curses.ACS_LTEE)
        self.window.hline(2, 1, curses.ACS_HLINE, width - 2)
        self.window.addch(2, width - 1, curses.ACS_RTEE)


class Menu:
    """Class to handle the menu display and interaction."""

    def __init__(
        self,
        scr: curses.window,
        name: str,
        options: MenuOptions,
        descriptions: list,
        primary_filename: str,
        secondary_filename: str,
    ):
        self.name = name
        self.scr = scr
        self.height = MENU_HEIGHT
        self.width = MENU_WIDTH
        self.y_pos = MENU_POS_Y
        self.x_pos = MENU_POS_X
        self.highlight = 1
        self.options = options.get_options()
        self.num_options = options.get_num_options()
        self.descriptions = descriptions
        self.window = curses.newwin(self.height, self.width, self.y_pos, self.x_pos)
        self.window.keypad(True)
        self.details_window = DetailsWindow()
        self.main_window = MainWindow(primary_filename, secondary_filename)

    def _print_selection(self, selection):
        self.scr.addstr(
            curses.LINES - 2, 2, f"Selection: {self.options[selection - 1]}"
        )
        self.scr.clrtoeol()
        self.scr.refresh()
        curses.napms(2000)

    def display_instructions(self):
        """Display instructions for menu navigation."""
        self.scr.addstr(curses.LINES - 2, 2, "Use arrow keys to navigate up and down. ")
        self.scr.addstr("Press enter to make a selection.")
        self.scr.refresh()

    def print_menu(self):
        """Print the menu options."""
        y_pos = 3
        x_pos = 2
        self._draw_box(self.name)
        for index, option in enumerate(self.options, 1):
            if self.highlight == index:  # Highlight the current option
                self.window.addstr(y_pos, x_pos, option, curses.A_REVERSE)
            else:
                self.window.addstr(y_pos, x_pos, option)
            y_pos += 1
        self.window.refresh()  # Draw the menu
        self.print_details()

    def _draw_box(self, title: str = ""):
        """Helper method to draw a box with an optional title."""
        _, width = self.window.getmaxyx()
        self.window.box()
        if title:
            self.window.addstr(1, 2, title)
        self.window.addch(2, 0, curses.ACS_LTEE)
        self.window.hline(2, 1, curses.ACS_HLINE, width - 2)
        self.window.addch(2, width - 1, curses.ACS_RTEE)

    def print_details(self):
        """Print the details for the highlighted menu option."""
        description = self.descriptions[self.highlight - 1]
        self.details_window.display_details(description)

    def navigate_menu(self) -> int:
        """Navigate through the menu and return the selected option."""
        first_item = 1
        last_item = self.num_options
        selection = 0
        current = self.window.getch()

        if current == curses.KEY_UP:
            if self.highlight == first_item:
                self.highlight = last_item
            else:
                self.highlight -= 1
        elif current == curses.KEY_DOWN:
            if self.highlight == last_item:
                self.highlight = first_item
            else:
                self.highlight += 1
        elif current in (KEY_RETURN, curses.KEY_ENTER):
            selection = self.highlight

        return selection
