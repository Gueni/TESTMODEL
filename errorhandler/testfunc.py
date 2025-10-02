from error_handler import safe_class, ErrorHint

@safe_class
class Calculator:
    def __init__(self):
        # Instance-level hint storage
        self.hint = ErrorHint()

    def divide(self, a, b):
        # Custom suggestion for this variable
        self.hint.add('b', "You cannot divide by zero! Provide a non-zero 'b'")
        return a / b

    def open_file(self, filename):
        # Custom suggestion for this variable
        self.hint.add('filename', "Make sure the file exists or create it before opening")
        with open(filename) as f:
            return f.read()

    def process_list_dict(self, lst, dct, index, key):
        # Custom hints
        self.hint.add('index', "Index should be within the bounds of the list.")
        self.hint.add('key', "Key must exist in the dictionary before accessing.")

        # Example operations that could fail
        total = lst[index] + dct[key]  # IndexError, KeyError, TypeError possible
        return total

# --- Example usage ---
calc = Calculator()

# Trigger custom ZeroDivisionError
calc.divide(10, 0)

# Trigger custom FileNotFoundError
calc.open_file("missing.txt")

# Trigger multiple errors
calc.process_list_dict([1, 2, 3], {"a": 10}, 5, "b")  # IndexError and KeyError
