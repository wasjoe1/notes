* python does enforce abstract methods & classes at runtime
    - when class inherits from `ABC` python treats it as `base class` meant to be subclassed
    - abstract classes can be instantiated (if it has no abstract methods) => whereas abstract classes in java dont
    - subclasses that inherits from the ABC class will need to implement abstract methods, else it will raise exception at runtime => at compile time no exception raised yet!

```python
# INVALID e.g. -> abstract method not implemented
class BadStrategy(FilterStrategy):
    pass
# no exception raised yet!
BadStrategy() # raise Exception!!

# VALID e.g. -> abstract method has wrong signature
class WeirdStrategy(FilterStrategy):
    def removeValue(self):  # wrong signature
        return False
WeirdStrategy() # valid; doesnt raise Exception though!!

# VALID e.g. -> instantiation of abstract class (w no abstract method)
class Good(ABC):
    def hi():
        pass
Good() # allowed!
```
