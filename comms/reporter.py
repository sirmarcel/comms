from .spinner import Spinner, Ticker
from .timer import Timer


class Reporter:
    """Reporter for command line feedback"""

    def __init__(self, comms, verbose=True, silent=False):
        self.comms = comms

        self.silent = silent  # say absolutely nothing
        if silent:
            verbose = True

        self.log_steps = verbose  # should we log every step

        self.current_task = None
        self.current_step = None

        self.timer_task = None
        self.timer_step = None

        self.ticker = None
        self.spinner = None

    def start(self, task):
        self.done()

        if task is not None and not self.silent:
            self.current_task = task
            self.timer_task = Timer()
            self.comms.task(f"start {self.current_task} ...")

    def done(self, message=None):
        self.finish_step()
        if self.current_task is not None:
            if message is None:
                message = f"done {self.current_task}!"

            self.comms.task(message, done=True, suffix=f"{self.timer_task():.3f}s")
            self.current_task = None

    def step(self, step, spin=True):
        self.finish_step()

        if step is not None and not self.silent:
            self.current_step = step
            self.timer_step = Timer()
            if spin:
                self.spinner = Spinner(self.current_step, self.comms.step_formatter)
                self.ticker = None
            else:
                self.spinner = None
                self.ticker = Ticker(self.current_step, self.comms.step_formatter)

    def finish_step(self):
        if self.spinner is not None:
            self.spinner.stop()
            self.spinner = None
        if self.ticker is not None:
            self.ticker = None

        if self.current_step is not None and self.log_steps:
            self.comms.step(
                f"{self.current_step}", done=True, suffix=f"{self.timer_step():.3f}s"
            )

        self.current_step = None

    def tick(self, message):
        if self.ticker is not None:
            self.ticker(f"{self.current_step} {message}")
