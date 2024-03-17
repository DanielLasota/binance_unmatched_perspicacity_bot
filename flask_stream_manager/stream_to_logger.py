import sys


class Subject:
    def __init__(self):
        self.observers = []

    def register(self, observer):
        self.observers.append(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message_type, message):
        for observer in self.observers:
            observer.update(message_type, message)


class FlaskConsoleLogger(Subject):
    def __init__(self):
        super().__init__()
        self.original_stdout = sys.stdout

    def write(self, message):
        self.notify_observers('matrixModeGlobalConsole', message)
        self.original_stdout.write(message)

    def flush(self):
        self.original_stdout.flush()

    def close(self):
        sys.stdout = self.original_stdout
