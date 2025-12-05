# with statement in python is useful in managing external resourcesin your programs
# can automatically set up & teardown phases whenever you're dealing with external resources
# avoid resource leaks

# python with statement creates a runtime context that allows u to run
# a group of statements under the control of a context manager

# The context manager object results from evaluating the expression after with.
# In other words, expression must return an object that implements the context management protocol.
# This protocol consists of two special methods:
# .__enter__() is called by the with statement to enter the runtime context.
# .__exit__() is called when the execution leaves the with code block.



# (1) with statement
# (2) context management protocol
# (3) implement own context managers

# files ,lock & network connections => prone to mem leaks; becoz never close after opening them
# setup & teardown phase
# common scenarios
    # DB
    # DB gets queried & new connections keep forming without releasing or reuisng them
    # DB can stop accepting new connections => will need admin to log in & manually kill those stale connections

    # Files
    # writing text to file usually buffered ops => write to a buffer first before writing to file
    # sometimes when buffer isnt full & devs forget to call .close(), part of the data is lost forever

    # Error encounter
    # app run into error & control flow bypasses code responsible for releasing the resources at hand

# ---------------------------------------------
# File example
file = open("hello.txt", "w") # can read "r" also
file.write("hello, world!")
file.close() # is not guaranteed to be closed!

# try ... finally construct => verbose, might forget clean up actions
file = open("hello.txt", "w")
try:
    file.write("hello, world!")
except Exception as e:
    print(f"an error occured: {e}")
finally:
    file.close() # so even if theres error file is closed

# with construct
# creates runtime context that allws you to run a group of statements under the control of a context manager
# with expression as target_var:
#     do_something(target_var)

with open("hello.txt", mode="w") as file:
    file.write("hello world!")

with A() as a, B() as b: # can even use multiple context managers
    pass

# COMMON MISTAKES
file = open()
with file:
    file.write("hello world!") # returns the numof bytes written into the file
# returns 13
with file:
    file.write("try again")
# ValueError: I/O operation on closed file => because the file that is referenced is already closed

# use try to avoid missing file errors
import pathlib
import logging
fail_path = pathlib.Path("hello.txt")
try:
    with file_path.open(mode="w") as file: # err is raised from opening the file
        file.write("hello world")
except OSError as e:
    logging.error("Writing to file %s failed due to: %s", file_path, e)

# ---------------------------------------------
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

# ---------------------------------------------
# my own test
class StringContextManager:
    def __init__(self, string):
        self.string = string

    def __enter__(self):
        print(f"enter the {self.string}")
        return self.string
        pass
    def __exit__(self):
        print(f"exit the {self.string}")
        pass
with StringContextManager("poop") as string:
    print("im inside the context")
    print(f"context uses {string}")
















# ---------------------------------------------
# PATHLIB
import pathlib
file_path = pathlib.Path("hello.txt") # represents concrete paths to physical files in your computer
# calling .open() on Path object is just like open()
with file_path.open("w") as file:
    file.write("Hello world!")
# returns 13

# ---------------------------------------------
# iterator that supports context mgmt protocol
# scandir() returns an iterator
import os
with os.scandir(".") as entries:
    for entry in entries:
        print(entry.name, "->", entry.stat().st_size, "bytes") # prints out the size of each dir

# ---------------------------------------------
# handling locks
import threading
balance_lock = threading.Lock()
balance_lock.acquire()
# try:
#     # update acc bal here
#     pass
# finally:
#     balance_lock.release()

# can do twice since entering & exiting context manager will acquire & release the lock
with balance_lock:
    # update bal acc here
    pass
with balance_lock:
    # update bal acc here
    pass
