from typing import Final

import unicurses

from sg_pass.ui import Screen


KEY_ESCAPE: Final[int] = 27
KEY_Q: Final[int] = ord("q")


class TUI:

    def __init__(self, screen: Screen):
        self.screen = screen
        self.is_running = True

    def run(self):
        while self.is_running:
            self.screen.refresh()
            self.handle_input()

    def handle_input(self):
        key = unicurses.get_wch()

        if key in (KEY_ESCAPE, KEY_Q):
            self.is_running = False
