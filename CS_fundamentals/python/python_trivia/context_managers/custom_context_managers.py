# provide same functionality by implementing both
# .__enter__() & .__exit()__ in classbased context managers
# can also create function based context managers using contextlib.contextmanager decorator

class example:
    # def __init__(self): # no need init
    #     pass
    
    def __enter__(self): # returns the target variable which is assigned to the variable after the as keyword
        pass
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        # is executed when flow of execution leaves context
        # if no exeception, 3 last args are set to None
        # otherise type, value & traceback are assigned to them
        pass

# ----------------------------------------------------
class HelloContextManager:
    def __enter__(self):
        print("Entering the context...")
        return "Hello, World!"
    def __exit__(self, exc_type, exc_value, exc_tb):
        print("Leaving the context...")
        print(exc_type, exc_value, exc_tb, sep="\n")

with HelloContextManager() as hello: # need to call the call the object HelloContextManager()
    print(hello)

# Entering the context...
# Hello, World!
# Leaving the context...
# None
# None
# None

# ----------------------------------------------------
with HelloContextManager() as hello:
    print(hello)
    hello[100] # will have err here

# Entering the context...
# Hello, World!
# Leaving the context...

# <class 'IndexError'>                  => err raised & all the args were set accordingly
# string index out of range
# <traceback object at 0x7f0cebcdd080>
# Traceback (most recent call last):
#   File "<stdin>", line 3, in <module>
# IndexError: string index out of range

# ----------------------------------------------------
# forget to call object passed to the with statement
with HelloContextManager as hello: # HelloContextManager is not called
    print(hello)
# Traceback
# AttributeError __enter__

# ----------------------------------------------------
# Handling exception within __exit__
# exc_handling.py

class HelloContextManager:
    # can have __init__ but is not required since no argument taken in
    def __enter__(self):
        print("Entering the context...")
        return "Hello, World!"

    def __exit__(self, exc_type, exc_value, exc_tb):
        print("Leaving the context...")
        if isinstance(exc_value, IndexError):
            # Handle IndexError here...
            print(f"An exception occurred in your with block: {exc_type}")
            print(f"Exception message: {exc_value}")
            return True

with HelloContextManager() as hello:
    print(hello)
    hello[100] # previously this would stop execution here

print("Continue normally from here...") # but now exec continues

# Entering the context...
# Hello, World!
# Leaving the context...
# An exception occurred in your with block: <class 'IndexError'>
# Exception message: string index out of range
# Continue normally from here...

# ----------------------------------------------------
# Custom file
class WritableFile:
    def __init__(self, file_path): # the init is used when you instantiate the object, which has __enter__ & __exit__ methods
        self.file_path = file_path

    def __enter__(self):
        self.file_obj = open(self.file_path, mode="w")
        return self.file_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file_obj:
            self.file_obj.close()

with WritableFile("hello.txt") as file:
    file.write("Hello")