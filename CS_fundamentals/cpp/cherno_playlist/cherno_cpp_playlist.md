(skip Episode 1- Episode 4)

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 5: how cpp works

content covered:

TODO: 

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 6: how the cpp compiler works?

content covered:
## Compilation + linking
## files & translation unit
## preprocesing
## constant folding + optimization

# -------------------------------------------------------------------------------------------------
## Compilation + linking
2 main operations need 
1. compiling - takes 
    - preprocess code
    - tokenizing, parsing, constant folding etc. => abstract syntax tree created
    - use ast to analyze src code & optimize
2. linking (discuss in another notes file)

# -------------------------------------------------------------------------------------------------
## files & translation unit
- each cpp file compiled -> 1 translation_unit -> results in object file
- cpp dont care about files; unlike in java
    * in java, class name ties to file name, folder hierarchy ties to package => java expects certain files to exist
- .c, .h, .cpp -> default conventions; compiler treats these files according to how it knows to
    - could even have .joe files & then tell the compiler to treat it as a .cpp file => __files have no meaning__
- when .cpp is inputted, compiler will treat it as a single __translation unit__
    - 1 transaltion unit produces __1 object file__
    - its actually quite common to include __many cpp files in 1 cpp files__ => and only compile 1 cpp file => then __only 1 translation unit__ is produced
    - __cpp file != translation unit__

# -------------------------------------------------------------------------------------------------
## preprocesing
- preprocessing occurs b4 compilation
- preprocessing statements: `#inlcude`, `#define`, `#if`

- `#include` for header files
    - compiler opens the target file & paste all the code inside that file, into the current file
    - i.e.
        - this example literally inserts the end brace => can sest preprocess to a file and see the actual file to be compiled `.i` file
        ```cpp
        // in main.cpp
        int Multiply(int a, int b) {
            int result = a * b;
            return result
        #include<"EndBrace.h">
        
        // in EndBrace.h
        }
        ```
    - hence, cpp files that include #include<iostream> will be huge because its alot of code

- `#define`
    - i.e. this literally subs Cherno into the INTEGER type
    ```cpp
    #define INTEGER Cherno
    INTEGER Multiply(int a, int b) {
        INTEGER result = a * b;
        return result
    #include<"EndBrace.h">
    ```
- `#if` - include or exclude file

# -------------------------------------------------------------------------------------------------
## constant folding + optimization
- constant arithmetic operations are done first before AST is generated
- this occurs even without optimization
- i.e. upon inspection of asm code, 5 * 2 is minimized to 10, no calculation occurs during runtime
    ```cpp
    int return_10() {
        return 5 * 2
    }
    ```
- compilation
    - un-optimized: -O0 fast debuggin; prioritize dev exp `g++ -O0 main.cpp -o my_program`
    - optimized
        - -O2: Standard for "Release" versions; balances speed and file size.
        - -O3: High performance; might increase the size of the executable.
        - -Os: Great for embedded systems with limited memory.

- additional optimization
    - if there is code which is not referenced => compiler can essentially even remove that instruction

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 7: Linker

content covered:

TODO: 

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 8: Variables

content covered:

TODO: 

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 9: Functions

content covered:

TODO: 

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 10: cpp Header files

content covered:

TODO: 

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 11: How to debug in cpp in vscode

content covered:

TODO: 


(skip Episode 13)

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 12, 14 & 15: Conditions & branches, Loops, Control flow

content covered:

TODO: 

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 16 & 17: Pointers & reference

content covered:

TODO: 

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 18: Class

content covered:

TODO: 

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 19: Classes vs structs

content covered:

## small difference
## backwards compatability
## semantic difference

# -------------------------------------------------------------------------------------------------
## small difference => visibility
- class members are by default private
- struct members are by default public => if u want private, need to declare the private keyword

## backwards compatability with C
- backwards compatability with C => C has no classes keyword/ concept
- workaround if this compatability did not exist: `#define struct class`

## semantic difference (usage in code)
- up to coding style/preference (here we will cover cherno's preference)
- when to use:
    - __struct__: POD (plain old data)
        i.e. mathematical vector class => is just a representation of 2 floats
        => not suppose to handle alot of functionality i.e. moving
        => can still have methods => for data manipulation
        * dont want complexity
        => dont want to use inheritance (not that struct cant use it)
    - __class__
        => to handle more complex functionality

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 20: write a cpp class

content covered:

## create Log class

# -------------------------------------------------------------------------------------------------
## create Log class
(refer to `./example_codes/src/log.cpp`)

* notes:
    - m_ => for member variables
    - logging levels decrease (lowest being the most specific, highest most generic)
        info is lvl 2 => will print lvl 0, 1 & 2: info, warning & error
        check `if (m_current_lvl >= method's lvl)` => print when current lvl is more generic(high enough) than current method
        * in my implementation, i did the opposite because i attempted to write my own & claude suggested the opposite ordering... (too lazy to change now)
        hence i checked `if (m_current_lvl <= method's lvl)`
    - enum vs class enum
        - plain enum leaks value into current scope
        - class enum encapsulates values into its own class scope

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode 21: static

content covered:

## Overview
## 1 vs 2: outside vs inside class/ struct
## 3 inside function
## Memory

# -------------------------------------------------------------------------------------------------
## Overview

the static keyword has 3 meanings, based on where their defined:

1. outside a class/ struct & function [global namespace]
2. inside a class/ struct [class/ struct]
    - static member variable & method
3. inside a function

## 1 vs 2: outside vs inside class/ struct

### 1 vs 2 elaboration

for 1, outside a class/ struct & function
- linkage of that static symbol is going to be internal => only visible to that translation unit u've defined in

for 2, inside a class
- variable will share memory with all instances of that class (across all class instance, theres only 1 instance of that static variable) => stored in 
- static method will not have object instance passed into it
    * it only has knowledge of static variables

### 1 vs 2 Examples

[static.cpp] => 1 TU

```cpp
// during linkage to actually define symbols (assigning them the address to be called from)
    // linker is not going to look outside the scope of this TU for the symbol definition

// step 1
static int s_variable = 5   // no linkage redefinition error as this is local to the TU
// step 2
int s_variable = 5       // => when static removed, this will be re-definition error; LINK2005: "int s_variable (...)" already defined in main.obj
//step 3
int s_variable = 5       // => when static removed, this will be re-definition error; LINK2005: "int s_variable (...)" already defined in main.obj
// step 4
static int s_variable; // ERROR => static keyword makes this variable local to the TU
// step 5
int function() {}; // ERROR => re definition across TUs
// step 6
static int function() {}; // fine, no re-definition
```

[main.cpp] => 1 TU

```cpp
// step 1
int s_variable = 10; // fine, no redefinition because of static in static.cpp
// step 2
int s_variable = 10; // ERROR
// step 3
extern int s_variable; // fine, below returns 5 // extern keyword => tells compiler it has external linkage (can be local or another TU)
// step 4
extern int s_variable; // ERROR => cant find hidden s_variable
// step 5
int function() {}; // ERROR => re definition across TUs
// step 6
int function() {}; // fine, no re-definition

int main() {
    std::cout << s_variable << std::endl;
    std::cin.get();
}
```

* extern is a *storage class specifier* that determines a function's linkage (visibility across files), not its data type
    its a storage class specifer that:
    1. tells compiler this is just declaration, dont set aside MEM for this variable now
    2. allows code to compile using this name even if definition hasnt been seen yet
    3. look for a symbol with this name that is visible to entire program (both local TU & outside of current TU)
    
    - storage class specifier - control object lifetime (storage duration) & where its visible(linkage)
        => static is also an example of storage class specifier
        * object lifetime => how long an object lives
        * visibility => controlled by linkage
    - class specifiers (type definitions) - refers to syntax used to define a new type
        i.e. class, struct, union, enum => all of these define new types

* main use of static is because u want to keep it local to the TU
 - you dont want the linker to pick it up & start using it in a global setting (for all TUs)

EXAMPLES:
[variables]
step 1: *static variable* in `static.cpp` + *non-static variable* in `main.cpp` => fine
step 2: *non-static variable* in `static.cpp` + *non-static variable* in `main.cpp` => ERROR: becoz now there is redefinition across TUs
step 3: *extern non-static variable (declaration only)* in `static.cpp` + *non-static variable* in `main.cpp` => fine, extern keyword + declaration only means program only has 1 definition
step 4: *extern non-static variable (declaration only)* in `static.cpp` + *static variable* in `main.cpp` => ERROR, extern keyword + declaration && static means program cant link static variable (hidden)
[functions]
step 5: *non-static function* in `static.cpp` + *non-static function* in `main.cpp` => ERROR: becoz now there is redefinition across TUs (similar to step 2)
step 6: *non-static function* in `static.cpp` + *static function* in `main.cpp` => fine: becoz now there is NO redefinition across TUs (similar to step 1)

## 3 inside function

- similar to class/ struct, its memory is dependent on the entity (function)
    - if function is linked across multiple TUs, it can be used across all TUs
    - if function is also static, then entire static function & static variable is only visible in current TU

```cpp
// main.cpp
int function() {
    static variable = 1;
    variable++;
    std::cout << variable << std::endl;
}
function() // prints 2

// other.cpp
function() // what does this print? 3!
```

## Memory

* [IMPT!!] static variable for all 3 scenarios is actually stored on the __data segment__!!
    - they are stored on the data segment for the entire duration of the program
    - never popped off the stack & never dynamically allocated during runtime

    * THUS static w.r.t `TU` & `linkage` is about visibility of values,
        vs memory management is about where the memory is stored

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# Episode __: ___

content covered:

TODO: 