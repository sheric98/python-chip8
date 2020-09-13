from constants import NANO
import time


class Clock:
    def __init__(self, freq):
        self.period = NANO // freq
        self.offset = time.time()

    def tick(self):
        if time.time() - self.offset > self.period / NANO:
            self.offset += self.period / NANO
            return True
        else:
            return False
