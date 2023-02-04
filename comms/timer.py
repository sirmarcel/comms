import time


class Timer:
    def __init__(self):
        self.start = time.monotonic()

    def __call__(self, reset=False):
        now = time.monotonic()
        duration = now - self.start
        if reset:
            self.reset()

        return duration

    def reset(self):
        self.start = time.monotonic()
