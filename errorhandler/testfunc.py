from error_handler_2 import safe_class, ErrorHint

# Define which methods trigger which recovery
skip_rules = {"step1": "step_end", "step5": "step_end"}

@safe_class(skip_rules)
class MyClass:
    def __init__(self):
        self.hint = ErrorHint()

    def step1(self, a, b, c):
        # Multiple hints in the same function
        self.hint.add("b", "b must not be zero — warning only", force_skip=False)  # warning
        self.hint.add("c", "c must not be zero — triggers recovery", force_skip=True)  # jump
        print("Step1 executing")
        # This line triggers the exception for demonstration
        print(a / c)  # ZeroDivisionError


    def step2(self):
        self.hint.add("none", "Step2 normal warning", force_skip=False)
        print("Step2 runs normally")

    def step5(self):
        self.hint.add("custom", "Step5 failed — going to recovery", force_skip=False)
        raise ValueError("Step5 triggers recovery")

    def step_end(self):
        self.hint.add("recovery", "Step_end recovery running — program will halt if fails", force_skip=False)
        print("Step_end recovery running...")
        1 / 0  # simulate fatal error in recovery

# ===== Demo =====
if __name__ == "__main__":
    obj = MyClass()

    obj.step1(10, 5, 0)  # 'b' hint ignored, 'c' hint triggers recovery
    obj.step2()           # skipped because recovery flag was set
    obj.step5()           # would trigger recovery, skipped if already ran
    obj.step_end()           # would trigger recovery, skipped if already ran
