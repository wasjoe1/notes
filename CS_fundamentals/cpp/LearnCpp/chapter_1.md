# chapter 1: basics

## chp 1.1: statements & structure of a program

computer _program_ - made up of sequence of instructions
_statement_ - type of instruction that performs actions; (most) end in semicolons`;`; may be compiled into many machine language instructions
_functions_ - a unit of grouped statements
_text_ / plain text / string - sequence of characters
_control character_ - characters with special meaning to the computer system (i.e. `escape`, `tab`, `backspace`)

program runs by executing main() - (dont actually need to name it main, but you will have to change the entry point in your configs)
#include is a preprocessor directive
blank line is ignored by the compiler, exists to make the program more readable to humands
std::cout - stands for character output

## chp 1.2: comments

- 2 types of comments: single-line & multi-line
- its okay to nest single-line comments inside multi-line comments, BUT DONT nest multi-line comments with multi-line comments
- 3 proper ways to use comments:
    ```cpp
    // (1) At the top of file to describe what the program does

    int main() {
        /* (2) Inside a function to describe how code accomplishes its goal */
        // this is allowed too:
        // 1) ..
        // 2) ..

        // (3) statement level to describe why the code does something
        int x = 0;
    }
    ```

## chp 1.3: intro to objects & variables

chapter touches on how to define a variable that can store values

_data_ - information that can be moved, proessed or stored; programs are instructions that manipulate data
_value_ - single piece of data
_character_ values - value in single-quotes
text / _string_ values - value in double-quotes
_numeric_ values - not quoted
_literals_ - values placed directly into src code

_object_ - represents a region of storage(in RAM or registers); stores a value in MEM; excludes functions
objects can be unnamed, but we typically name them => naming objects enables us to refer to them later
_variable_ - named objects; object with name(identifier)

variable _definition_ [compile-time] - a type of declaration statement (i.e. int x; // defines a variable x of type int) that occurs during compilation
_variable creation_ [runtime] - at runtime, each object is given a storage location (RAM/ Cpu register) that can be used to store values
allocation - process of reserving storage for an object's use
* once allocation is done, object is created & can be used

## chp 1.4: variable assignment & initialization

### _(definition + assignment) vs initialization_
- definition + assignment
    ```cpp
    // 2 statements version:
    int width; // definition (MEM allocated)
    width = 5; // (copy) assignment

    // 1 statement: initialization
    int width{5}; // define & initialize with value 5
    ```
- initializations
    - 5 common forms of initialization
        ```cpp
        int a; // default initialization (no initializer) => MEM still allocated but garbage value init-ed
        // traditional initialization
        int b = 5; // copy-initialization / copy initialization (initial value after equals sign)
        int c(6); // direct-initialization / direct initialization (initial value in paranthesis)
        // modern initialization
        int d{7}; // list-initialization / list initialization / brace initialization / uniform initialization / direct-list-initialization (initial value in braces)
        int e{}; // value-initialization / value initialization (empty braces)
        ```
        * as of cpp17, copy, direct & direct-list initializations behave identically in most cases (edege cases to be brought up later)
    - other (notable) initializations
        - aggregate initialization
        - copy-list-initialization (discussed here)
        - reference initialization
        - static-initialization, constant-initialization & dynamic-initialization
        - zero-initialization (discussed here)

    - _default initialization_ `int a;` - leaves variable with garbage value
    - _copy initialization_ `int a = 5;` - inefficient for *some complex types*, also used whenever values are implicitly copied (i.e. when passing args into a function by value, returning from function by value, catching exceptions by value)
        => inefficiency only occurs for complex types (not primitive types, i.e. std::vector)
        => `MyObject obj = otherObj` inefficiency is because `otherObj` is created in a temp object before being copy or moved to the temp's final variable obj
    - _direct initialization_ `int a(5);` - allowed for efficient initialization of complex objects, but was superseded by *list-initialization*
    - _list-initialization_ / _brace initialization_ `int a{5};`
        - disallows narrowing conversions - if a variable is initialized with a value it cant safely hold, compiler produces a compilation error / warning
        => this only occurs for the initialization, not assignment afterwards
    - _value initialization & zero initialization_
        in cases where value initialization does *zeroing* -- variable is initialized to 0 (or whatever value closest to 0), this is called *zero-initialization*
        for class types, value-initialization may instead initialize object to predefined default values (may be non-zero)

### _initialization vs instantiation_
_instantiation_ - fancy word meaning variable was created(_allocated_) & _initialized_; _allocated_ + _initialized_
* term is often used for class type objects, but may occassionally be applied to objects of other types as well

### `[[maybe_unused]]` attribute

when compiling strict language warnings as errors, unused variables will be flagged as errors & sometimes we have good reasons to keep those unused variables in

```cpp
#include <iostream>

int main() {
    [[maybe_unused]] double pi {3.14159};
    [[maybe_unused]] double gravity {9.8};
    std::cout << pi '\n';
    // compiler wont complain about gravity not being used
}
```