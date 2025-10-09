import __main__
from error_handler_2 import safe_class, ErrorHint

# -------------------
# Example usage
skip_rules = { "step1": "step_end", "step5": "step_end" }

@safe_class(skip_rules)
class MyClass:
    def __init__(self):
        self.hint = ErrorHint()
        self._step_end_ran = False

    def step1(self, a, b):
        self.hint.add("b", "b cannot be zero")
        print("Step1 result:", a / b)

    def step1_5(self, multiplier):
        print("Step1.5 result:", multiplier * 2)

    def step2(self):
        print("Step2 runs normally")

    def step3(self):
        self.hint.add("", "step3 hinht")
        print("Step3 runs normally")

    def step5(self):
        raise ValueError("Step5 error!")

    def step_end(self):
        print("Step_end runs as recovery")

# -------------------
# Test workflow
def main():

    obj = MyClass()
    obj.step1(10, 0)  # triggers step_end automatically
    obj.step1_5(5)    # skipped because _skip_next_steps=True
    obj.step2()       # skipped
    obj.step_end()    # already ran, skipped


main()


# main.py
from error_handler_2 import MyClass, safe_class, ErrorHint

skip_rules = {"step1": "step_end", "step5": "step_end"}
MyClass = safe_class(skip_rules)(MyClass)  # re-decorate

def main():
    obj = MyClass()
    obj.step1(10, 0)
    obj.step1_5(5)
    obj.step2()
    obj.step_end()
