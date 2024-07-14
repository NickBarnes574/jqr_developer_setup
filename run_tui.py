#!/usr/bin/env python3

import curses
import textwrap

# Big Window Constants
BIG_WINDOW_HEIGHT = 13
BIG_WINDOW_WIDTH = 78
BIG_WINDOW_POS_Y = 0
BIG_WINDOW_POS_X = 1

# Menu Constants
MENU_HEIGHT = 9
MENU_WIDTH = 30
MENU_POS_Y = 13
MENU_POS_X = 1

# Details Constants
DETAILS_HEIGHT = MENU_HEIGHT
DETAILS_WIDTH = 47
DETAILS_POS_Y = MENU_POS_Y
DETAILS_POS_X = MENU_POS_X + MENU_WIDTH + 1

KEY_RETURN = 10

OPTIONS = [
    "Basic Installation",
    "Custom Installation",
    "Update Tools",
    "Advanced Options",
    "Exit",
]
DESCRIPTIONS = [
    "Perform a basic installation with default settings.",
    "Customize installation settings to your preference.",
    "Update existing tools to the latest versions.",
    "Access advanced configuration options and settings.",
    "Exit the installation manager.",
]


def configure_curses():
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)


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


class BigWindow:
    """Class to handle the big window display."""

    def __init__(
        self, scr: curses.window, height: int, width: int, y_pos: int, x_pos: int
    ):
        self.scr = scr
        self.height = height
        self.width = width
        self.y_pos = y_pos
        self.x_pos = x_pos
        self.window = curses.newwin(height, width, y_pos, x_pos)

    def display_title(self):
        self.window.clear()
        self.window.box()
        title_lines = ""
        subtext_lines = ""
        with open("title.txt", "r") as file:
            title_lines = file.readlines()

        # Display the title
        title_y_pos = 1
        for line in title_lines:
            self.window.addstr(title_y_pos, 2, line.rstrip(), curses.color_pair(1))
            title_y_pos += 1

        with open("subtext.txt", "r") as file:
            subtext_lines = file.readlines()

        # Display the subtext
        subtext_y_pos = len(title_lines) + 1
        for line in subtext_lines:
            self.window.addstr(subtext_y_pos, 2, line.rstrip())
            subtext_y_pos += 1
        self.window.refresh()


class DetailsWindow:
    """Class to handle the details window display."""

    def __init__(self, height: int, width: int, y_pos: int, x_pos: int):
        self.window = curses.newwin(height, width, y_pos, x_pos)

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
        height: int,
        width: int,
        y_pos: int,
        x_pos: int,
        options: MenuOptions,
        descriptions: list,
    ):
        self.name = name
        self.scr = scr
        self.height = height
        self.width = width
        self.y_pos = y_pos
        self.x_pos = x_pos
        self.highlight = 1
        self.options = options.get_options()
        self.num_options = options.get_num_options()
        self.descriptions = descriptions
        self.window = curses.newwin(self.height, self.width, self.y_pos, self.x_pos)
        self.window.keypad(True)
        self.details_window = DetailsWindow(
            DETAILS_HEIGHT, DETAILS_WIDTH, DETAILS_POS_Y, DETAILS_POS_X
        )

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

    def run_event_loop(self):
        """Run the event loop for menu interaction."""
        while True:
            self.print_menu()
            selection = self.navigate_menu()
            if selection != 0:
                self._print_selection(selection)
                break
            self.scr.refresh()


def main(stdscr: curses.window):
    """Main function to initialize and run the menu."""
    configure_curses()
    stdscr.clear()
    stdscr.refresh()
    big_window = BigWindow(
        stdscr, BIG_WINDOW_HEIGHT, BIG_WINDOW_WIDTH, BIG_WINDOW_POS_Y, BIG_WINDOW_POS_X
    )
    big_window.display_title()
    options_instance = MenuOptions(OPTIONS)
    menu = Menu(
        stdscr,
        "Main Menu",
        MENU_HEIGHT,
        MENU_WIDTH,
        MENU_POS_Y,
        MENU_POS_X,
        options_instance,
        DESCRIPTIONS,
    )
    menu.display_instructions()
    menu.run_event_loop()


if __name__ == "__main__":
    curses.wrapper(main)
