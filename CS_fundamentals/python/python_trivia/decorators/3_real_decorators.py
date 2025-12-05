# timer decorator
# i only want to start the time and end the time when the function has completed
# i dont need to take in any arguments for my decorator
# my function might take in args & kwargs though
def timer(func):
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        return_val = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        print(f"Execution time: {total_time}")
        return return_val
    return wrapper