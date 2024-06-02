import sys

from abstract_base_classes.observer import Observer


class FlaskConsoleLogger(Observer):
    def __init__(self):
        super().__init__()
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self

    def write(self, message):
        if sys.exc_info() != (None, None, None):
            message_type = 'error'
        else:
            message_type = 'output'

        self.notify_observers({'matrixModeGlobalConsole': message})

        self.original_stdout.write(message)

    def flush(self):
        self.original_stdout.flush()
        self.original_stderr.flush()

    def close(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr