from click import echo as _echo

CLEAR_LINE = "\033[K"


def echo(message, clear=True, newline=True):
    if clear:
        message = "\r" + CLEAR_LINE + message

    _echo(message, nl=newline)


def clear():
    _echo("\r" + CLEAR_LINE, nl=False)
