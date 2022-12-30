import unicurses


class Screen:

    def __init__(self):
        self.__screen = unicurses.initscr()

        unicurses.start_color()
        unicurses.cbreak()
        unicurses.noecho()

        unicurses.curs_set(0)
        unicurses.mouseinterval(0)
        unicurses.mousemask(unicurses.ALL_MOUSE_EVENTS)

        unicurses.keypad(self.__screen, True)
        unicurses.refresh()

    def __enter__(self):
        return self

    @staticmethod
    def refresh():
        unicurses.refresh()

    def __exit__(self, exc_type, exc_val, exc_tb):
        unicurses.endwin()
