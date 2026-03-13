# Design patterns
This notes cover design patterns used in software.

# 8 common design patterns by neetcode

# -------------------------------------------------------------------------------------------------
# 8 common design patterns by neetcode
resource: https://neetcode.io/courses/lessons/8-design-patterns

`creational`
1. factory method - creates objs without exposing exact class of the instance being created
2. singleton - class only has 1 global instance
3. builder - constructs complex objs step by step (building custom burger)
`behaviourial`
4. observer (PubSub) - apps react to events, need to comms events; so we have publisher (src of events), subscriber (consume events)
5. iterator
6. strategy
`structural`
7. facade - an outward appearance that is maintained to conceal a less pleasant or creditable reality (i.e. class, context managers, generators etc.)
    => less creditable meaning less respectable lol
8. adaptter - allows incompatible objects to be used together.

## elaboration
1. factory method
    - not the same as singleton!! => its own design pattern
    - mainly to provide an interface for creating objs without exposing the concrete class
    ```cpp
    class Shape {
        public:
        virtual void draw() = 0;
    };

    class Circle : public Shape {
        public:
        void draw() override {}
    };

    class ShapeFactory {
        public:
        static Shape* createShape() {
            return new Circle();
        }
    }
    // this shows that Circle class constructor was never exposed, yet we can create a Circle instance via the
    // ShapeFactory by calling createShape => & then it still has the draw method
    ```
2. Singleton
    - only class itself can create a single instance
    - need a factory method => more accurate to say a singleton uses a static factory method to control obj creation
        1. private constructor
        2. static storage of instance
    ```cpp
    class Logger {
    public:
        static Logger& getInstance() {
            static Logger instance; // static instace that holds the single instance of the classs
            return instance
        };
    private:
        Logger() {} // private constructor
    };

    // THUS
    Logger log; // X compile error => this actually does 1. allocate mem for log, constructor for Logger() is called, obj is initialized => constructor is actually called!!
    Logger* log = new Logger(); // X compile error
    ```
6. strategy
- helps select algo at run time
- issue solved: avoids large conditional statements that switch between `different variants` for the `same algo`
i.e. 
```python
from abc import ABC, abstractmethod
class FilterStrategy(ABC):
    @abstractmethod

```

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

8. adapters
example of adapter usage to make a new USB type be pluggable to a USB port
```python
class UsbCable:
    def __init__(self):
        self.isPlugged = False

    def plugUsb(self):
        self.isPlugged = True


class UsbPort:
    def __init__(self):
        self.portAvailable = True

    def plug(self, usb_cable):
        if self.portAvailable:
            usb_cable.plugUsb()
            self.portAvailable = False


class MicroUsbCable:
    def __init__(self):
        self.isPlugged = False

    def plugMicroUsb(self):
        self.isPlugged = True


class MicroToUsbAdapter:
    def __init__(self, micro_usb_cable):
        self.micro_usb_cable = micro_usb_cable

    def plugUsb(self):
        self.micro_usb_cable.plugMicroUsb()


# UsbCable can plug directly into a UsbPort
usb_cable = UsbCable()
usb_port1 = UsbPort()
usb_port1.plug(usb_cable)

print("USB cable plugged:", usb_cable.isPlugged)   # True
print("USB port 1 available:", usb_port1.portAvailable)  # False


# MicroUsbCable needs an adapter to plug into a UsbPort
micro_usb_cable = MicroUsbCable()
adapter = MicroToUsbAdapter(micro_usb_cable)

usb_port2 = UsbPort()
usb_port2.plug(adapter)

print("Micro USB cable plugged:", micro_usb_cable.isPlugged)   # True
print("USB port 2 available:", usb_port2.portAvailable)  # False
```