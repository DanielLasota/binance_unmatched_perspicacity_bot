import sys
from io import StringIO
from abstract_base_classes.observer import Observer
import argparse


class Calculator(Observer):
    def __init__(self):
        super().__init__()
        self.main_invocation_command = 'calculator'

    def create_parser(self):
        parser = argparse.ArgumentParser(
            prog='calculator',
            description='Calculator command interpreter.'
        )

        operators = parser.add_mutually_exclusive_group(required=True)
        operators.add_argument('--add', nargs=2, type=float, metavar=('OPERAND1', 'OPERAND2'),
                               help='Adds two numbers')
        operators.add_argument('--sub', nargs=2, type=float, metavar=('OPERAND1', 'OPERAND2'),
                               help='Subtracts the second number from the first')
        operators.add_argument('--mul', nargs=2, type=float, metavar=('OPERAND1', 'OPERAND2'),
                               help='Multiplies two numbers')
        operators.add_argument('--div', '-d', nargs=2, type=float, metavar=('OPERAND1', 'OPERAND2'),
                               help='Divides the first number by the second')
        return parser

    def update(self, data):
        if (list(data.items())[0][0] == 'cli_request'
                and list(data.items())[0][1].split()[0] == self.main_invocation_command):
            self.execute_command(list(data.items())[0][1])

    def execute_command(self, command):
        args = command.split()[1:]
        parser = self.create_parser()

        try:
            parsed_args = vars(parser.parse_args(args))
            result = 0
            if parsed_args['add']:
                result = parsed_args['add'][0] + parsed_args['add'][1]
            elif parsed_args['sub']:
                result = parsed_args['sub'][0] - parsed_args['sub'][1]
            elif parsed_args['mul']:
                result = parsed_args['mul'][0] * parsed_args['mul'][1]
            elif parsed_args['div']:
                operands = parsed_args['div']
                if operands[1] != 0:
                    result = operands[0] / operands[1]
                else:
                    raise ValueError("Division by zero is not allowed.")

            print(f'CALCULATOR RESULT: {result}')
            self.notify_observers(f'Result: {result}')
        except Exception as e:
            print(f'Error: {e}')
            self.notify_observers(f'Error: {e}')

    def get_help_string(self):
        parser = self.create_parser()
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        parser.print_help()
        help_string = sys.stdout.getvalue()
        sys.stdout = old_stdout
        return help_string
