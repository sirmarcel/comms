from shutil import get_terminal_size
import sys


def is_terminal():
    file = sys.stdout
    if hasattr(file, "isatty"):
        return file.isatty()
    else:
        return False


def get_size():
    terminal_size = get_terminal_size()
    if is_terminal():
        if terminal_size != 0:
            return terminal_size.columns
        else:
            return 80
    else:
        return 80


tty = is_terminal()
