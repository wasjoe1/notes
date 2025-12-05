# python does not support method overloading => it will jsut use the latest method declared

class Example:
    def method(self, a):
        return a + 1
    
    def method(self, a, b): # this is the latest method declared
        return a + b

obj = Example()
print(obj.method(5, 3))  # This works
# print(obj.method(5))   # This would raise a TypeError