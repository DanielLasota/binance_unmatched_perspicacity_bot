import argparse

from abstract_base_classes.observer import Observer


class CLIDaemon(Observer):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CLIDaemon, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super().__init__()

    def create_parser(self):
        parser = argparse.ArgumentParser(
            prog='BINANCE Unmatched Perspicacity BOT CLI Daemon',
            description='BINANCE Unmatched Perspicacity BOT CLI Daemon'
        )

        parser.add_argument(
            '--print_hello',
            action='store_true',
            help='Prints "hello" as a response to the command.'
        )

        return parser

    def execute_command(self, command):
        args = command.split()
        parser = self.create_parser()

        try:
            parsed_args = parser.parse_args(args)
            if parsed_args.print_hello:
                print('hello')

        except Exception as e:
            print(f'Error: {e}')

    def update(self, data):
        self.notify_observers(data)
        if list(data.items())[0][0] == 'cli_request':

            command_found = False
            command_name = list(data.items())[0][1].split()[0]

            for observer in self._observers:
                if (hasattr(observer, 'main_invocation_command')
                        and getattr(observer, 'main_invocation_command') == command_name):
                    command_found = True
                    break

            if command_name in ['--help', '-h'] and command_found is False:
                print(':::::::::::::::::::::::::::::::::::::::::::::::::::')
                print(':::BINANCE Unmatched Perspicacity BOT CLI Daemon:::')
                print(':::::::::::::::::::::::::::::::::::::::::::::::::::')
                print(' ')

                for observer in self._observers:
                    print(observer.get_help_string())
                    print(' ')
                    print(' ')
                    print(' ')

                self.execute_command(list(data.items())[0][1])  # w tym miejscu kodu

                return

            if command_found is False:
                self.execute_command(list(data.items())[0][1])
                print(' ')
