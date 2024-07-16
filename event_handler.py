# event_handler.py

import curses
from menu import Menu, MenuOptions
from config import (
    MAIN_MENU_OPTIONS,
    MAIN_MENU_DESCRIPTIONS,
    BASIC_INSTALLATION_OPTIONS,
    BASIC_INSTALLATION_DESCRIPTIONS,
    KEY_RETURN,
)


class EventHandler:
    """Class to handle menu events and transitions."""

    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr

    def run_main_menu(self):
        options_instance = MenuOptions(MAIN_MENU_OPTIONS)
        menu = Menu(
            self.stdscr,
            "Main Menu",
            options_instance,
            MAIN_MENU_DESCRIPTIONS,
            "0_main_menu/title.txt",
            "0_main_menu/subtext.txt",
        )
        menu.main_window.display()
        menu.display_instructions()
        self.run_event_loop(menu)

    def run_basic_installation_menu(self):
        options_instance = MenuOptions(BASIC_INSTALLATION_OPTIONS)
        menu = Menu(
            self.stdscr,
            "Basic Installation",
            options_instance,
            BASIC_INSTALLATION_DESCRIPTIONS,
            "1_basic_installation/basic_primary.txt",
            "1_basic_installation/basic_secondary.txt",
        )
        menu.main_window.display()
        menu.display_instructions()
        self.run_event_loop(menu)

    def run_event_loop(self, menu: Menu):
        while True:
            menu.print_menu()
            selection = menu.navigate_menu()
            if selection != 0:
                if menu.options[selection - 1] == "Basic Installation":
                    self.run_basic_installation_menu()
                elif menu.options[selection - 1] == "Go Back":
                    self.run_main_menu()
                elif menu.options[selection - 1] == "Exit":
                    return
                else:
                    menu._print_selection(selection)
                break
            self.stdscr.refresh()
