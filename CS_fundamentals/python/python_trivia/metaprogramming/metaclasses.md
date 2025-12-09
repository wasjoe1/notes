# metaclasses

python supports a form of metaprogramming for classes called metaclasses
- metaclasses are an esoteric OOP concept => esoteric: intended to be understood by only a small # of ppl
- it is a capability not all OOP languages support => but python does
- can get UTH & define custom metaclasses

* to note: in python everything is an object

---------------------------------------------------------------------------------------------------
## old style vs new style classes
- class can either be new or old style classes








# TODO: tidy up the below notes (notes take in plane)
type() built in function

When 1 arg passed in:
Returns the type of an object => for new style classes, that is the same as the obj’s .__class__ attr
i.e. type(3) # returns <class ‘int’>

When multiple args passed in:
type(<class_name>, <bases/ inehritance>, <dct>)
<class_name> - specified class name and becomes name attr of the class
<bases/ inehritance> - specifies the base class this new class inherits from. This becomes the bases attr of the class
<dct> - specifies a namespace dict (python namespaces are mostly implemented using dictionaries, key is names, value is objects)
i.e. bar = type(‘Bar’, (Foo,), dict(attr=100, some_fn=declared_fn)
*type() creates attrs that are initially shared by all instances (class variables)

Useful scenarios: Auto-registering subclasses

# Metaclass that auto-registers subclasses
class PluginMeta(type):
    registry = {}

    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        if name != 'Plugin':  # don't register the base class
            PluginMeta.registry[name] = new_cls
        return new_cls

# Base class uses the metaclass
class Plugin(metaclass=PluginMeta):
    pass

# Subclasses automatically get registered
class PluginA(Plugin):
    pass

class PluginB(Plugin):
    pass

print(PluginMeta.registry)
# Output: {'PluginA': <class '__main__.PluginA'>, 'PluginB': <class '__main__.PluginB'>}

Metaclasses vs actual classes
Metaclasses allow u to enforce rules during CREATION of the class itself; not just at INSTANTIATION


This is done so as:
1. MyClass is an instance of type i.e. type(MyClass) <class ‘type’>
2. MyClass(10) actually invokes call => obj = metaclass.__call__(10)
# what call does:
def __call__(cls, *args, **kwargs):
    obj = cls.__new__(cls, *args, **kwargs)
    if isinstance(obj, cls):
        cls.__init__(obj, *args, **kwargs)
    return obj
* meta.__call__ invokes cls.__new__ and cls.__init__

* defining a class calls metaclass.__new__ && metaclass.__init__
* instantiating a class calls metaclass.__call__ cls.__new__ && cls.__init__