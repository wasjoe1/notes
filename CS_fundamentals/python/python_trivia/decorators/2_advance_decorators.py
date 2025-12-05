# decorator that takes in arguments

def decorator_wtih_args(arg1, arg2):
    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            # do smt with args
            print(arg1)
            print(arg2)
            
            print("start effect")
            func(*args, **kwargs)
            print("end effect")
        return wrapper

@decorator_wtih_args(1,2) # this executes and returns the decorator function
def test():               # @ is just syntatic sugar to use the function and take in the function below
    print("test")
