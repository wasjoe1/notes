class StringContextManager:
    def __init__(self, string):
        self.string = string

    def __enter__(self):
        print(f"enter the {self.string}")
        return self.string # return val used in context manager

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type: # if no err, this will be none
            print(exc_type, exc_val, exc_tb)
        print(f"exit the {self.string}")

with StringContextManager("poop") as string:
    # inside the context
    print("im inside the context")
    raise ValueError
    print(f"context uses {string}")

print("im continuing here...")

