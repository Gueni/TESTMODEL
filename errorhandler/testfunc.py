from error_handler import safe_class, ErrorHint

@safe_class
class Calculator:
    def __init__(self):
        # instance-level hint
        self.hint = ErrorHint()

    def divide(self, a, b):
        # custom suggestion for this variable
        self.hint.add('b', "You cannot divide by zero! Provide a non-zero 'b'")
        return a / b

    def open_file(self, filename):
        # custom suggestion for this variable
        self.hint.add('filename', "Make sure the file exists or create it before opening")
        with open(filename) as f:
            return f.read()

calc = Calculator()
calc.divide(10, 0)           # Uses custom suggestion
calc.open_file("missing.txt") # Uses custom suggestion
