from sg_pass import __version__
from sg_pass.ui import Screen, TUI


def main():
    print(f"Running SgPass v{__version__}")

    with Screen() as screen:
        ui = TUI(screen)
        ui.run()


if __name__ == '__main__':
    main()
