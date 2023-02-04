import itertools
import threading
import time

from .terminal import tty
from .echo import echo, clear
from .timer import Timer

# with many thanks to the ase-bar
sequences = itertools.cycle(["⬒⬔◨◪⬓⬕◧◩", "⬖⬘⬗⬙", "⊙⦾⦿⊛⎊✪⬤◌ ", "𐬼𐬽", "◢◣◤◥"])


class Animation:
    def __init__(self):
        self.sequence = itertools.cycle(list(next(sequences)))

    def __next__(self):
        return next(self.sequence)


class Animated:
    """base for spinner and ticker"""

    def __init__(self, message, formatter, delay=0.1):
        super().__init__()
        self.message = message
        self.formatter = formatter
        self.delay = delay
        self.animation = Animation()

    def frame(self):
        msg = self.formatter(self.message, indicator=next(self.animation))
        echo(msg, newline=False)


class Spinner(Animated):
    """
    Display an animation while waiting for long-running task.

    Distantly inspired by:
        https://stackoverflow.com/a/39504463/5172579
        and by halo
    """

    def __init__(self, message, formatter, delay=0.1):
        super().__init__(message, formatter, delay=delay)

        self.start()

    def start(self):
        if tty:
            self.running = True
            self.thread = threading.Thread(target=self.spin_task, daemon=True).start()

    def spin_task(self):
        while self.running:
            self.frame()
            time.sleep(self.delay)

    def stop(self):
        if tty:
            self.running = False
            if self.thread is not None:
                self.thread.join(timeout=0)
            clear()


class Ticker(Animated):
    """Display animation while running many fast tasks"""

    def __init__(self, message, formatter, delay=0.1):
        super().__init__(message, formatter, delay=delay)

        self.timer = None

    def __call__(self, message):
        """call every time a task starts/ends"""
        if tty:
            if self.timer is None:
                self.timer = Timer()
                duration = 0.0
            else:
                duration = self.timer()

            if duration > self.delay:
                self.message = message
                self.timer.reset()
                self.frame()
