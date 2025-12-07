# 
- templates
- iterators
- operator overloading
- pointer arithmetic

templated vector constructor
* the vector constructor is a templated function basically

# Template function
```C++
// vector construction i.e.
template<class InputIt>
vector(InputIt first, InputIt last); // no return type since this is a constructor => just creates the object, initialize internal state 

// random i.e.
template<typename T> // typename & class are interchangeable in template declarations; class has been in cpp since the start(C++98); typename was intro-ed later to  clarify that a template parameter represents a type
T add(T a, T b) {
    return a + b;
}
int x = add(1,2)
float y = add(1.1, 2.2)
std::cout << x << y
```
- the above are template functions/ constructors => allows u to write generic code that works with many types without duplicating the fn
