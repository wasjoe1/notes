# Chapter 5: constants & strings

## chp 5.1: constant variables

named constants - constant values associated with an identifier (aka symbolic constants)
literal constants - constant values not associated with an identifier

* this chapter's focus: named variables

_types of named constants_
1. constant variables
2. object-like macros with substitution text (from chp 2.1)
3. enumerated constants (to be covered in chp 13.2)

_constant variables_
- const keyword (aka const qualifier) used to decalre a constant variable
- const variables must be initialized => cant change via assignment
- initializer can be non-const
- when parameters are pass-by-value into func => dont use const (no point)
    - different for pass by ref & pass by address
- dont use const when return by value
    - temp copies will be destroyed anyway (meaning the return slot is const but will be destroyed)
    - will impede compiler optimizations => cant do move semantics, causes copy semantics

_object-like macros with sub text_
- prefer constant variable over preprocessor macros => 3 problems
    1. dont follow c++ scoping rules => can cause compilation errors
    2. harder to debug => compiler & debugger nvr see the macro becpz they will be sub-ed
    3. are different from normal c++ code, causes inadvertent errors

_extern_
- using const variable thorughout a multi-file program
    - normal variables are `extern` by default, but const is not => need to declare with extern for external linkage
    - declare in central location so multiple files can use

_type qualifiers_
- type qualifiers - keyword applied to a type that modifies how that type behaves
    - i.e. const => declares a constant variable (aka const type qualifier)
- as of c++23, it has 2 type qualifiers `const` & `volatile`
    - `cv-unqualified` type - type with no type qualifiers (i.e. int)
    - `cv-qualified` type - type with 1 or more type qualifiers (i.e. cosnt int)
    - `possibly cv-qualified` type - type that may be `cv-unqualified` or `cv-qualified`

## chp 5.2: literals

- literals/ literal constants - cannot be redefined
- literal suffixes - used to change the type of a literal by adding a suffix (when the default type of a literal is not as desired)
    i.e. `u` => unsigned int, or `s` => std::string, or `sv` => std::string_view
- string literals - collection of sequential chars to represent text
    - placed between double quotes "
    - C strings / C-style strings have implicit null terminator => used to determine where the string ends
    - unlike other literals (which are values & not objects), C string literals are const objects created at the start of the program & exist for the entire program
    - unlike C strings, std::string & std::string_view literals create temp objs; they must be used immediately & are destroyed at the end of the full expression 
- magic numbers
    - magic number - literal that has unclear meaning or may need to be changed later
    - avoid magic numbers, use constexpr instead

## chp 5.3: numeral systems (decimal binary hexadecimal & octal)
* just explanations on how the different numeral systems are calculated
    - binary base 2
    - hexadecimal base 16 (4 bits each) => hence need 2 hex for 1 byte, 8 hex for 32 bits (4 bytes)

## chp 5.4: optimization & `as-if` rule

- optimization - process of modifying SW to make it more efficient
- profiler - program that measures how long various parts of the program take to run
- optimizer - program that optimizes another program
    optimizing compilers enables devs to focus on writing code that is readable & maintainable without sacrificing performance
- _as-if_ rule - says that compiler can modify a program however it likes as long as those modifications dont affect a program's "observerable behavior"
    - an exception: unnecessary calls to copy (or move) constructor can be elided(omitted) even if those constructors haveobservable behavior
    - there are variety of techniques, different compilers optimize differently
- compile time evaluation - fully or partially evaluating certain expression at compile-time
    - resulting executables are faster & smaller
_3 optimization techniques_
- constant folding - optimization technique where compiler replaces expressions that have literal operands with result of the expression
- constant propagation - optimization technique where compiler replaces variables known to have constant values with their values
    => removes the need for the program to go out to MEM to fetch the value (embedded directly in the insn)
- dead code elimination - optimization technique where compiler removes code that may be executed but has no effect on the program's behavior

```cpp
// 1. constant folding
int x {3 + 4}; // 3+4 is evaluated at compile time & becomes the e.g.2 below
cout << x;

// 2. constant propagation
int x{7}; // x is not used, & is ultimately removed
cout << x;
// becomes the e.g.3 below since x's value can be sub-ed

// 3. dead code elimination
int x{7}; // x is not used, & is ultimately removed
cout << 7;
```

- optimizations make programs harder to debug
- compile time vs runtime constants
    - compile time constant - value known at compile time (i.e. literals, constant objs whose initializers are compile-time constants)
    - runtime constant - value determined in a runtime context (i.e. constant func params, constant objs whose initializeres are non-constants or runtime constants)

## chp 5.5: constant expression
## chp 5.6: constexpr

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