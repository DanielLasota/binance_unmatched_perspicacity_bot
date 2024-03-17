from abstract_base_classes.observer import Observer


class CLIDaemon(Observer):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CLIDaemon, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()

    def update(self, command):
        print(f"cli has received command: {command}")
        self.notify_observers(command)
