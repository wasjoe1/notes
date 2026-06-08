# Chapter 5: constants & strings

## chp 5.1:
## chp 5.2:
## chp 5.3:
## chp 5.4:
## chp 5.5:
## chp 5.6:

## chp 5.7: intro to std::string

### C-style string literals vs std::string

```cpp
#include <iostream>

int main()
{
    std::cout << "Hellow, world!"; // "Hello world!" is a C-style string literal
}
```

- C-style strings literals
    - hard to work with (i.e. cant use assignments to assign new string to existing string variable)
    - dangerous (i.e. copying larger string into shorter C-style strings, undefined behavior occurs)
- `std::string` & `std::string_view` easiest way to work with strings & safe
    - are class types (not fundamental types)
    - lives in the <string> header

### std::string basics

```cpp
#include<string> // allows use of std::string

// (1) basics
std::string name{}; // empty string
std::string alice{"Alice"}; // intializae alice with string literal "Alice"

std::string myId{"45"}; // string-formed numbers cant be manipulated as numbers (i.e. cant multiply)

// (2) std::cout
// string output with std::cout
std::cout << "My name is: " << name << '\n'; // \n is a character


// (3): can handle strings of different lengths - if std::string doesnt have enough MEM, it will request additional MEM at runtime using *dynamic MEM allocation*
name = "John" // change name to John
```

### std::cin, std::getline(cin, str_var) & std::ws

```cpp
// (4): std::cin (refer to notes & cin_Error.cpp)
// (5): std::getline() & std::ws (refer to notes & cin_Correct.cpp)
```

(4) std::cin
- operator>> only returns characters up to the first whitespace it encounters, any other chracters are left inside `cin`'s buffer
- using the example, surname was used as the input for color without waiting for 2nd input by user
- it then auto uses the buffered input for the next query

(5) std::getline() & std::ws `std::getline(std::cin >> std::ws, color);`
- std::getline() - just gets the entire line you've inputted EXCEPT the escape character `\n` when u hit enter
- std::ws - is a _input string manipulator_ tells cin to ignore leading whitespace (spaces, tabs, newlines)
- this is useful because, whenever the program asks for a string input, the user places a `\n` character to mark the end of the line. we want to ignore this for the next input
- when using std::getline() to read strings, use std::cin >> std::ws input manipulator to ignore leading whitespace; this needs to be done for each std::getline()

* NOTE: `std::cin` already ignores leading white space hence it doesnt need `std::ws` when reading multiple texts

### length of string

```cpp
name.length() // returns 4 if name was "Alex";
```

- std::string is required to be null-terminated (`\0`) but it returns the length of std::string not including the null-terminator character
- its a member function sometimes writted as `std::string::length` in docs
- returns an unsigned integral value (typically `size_t`) => need to staic_cast to avoid compiler warnings about signed/ unsigned conversions

* note that size & capacity is for containers in general but length is specifically for strings

### _initialize_ std::string

- during std::string initiliazation, a copy of the string is used to initialize it; making copies is expensive, care should be taken to minimize the number of copies made

### _pass_ std::string to function (by value, std::string_view)

- DONT PASS `std::string by value` - expensive, because function parameter must be instantiated & initialized, resulting in copy (expensive)
- use `std::string_view`

### _return_ std::string

- typically returning std::string by value to the caller creates a copy => expensive
- BUT its okay to return _by value_ when the return statement resolves to any of the following:
    - a local variable(inside callee) of type `std::string`
    - a `std::string` that has been returned by value from another function call or operator
    - a `std::string` temporary that is created as part of the return statement
    * `std::string` supports copy ellision (URVO, NRVO) +  move semantics which doesnt copy the data (refer to [# move semantics vs copy elision](../../quick_notes_cpp.md))
- _C-style string literal_ & `std::string_view` - when returning _C-style string literal_ use `std::string_view`
- return _by const reference_ in some cases to avoid copy (return by reference & by address)

### _literals_ for std::string (C-style string literals vs std::string continuation)

```cpp
auto s1 = "hello\0world"  // type const char*, length = 5 ("hello")
#include <string>
auto s2 = "hello\0world"s // type std::string, length = 11 ("hello\0world")
#include<string_view>
auto view = "hello\0world"sv // type std::string_view (to be discussed later)
```

* "hi" is an lvalue - character array baked into program's `read-only data` segment at *compile time* => MEM address lasts for entire duration of program
* "hi"s is a prvalue - creates transient std::string instance on the fly (*runtime*) => is destroted at the end of scope, unless you bind or move it to permenant variable

- C-style strings - double quote string literals have a strange type
- s suffix added after the double-quoted string literal to create string literals with type `std::string`
- _std::string literal_ is not a separate type like `std::string_literal`(its type is `std::string`); it evaluates directly to a `std::string` temporary object - literal operator (operator""s) instructs the compiler to construct a `std::string` right where you wrote it

- "s" suffix lives in the namespace `std::literals::string_literals`
- most concise way to access the literal suffixes is via using-directive `using namespace std::literals` -> this imports all the std lib literals into the scope
- thus reccomendation is to use: `using namespace std::string_literals`, which imports only literals for `std::string`
    - the exception case where *using* an entire namespace is okay because the suffixes defined is unlikely to collide with any of your code
    - STILL, avoid using-directives outside of functions in header files
- its *rare* to use std::string literals (its fine to initialize std::string objects with C-style string literals) BUT there are few rare cases involving type deduction
    where using std::string literals instead of C-style string literals make things easier??

### _constexpr_ std::string
- if you try to define a `constexpr std::string`, compiler will likely throw an error -> not supported in cpp17, typically supported in cpp20/23
- if you need to do this, use `std::string_view`

* constexpr specifies that a value/ variable/ return value can be evaluated at _compile time_ rather than _runtime_

```cpp
#include<iostream>
#include<string>

int main()
{
    using namepspace std::string_literals;
    
    constexpr std::string name{"Alex"}; // compile error
    std::cout << "my name is: " << name;

    return 0;
}
```