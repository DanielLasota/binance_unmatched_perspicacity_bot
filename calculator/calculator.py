from abstract_base_classes.observer import Observer
import argparse


class Calculator(Observer):
    def __init__(self):
        super().__init__()

    def update(self, data):
        print(f'received: {list(data.items())[0]}')

        if list(data.items())[0][0] == 'cli_request' and list(data.items())[0][1].split()[0] == 'calculator':
            self.execute_command(list(data.items())[0][1])

    def execute_command(self, command):
        args = command.split()[1:]
        parser = argparse.ArgumentParser(description='Calculator command interpreter.')
        parser.add_argument('operator', type=str, choices=['add', 'sub', 'mul', 'div'], help='Operation to perform')
        parser.add_argument('operands', type=float, nargs=2, help='Two operands for the operation')

        try:
            parsed_args = parser.parse_args(args)
            result = 0
            if parsed_args.operator == 'add':
                result = parsed_args.operands[0] + parsed_args.operands[1]
            elif parsed_args.operator == 'sub':
                result = parsed_args.operands[0] - parsed_args.operands[1]
            elif parsed_args.operator == 'mul':
                result = parsed_args.operands[0] * parsed_args.operands[1]
            elif parsed_args.operator == 'div':
                if parsed_args.operands[1] != 0:
                    result = parsed_args.operands[0] / parsed_args.operands[1]
                else:
                    raise ValueError("Division by zero is not allowed.")
            print(f'CALCULATOR RESULT: {result}')
            self.notify_observers(f'Result: {result}')
        except Exception as e:
            self.notify_observers(f'Error: {e}')