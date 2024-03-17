import sys

from abstract_base_classes.observer import Observer


class FlaskConsoleLogger(Observer):
    def __init__(self):
        super().__init__()
        self.original_stdout = sys.stdout

    def write(self, message):
        self.notify_observers({'matrixModeGlobalConsole': message})
        self.original_stdout.write(message)

    def flush(self):
        self.original_stdout.flush()

    def close(self):
        sys.stdout = self.original_stdout
