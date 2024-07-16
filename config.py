# config.py

import curses

# Main Window Constants
MAIN_WINDOW_HEIGHT = 13
MAIN_WINDOW_WIDTH = 78
MAIN_WINDOW_POS_Y = 0
MAIN_WINDOW_POS_X = 1

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

MAIN_MENU_OPTIONS = [
    "Basic Installation",
    "Custom Installation",
    "Update Tools",
    "Advanced Options",
    "Exit",
]
MAIN_MENU_DESCRIPTIONS = [
    "Perform a basic installation with default settings.",
    "Customize installation settings to your preference.",
    "Update existing tools to the latest versions.",
    "Access advanced configuration options and settings.",
    "Exit the installation manager.",
]

BASIC_INSTALLATION_OPTIONS = ["Install", "Go Back"]
BASIC_INSTALLATION_DESCRIPTIONS = [
    "Start the basic installation process.",
    "Return to the main menu.",
]


def configure_curses():
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
