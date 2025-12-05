#/usr/bin/env python3

# A first class object is an entity that can be dynamically created, destroyed,
# passed to a function, returned as a value, and have all the rights as other
# variables in the programming language have

# A decorator is a function, that takes in another function as an argument,
# and returns a new function with extra functionality

# ---------------
# 1st draft => simple wrapper with print statements
# def decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper

# def say_whee():
#     print("Whee!")

# say_whee = decorator(say_whee) # take in say_whee to decorator while
# ---------------
# 2nd draft => wrapper that makes function only executable at night
# from datetime import datetime

# def not_during_the_night(func):
#     def wrapper():
#         if 7 <= datetime.now().hour < 22:
#             func()
#         else:
#             pass  # Hush, the neighbors are asleep
#     return wrapper

# def say_whee():
#     print("Whee!")

# say_whee = not_during_the_night(say_whee)

# ---------------
# 3rd draft => syntactic sugar @ symbol (pie symbol)
# def decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper

# @decorator
# def say_whee():
#     print("Whee!")
# @decorator is just a shorter way of saying say_whee = decorator(say_whee)
# @function that will take in the below function
# then return a wrapper function with the same name as the below function
# yet modifies the behaviour

# reduces chunkiness of code
# @ decorator is just a regular python function

# ---------------
# 4th draft => decorators with args
# function that accepts args, then you want to add decorators
# how to accept args? => both positional & keyword args

def decorator(func):
    def wrapper(*args, **kwargs): # takes in positional & kwargs
        print("smt")
        func(*args, **kwargs) # unpacks args & kwargs into arguments
        # *args unpacks list or tuples into positional arguments
        # **kwargs unpakcs dictionary into keyword args
        print("smt")
    return wrapper

# @decorator
# def test(num1,num2,num3, name, age):
#     print(num1,num2,num3)
#     print(name, age)

# @decorator => this works too
# def test(num1,num2,num3, **kwargs):
#     print(num1,num2,num3)
#     print(kwargs)

# test(1,2,3, name="joe", age=24)

# ---------------
# 5th draft => return value from decorated functions
def decorator(func):
    def wrapper(*args, **kwargs): # takes in positional & kwargs
        print("smt")
        return_val = func(*args, **kwargs) # unpacks args & kwargs into arguments
        # *args unpacks list or tuples into positional arguments
        # **kwargs unpakcs dictionary into keyword args
        print("smt")
        return return_val
    return wrapper

@decorator
def test(some_val):
    return some_val # whether this is returned depends on the decorator

print(test("test test"))