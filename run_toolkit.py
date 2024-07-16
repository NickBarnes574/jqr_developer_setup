#!/usr/bin/env python3

# run_toolkit.py

import curses
from event_handler import EventHandler
from config import configure_curses


def main(stdscr: curses.window):
    """Main function to initialize and run the menu."""
    configure_curses()
    stdscr.clear()
    stdscr.refresh()
    event_handler = EventHandler(stdscr)
    event_handler.run_main_menu()


if __name__ == "__main__":
    curses.wrapper(main)
