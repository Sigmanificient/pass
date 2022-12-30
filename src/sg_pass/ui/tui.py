from __future__ import annotations
from typing import TYPE_CHECKING

import unicurses

if TYPE_CHECKING:
    from sg_pass.ui import Screen
    from typing import Final


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
            return

        if key == unicurses.KEY_RESIZE:
            unicurses.resize_term(0, 0)
            self.screen.update_size()
            return
