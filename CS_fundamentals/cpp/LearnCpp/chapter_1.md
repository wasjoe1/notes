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
_allocation_ - process of reserving storage for an object's use; MEM allocated for variable, value might not be assigned/ initialized
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
    - _value initialization `int a{};` & zero initialization_
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

### intializing multiple variables

```cpp
int a = 5, b = 6;          // copy-initialization
int c ( 7 ), d ( 8 );      // direct-initialization
int e { 9 }, f { 10 };     // direct-list-initialization
int i {}, j {};            // value-initialization

// wrong - a has garbage values
int a, b = 5;
```

## chp 1.5: intro to iostream: _cout, cin, endl_

input/ output library (io lib) is part of the c++ std lib => used to get input from the keyboard & output data to the console
`#include <iostream>`

iostream lib contains a few `predefined variables`:
- _std::cout_ - uses insertion operator (i.e. std::cout << 4) to send text/ ints to the console to be printed
- _std::cin_ - uses extraction operator (i.e. std::cin >> name) to put input data in a variable
- _std::endl_ - is used to output a newline & flushes the buffer

### _std::cout_

- is buffered by queuing strings to be printed, and periodically flushing the buffer
- con: if program crashes & data was left in the buffer, output in the buffer will not be displayed
- pro: writing data to a buffer then transferring data in batches to an output device is typically faster (due to reducing requests to the output device)
    than always immediately transferring data to the output device

### std::endl vs \n

`std::endl` - immediately flushese the buffer
LF (linefeed character)`\n` - doesnt flush the buffer

### std::cin

- uses whitespaces (tabs, newlines, spaces) as a delimiter to mark the end of a string => it only prints/ stores the input until the character before the white space
- cin then ignores leading white spaces for the next input => so the whitespaces are never registered
- dont need to output '\n' when accepting a line of input, the user would've pressed the `enter` key & this moves the cursor to the next line

- `std::cin` is also buffered, where strings are queued to be assigned to a variable
    => if you input multiple input data in 1 shot, it will be used for multiple `std::cin >> var`
    => i.e. `std::cin >> num1;` `std::cin >> num2;` but you typed 4 5 in 1 shot, then input will be used for both requests since your initial input was buffered

extraction process
- leading whitespaces (spaces, tabs & newlines at the front of the buffer) are discarded from the input buffer => hence the whitespace was ignored for the above `4 5` input
- if the input buffer is now empty, the >> operator will wait for the user to enter more data
- operator >> then extracts as many consecutive chars until it encounters either a whitespace OR a char that is not valid for the variable being extracted
    i.e. `int x; std::cin >> x;` // user inputs 5a, returning "5a\n" thus 5 is extracted into int x, while leaving "a\n" inside the buffer

## chp 1.6: _uninitialized variables_ & _undefined behavior_

_uninitialized variables_ - variable that is not given a known value (through initialization or assignment)

- _initialized_ - object is given a known value at the point of definition
- _assignment_ - object is given a known value beyond the point of definition
- _uninitilized_ - object has not been given a known value yet
    * note that uninitialized is not the strict opposite of initialized

using uninitialized variables [dangerous]
- using values of uninitialized variables can lead to unexpected results!!
- when in debug build config, some compilers will initialize contents of MEM to some preset value -> this doesnt happen in release builds
- most modern compilers when detect usage of uninitialized variables will issue a warning / error => saw that in MSVC, it raises errors, whereas clang on mac issues warning

- _undefined behavior_ - result of executing code whose behavior is not well-defined by the c++ language

- _implementation_ - specific compiler + associated standard lib (as these are what actually implements the C++ language)
    - C++ language standard allows the implementation to determine how some aspects of the language will behave so that the compiler can choose a behavior that is efficient for a given platform
- _implementation behavior_ / _implementation-defined behavior_ -behavior that is deinfedb y the implementation is called
    - i.e. `sizeof(int)` on most platforms returns 4, but on others may produce 2

## chp 1.7: _keywords_ & _naming identifiers_

C++ reserves 92 words
_keywords_ - reserved words that has special meaning in the c++ language
_identifier_ - name of a variable / function/ type
    - cant be a keyword
    - composed of only letters, numbers & underscore
    - must begin with a letter or underscore
    - case sensitive

## chp 1.8: whitespace & basic formatting

_whitespace for formatting_
- quoted text takes the amount of whitespace literally
    i.e. `std::cout << "Hello world!";` is different than `std::cout << "Hello           world!";`
- quoted text separated by nothing but whitespces will be concatenated
    ```cpp
    std::cout << "Hello "
     "world!"; // prints "Hello world!" 
    ```
_basic formatting_
- fine to use tabs or spaces for indentation
    - proponents of using spaces: aruges that code can be precisely aligned as intended regardless of which editor or settings is used
    - proponents of using tabs: argues that one should use the character desgined to do indentation & set the width to wtv is your personal preference
- place open curly braces
    - same line: reduces amount of vertical whitespace to fit more code on a screen & dont have to scroll as much
    - next line: enhances readability to since brace pairs should always be indented at the same level
- line length - typically kept to *80 chars* or less
    - if long line is split with an operator, the operator should be placed at the start of the next line; makes it clear that subsequent lines are continuations of the previous lines
    ```cpp
    std::cout << 3 + 4
        + 5 + 6
        * 7 * 8;
    ```

## chp 1.9: intro to _literals_ & _operators_

_literal_ / _literal constant_ - fixed value inserted directly into src code; their values cant be changed

```cpp
std::cout << "hello world"; // "hello world" is a literal
int x { 5 }; // 5 is a literal
```

_operations_ involve 0 or more input values (_operands_) & produces a new value (_return_ value)
specific operation to be performed is denoted by _operator_

_nullary_ - acts on - operands
_nullary_, _binary_, _ternary_ operators

_chaining_ operators - output of 1 operator can be used as the input for another operator
_side effects_ - a function / operator that has observable effects beyong producing a return value is said to have side effects

## chp 1.10: intro to _expressions_

_expressions_ - a non-empty sequence of literals, variables, operator & function calls that returns a value [sequence]
_evaluation_ - process of executing an expression [process]
_result_ - result of the expression [return-value]

examples of expressions:
```cpp
2               // 2 is a literal that evaluates to value 2
"Hello world!"  // "Hello world!" is a literal that evaluates to text "Hello world!"
x               // x is a variable that evaluates to the value held by variable x
2 + 3           // operator+ uses operands 2 and 3 to evaluate to value 5
five()          // evaluates to the return value of function five()
x = 4 + 5;
```

## chp 1.11: summary

- just showing some bad & good examples of code, speicifically when printing out a number that we need to multiply, we dont assign it to a variable & immediately pass the expression to std::cout
    i.e. std::cout << num * 2 << std::endl;