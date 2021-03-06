#============================================
# Credit: Victor Moyseenko - StackOverflow
# https://stackoverflow.com/questions/4995733/
#
#   USAGE:
#        with Spinner():
#           # ... some long-running operations
#           # time.sleep(3)
#============================================
import sys
import time
import threading

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None, mute=False):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay
        self.mute = mute

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        if self.mute: self.busy = False
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False
