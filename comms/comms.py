from functools import partial

from .echo import echo
from .message import message
from .reporter import Reporter

indent_step = ".. "
icon_done = "✓"


class Comms:
    def __init__(self, prefix="comms"):
        self.prefix = prefix

    def talk(self, msg, full=False):
        echo(message(msg, prefix=self.prefix, indent="-> ", truncate_message=(not full)))

    def warn(self, msg, level=None, full=True):
        echo(
            message(
                msg,
                style_message={"fg": "red", "bold": True},
                prefix=self.prefix,
                indent="** ",
                truncate_message=(not full),
            )
        )

    def announce(self, msg, full=False):
        echo(
            message(
                msg,
                prefix=self.prefix,
                style_message={"bold": True},
                truncate_message=(not full),
            )
        )
        echo("")

    def task(self, msg, done=False, **kwargs):
        echo(self.task_formatter(msg, done=done, **kwargs))

    def step(self, msg, done=False, **kwargs):
        echo(self.step_formatter(msg, done=done, **kwargs))

    def task_formatter(self, msg, done=False, **kwargs):
        style = {
            **kwargs,
            "indent": 0,
            "prefix": self.prefix,
            "style_message": {"bold": True},
        }

        if done:
            style["indicator"] = icon_done

        return message(msg, **style)

    def step_formatter(self, msg, done=False, **kwargs):
        style = {
            **kwargs,
            "indent": indent_step,
            "prefix": self.prefix,
        }

        if done:
            style["indicator"] = icon_done

        return message(msg, **style)

    def reporter(self, silent=False, verbose=True):
        return Reporter(self, silent=silent, verbose=verbose)


comms = Comms()
