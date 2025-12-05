# Special / Dunder methods

(5).__add__(2)

# ------------------------------------
# Controlling object creation process

def __init__(self):
    pass
# Python calls the .__init__() method whenever you call the constructor of 
# a given class. The goal of .__init__() is to initialize any instance attribute
# that you have in your class.

# basically when you instantiate a class, python auto calls __init__ under 
# the hood using the same args u passed into the construtor

# When you call a class constructor to create a new instance of a class,
# Python implicitly calls the .__new__() method as the first step
# in the instantiation process. This method is responsible for creating
# and returning a new empty object of the underlying class.
# Python then passes the just-created object to .__init__() for initialization.
# (in most cases default implementation of .__new__() is sufficient)

class Storage(int):
    # class method tho it does not need @class decorator since its executed before instantiating a class
    def __new__(cls, value, unit): # new is called before __init__
        instance = super().__new__(cls, value) # create a new instance
        instance.unit = unit # attach object attribute => can actl do it in __init__ as well
        return instance
# 3 steps:
# 1. create new instance of curr class => call __new__() on the float class w arg val
# 2. customize new instance by dynamically attaching unit to the instance
# 3. return instance

s1 = Storage(10, "GB")
s2 = Storage(20, "GB")
print(s1<s2)

# ------------------------------------
# Dev friendly string representations
class Person:
        def __repr__(self):
            return f"{type(self).__name__}(name='{self.name}', age={self.age})"

# ------------------------------------
# Operating overloading in custom classes
# arithmetic operators
# .__add__(self, other)
# .__sub__(self, other)

class Storage(float):
    def __new__(cls, value, unit):
        instance = super().__new__(cls, value)
        instance.unit = unit
        return instance

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(
                "unsupported operand for +: "
                f"'{type(self).__name__}' and '{type(other).__name__}'"
            )
        if not self.unit == other.unit:
            raise TypeError(
                f"incompatible units: '{self.unit}' and '{other.unit}'"
            )

        return type(self)(super().__add__(other), self.unit)