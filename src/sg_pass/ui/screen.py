from __future__ import annotations

import unicurses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ctypes import c_void_p
    from typing import Tuple

    UnicursesScreen = c_void_p


class Screen:

    def __init__(self):
        self.__screen = self.__setup_screen()
        x = unicurses.getmaxyx(self.__screen)
        self.__width, self.__height = x

    def __enter__(self) -> Screen:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        unicurses.endwin()

    @staticmethod
    def __setup_screen() -> UnicursesScreen:
        screen = unicurses.initscr()

        unicurses.start_color()
        unicurses.cbreak()
        unicurses.noecho()

        unicurses.curs_set(0)
        unicurses.mouseinterval(0)
        unicurses.mousemask(unicurses.ALL_MOUSE_EVENTS)

        unicurses.keypad(screen, True)
        unicurses.refresh()
        return screen

    @staticmethod
    def refresh():
        unicurses.refresh()

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    def update_size(self):
        size: Tuple[int, int] = unicurses.getmaxyx(self.__screen)
        self.__width, self.__height = size
