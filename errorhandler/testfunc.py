from error_handler_2 import safe_class, ErrorHint


@safe_class({"step1": "step_end", "step5": "step_end"})
class MyClass:
    def __init__(self):
        self.hint = ErrorHint()

    def step1(self, a, b):
        self.hint.add("b", "b must not be zero (division issue)")
        print(a / b)  # ZeroDivisionError triggers step_end

    def step2(self):
        print("Step2 runs normally")

    def step5(self):
        self.hint.add("custom", "Step5 failed due to invalid operation")
        raise ValueError("custom invalid state")

    def step_end(self):
        self.hint.add("fatal", "Recovery failed — stopping program")
        print("Running recovery...")
        1 / 0  # This will HALT the entire program


# ======== Demo ========
obj = MyClass()
obj.step1(10, 0)
obj.step2()
obj.step5()
