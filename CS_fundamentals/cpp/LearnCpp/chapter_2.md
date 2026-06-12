# chapter 2: functions & files

## chp 2.1: intro to functions

- functions provide a way to split programs into smaller modular chunks that are easier to organize, test & use
- _user-defined functions_ - functions written by yourself
- _function call_ - tells the CPU to interrupt the current function & execute another function
- _caller_ - function initiating the function call
- _callee_ - function being called
- _invocation_ - function call (caller invoking the callee)

_function header_ - tells compiler about the existence of a function; contains function name & other info
_function body_ - curly braces + statements in between them

nested functions - NOT SUPPORTED in C++

* nomenclature - refers to the naming system & terminology used by programmers

## chp 2.2: value-returning functions

- COMMON misconception: `main()` always executes first -- it doesnt!
    => global variables are initialized prior to main()
    => if the initializer for global variables invokes a function, the function will execute prior to `main()`

- _status code_ / exit code - signals whether program was successful or no
    - using ints
        => 0 - success
        => non-zero - indicate failure    
    - by #including <cstdlib>
        => 0 & EXIT_SUCCESS - success
        => EXIT_FAILURE - fail
    - status codes are passed back to the OS, & the OS typically makes the status code available to the caller program (parent program which called the child program returning the status code)

- main() implicitly returns 0 if no return statement is provided
- functions can only reutrn a single value => use pairs or tuples if you want multiple return values

## chp 2.3: void functions

- dont need return statement
- void functions cant be used in expressions that require a value (i.e. `std::cout << PrintNothing(); // compile error as PrintNothing return type is void`)
- returning value from a void function is also compile error

## chp 2.4: function parameters & arguments

_parameter_ - variable used in the header of a function; they are initialized with a value provided by the caller of a function
_argument_ - value that is passed from the caller to the function when function call is invoked

during function call
- all parameters of the functions are created as variables
- (pass by value) the value of each of the arguments are *copied* into the matching paramter (copy initialization)
- _value paramters_ - function parameters that utilize pass by value

* note that C++ does not have a universal left-to-right evalutaion rule => compiler is legally allowed to evaluate parts of a statement in any order to find most efficient

_unreferenced paramters_ - paramters not used in the body of the function (typically receive warning)
_unnamed paramters_ - in function definition, the parameter's name is optional; name not used in the body

* unreferenced parameters usage:
    1. backwards compatability: when function is updated in some way where param is no longer used but we dont want to break legacy code
    2. overload i.e. ++ & -- have prefix & postfix variants, & unreferenced parameters help us to determine which variant is being called

## chp 2.5: local scope & temporary objects

_local variables_ - variables defined inside the body of a function

_lifetime_ - parameters & local variables are destroyed at the end of the function; they are destroyed in the opposite order of creation
```cpp
int add(int x, int y) // x and y created and initialized here
{
    int z{ x + y };   // z created and initialized here

    return z;
} // z, y, and x destroyed here
```

_scope_ - an identifier's scope determines where the identifier can be seen & used within the src code
_out of scope_ - when identifier cant be seen & used
* scope is compile-time property & trying to use identifier when it is not in scope results in compile error
_local scope_ - local variable has local scope

_going out of scope_ - applied to objects rather than identifiers

scope example:
```cpp
#include <iostream>

int add(int x, int y) // add's x and y are created and enter scope here
{
    // add's x and y are visible/usable within this function only
    return x + y;
} // add's y and x go out of scope and are destroyed here

int main()
{
    int x{ 5 }; // main's x is created, initialized, and enters scope here
    int y{ 6 }; // main's y is created, initialized, and enters scope here

    // main's x and y are usable within this function only
    std::cout << add(x, y) << '\n'; // calls function add() with x=5 and y=6

    return 0;
} // main's y and x go out of scope and are destroyed here
```

- main() & add()'s x & y variables are separate identifiers in their own local scopes
- add & main's scopes dont overlap & its always clear to the compiler which x & y are being called => you cant reference main's local variables inside add's scope

_temporary object_ / _anonymous object_ - unnamed object used to hold a value that is only needed for a short period of time
    => are generated by the compiler when they are required

example of temp object being created:
```cpp
#include <iostream>

int getValueFromUser()
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;

	return input; // return the value of input back to the caller, BUT input is destroyed at the end of the funciton call
}

int main()
{
	std::cout << getValueFromUser() << '\n'; // where does the returned value get stored?

	return 0;
}
```

- `getValueFromUser()` returns the value stored in local variable `input` back to the caller
- because `input` is destroyed at the ned of the function, the caller receives a copy of the value it can use even after input is destroyed => where is this value stored?
- return value is stored in a *temporary object*, then its passed to the variable outside the function

* temporary objects have no scope
* they are destroyed at the end of the full expression => they are always destroyed before the next statement executes
* in our example `std::cout << getValueFromUser() << '\n'`, once this is executed, _temp object created to hold value_ from `getValueFromUser()` is destroyed
* in moden cpp, the compiler has many tricks to avoid generating temporaries where previously it would have needed to
    - i.e. it could skip creating the temporary & just initialize the variable directly with the return value (URVO & NRVO)

## chp 2.6: why useful & using effectively (skip)
## chp 2.7: forward declarations & definitions

- c++ doesnt do function hoisting (move function declarations to the top of the current scope) - compilers compiles code sequentially

_forward declaration_ - tells compiler about the existence of an identifier before actually defining the identifier
    => compiler can check we're calling a function call correctly even if it doesnt yet know how the function is defined
    => allows devs to define functions in an order-agnostic manner
_function declaration_ / _function prototype_ - used to write a forward declaration (i.e. `int add(int x, int y);`)

- forward declarations can have unnamed parameters; but are preferred to be named

order-agnostic manner:
- 2 functions calling each other
- resolve _circular dependencies_

### forward declaration - compile & link
- if function is forward declared but never defined, it still compiles
    - if function is never called, no error
    - if function is called, compiler is okay, BUT linker will complain -- linker cant resolve the function call (it cant find the definition)

### declaration vs definition
_declaration_ - tells compiler about the existence of an identifier & its type
_definition_ - a declaration that actually implements (for functions & types) or instantiates (for variables) the identifier
_pure declaration_ - a declaration that isnt a definition (no body)
_initialization_ - provides an initial value for a defined object

* all definitions are declarations => `int x;` is both a definition & declaration
* BUT not all declarations are definitions
* however, the term "declaration" is commonly used to mean "pure declaration" & "definition" is used for anything that is both a definition & a declaration

- in most cases, a declaration is sufficient to tell the compiler an identifier is being used properly (i.e. calling `add(5, 6)` just requires its forward declaration)

### ODR (one definition rule)

1. within a _file_, each function, variable, type or template in a given scope can only have 1 definition; definitions occurring in different scopes (i.e. local variables) do not violate this rule
2. within a _program_ - each function or variable in a given scope can only have 1 definition; this is coz programs can more than 1 file. functions & variables not visible to the linker are excluded from this (_internal linkage_)
2. _types_, _templates_, _inline functions_ & _inline variables_


* inline & static(global) & extern:
_extern_ - tells the compiler that a variable exists somewhere else & dont worry about it (forward declaration)
_static (global)_ - makes variable declared as static in global scope hidden from the linker (other.cpp cant use extern to access it)
_inline_ - a directive to the linker telling the compiler that a function or variable can be defined in multiple TUs without causing a "multiple definition" linker error
    => doesnt replace code with constants


## chp 2.8: programs with multiple code files?

to compile multiple files into 1 program: `g++ main.cpp add.cpp -o main`
* note that 1 program can only have 1 `main()` function (if program has multiple TUs / .cpp files, there should be only 1 `main()` out of all the files/ TUs)

_compilation & linking_
- compiler compiles each file individually, does not know the contents of other code files
- when changing a src file, only that src file needs to be recompiled

- forward declaration is used to tell the compiler that function `add(...)` is defined in another TU (add.cpp), then the linker will later link the definitions with this TU
    => we are able to give files access to functions that live in another file

## chp 2.9: naming collisions & namespaces

- all identifiers have to be non-ambiguous => if 2 identifiers are identical, the compiler or linker cant tell them apart => results in _naming collision_ / _name conflict_
    => i.e. A.cpp & B.cpp both have the function defined `int MyFoo();`

_scope region_ - area of src code where all declared identifiers are considered distinct from names declared in other scopes
    => 2 identifiers with the same name can be declared in separate scope regions
    => within a scope regionm all identifiers must be unique
    => an e.g. is a _function body_ (its a scope region) where 2 identically named identifiers can be defined in separate functions
_name spaces_ - provide another type of scope region (_namespace scope_) that allows you to declare or define names inside of it for the purpose of disambiguation
    => names declared in a namespace are isolated from names declared in other scopes (i.e. 2 functions with identical names can be declared in different namespaces)
_global namespace_ - any class, function or namespace is implicitly considered part of the global namespace
_std namespace_ - namespace for C++'s standard library
    => C++'s standard library variables & functions used to not be part of a namespce -- this was bad as future versions of C++ would conflict with existing code
    => decide to throw all the variables & functions into a namespace

### few ways to use namespace - specify get identifiers from namespace

1. explicit namespace qualifier `std::__`
    `::` scope resolution operator - identifier to the left identifies the namespace, & name to the right is contained inside that namespace
2. using namespace std (avoid)
    _using-directive_ `using namespace std` - makes the names visible as if they were declared in the nearest common ancestor namespace; does not copy the variables into local scope
        => compile error is only thrown when the declaration is in the same scope
    ```cpp
    #include <iostream> // imports the declaration of std::cout into the global scope

    // declaration in separate scope 1
    int main() {
        int cout = 4;
        if (true) {
            using namespace std; // this is actually fine
            cout << "hello"; // this has an error because its read as 4 << "hello"
        }
        cout = 5;
    }

    // declaration in separate scope 2
    int main() {
        using namespace std; // this is actually fine
        if (true) {
            int cout = 4;
            cout = 5; // this is actually fine
        }
    }

    // declaration in same scope
    int main() {
        using namespace std; // compilation error!
        int cout = 4;
        if (true) {
            cout = 5;
        }
    }
    ```
* _using-directive_ - is just a keyword, not a preprocessor directive

## chp 2.10: preprocessor

- prior to compilation, _preprocessing_ phase occurs by the preprocessor
- _preprocessor_ - makes changes to the text of the code file
* a side note: preprocessor was a separate program from the compiler but modern compilers may include the preprocessor

_preprocessor directives_ (typically called directives) - instructions that start with # symbol & end with a newline (not semicolon); tells the preprocessor to perform certain text manipulation tasks
- _#include_ - used to include file contents in another file
- _#define_ (macro defines) - used to create a macro
    macro - a rule that defines how input text is converted into replacement output text (there are 2 basic macro types)
    _function-like macros_ (use is generally considered unsafe)
    _object-like macros_ - defined in 2 ways; mostly seen in legacy code
        way 1: `#define IDENTIFIER`
        way 2: `#define IDENTIFIER substitution_text` - typically used to assign names to literals (no longer necessary)
            * if you need global constants & compiler is c++17 capable, prefer defining _inline constexpr global variables_ in a header file
- _object-like macros without substitution text_
    i.e. `#define USE_YEN`
    - generally considered acceptable to use (to help out in conditionaly compilation)
- _conditionaly compilation_ - allows you to define what to compile & what not to compile
    - _#ifdef_ - check whether an identifier has been previously defined (via _#define_)
        if yes, code between _#ifdef_ & _#endif_ is executed
    - _#if 0_ - enables convenient way to "comment out" code that contains multi-line comments
    
    ```cpp
    #include <iostream>

    #define PRINT_JOE

    int main()
    {
    #ifdef PRINT_JOE
        std::cout << "Joe\n"; // will be compiled since PRINT_JOE is defined
    #endif

    #ifdef PRINT_BOB
        std::cout << "Bob\n"; // will be excluded since PRINT_BOB is not defined
    #endif

        return 0;
    }
    ```


## chp 2.11: header files

### basics & best practices
- created to solve the issue of having to include too many forward declarations (i.e. total of 100 identifiers that needs to be used all in 1 file that came from another file)
- header file's content are added to .cpp file during pre-processing phase
- typically avoid putting function & variable definitions in header files (for now)
- generally dont include multiple `.cpp` files
    => changing 1 src .cpp file will cause re-compilation of both .cpp files

### angled brackets vs double quotes
    - angled brackets: telling preprocessor that the header file is not one we wrote; lookfor the header only in the directories specificed by the `include directories`
        => _include directories_ are configured as part of the project's / IDE/ compiler settings & typically default to directories containing header files that come with the compiler or OS
        => preprocessor will not search for header files in the project's src code directory
    - double quotes: header file is one that we wrote; preprocessor first looks for header file in current directory, if it cant be found, it will then search the `include directories`
    * what if header file is not part of current directory?
        - use relative path `#include "src/my_header.h"`
        - add src to include directories, add this into CMakeLists.txt: `target_include_directories(my_project_name PRIVATE src)`
            if compiling using the CLI, add -I flag followed by the path to the dir: `g++ main.cpp -I./src -o my_program`

### transitive includes

- a file `A.cpp` may include `Main.h` which within `Main.h`, also includes `Other.h`
- this additional header files are called _transitive includes_ - included implicitly rather than explicitly
- you should not rely on _transitive includes_ & should include both `Main.h` & `Other.h` in `A.cpp`, as `Main.h` may change over time & remove `Other.h`

### circular dependencies

what if file A includes file B but file B also includes file A?

i.e.
```cpp

// in Player.h
#ifndef PLAYER_H
#define PLAYER_H

#include "Weapon.h" // Player needs to know about Weapon

class Player {
    Weapon* currentWeapon; // Needs Weapon definition
    int health;
public:
    void takeDamage(int amount);
};
#endif

// in Weapon.h
#ifndef WEAPON_H
#define WEAPON_H

#include "Player.h" // Weapon needs to know about Player

class Weapon {
    Player* owner; // Needs Player definition
    int damage;
public:
    void attack() {
        owner->takeDamage(damage); 
    }
};

#endif
```

- WRONG:
    - when main.cpp hits `#includes "Player.h"` it opens Player.h (defines PLAYER_H) -> opens Weapon.h (defines WAEPON_H) -> opens Player.h (sees defined PLAYER_H, skips)
    - preprocessor returns to Weapon.h & tries to compile `Player* owner;`
    - compiler fails `unknown type name 'Player'` because Weapon.h tried to use Player before the compiler could see Player's definition

- CORRECT: proper way is to use forward declarations & not include a header inside another header. the definition is then inside a seaparate .cpp file (see below)

```cpp

// in Player.h
#ifndef PLAYER_H
#define PLAYER_H

#include "Weapon.h" // Player needs to know about Weapon

class Player {
    Weapon* currentWeapon; // Needs Weapon definition
    int health;
public:
    void takeDamage(int amount);
};
#endif

// in Weapon.h
#ifndef WEAPON_H
#define WEAPON_H

// REMOVED: #include "Player.h"

class Player; // FORWARD DECLARATION: Breaks the circle!

class Weapon {
    Player* owner; // Legal! The compiler knows how big a pointer is.
    int damage;
public:
    void attack(); // Move the actual implementation to a .cpp file
};
#endif
```

## chp 2.12: header guards

- duplicate definition problem: variable / function can only have 1 definition (ODR) in the program; program with > 1 definition will cause compile error
- _header guards_ / _include guard_ - conditional compilation directives
    - goal: prevent a code file from receiving more than 1 copy of a guarded header (using the transitive example, `A.cpp` will only receive `Main.h` & `Other.h` once)
    - i.e.
    ```cpp
    #ifndef SOME_UNIQUE_NAME_HERE
    #define SOME_UNIQUE_NAME_HERE
    // your declarations (and certain types of definitions) here
    #endif
    ```
* BUT header guards do not prevent a given header file from being included into separate code files (i.e. `A.cpp` uses `Main.h` & `B.cpp` uses `Main.h`)
    - if Main.h has a definition (variable or function), both A.cpp & B.cpp would have defined the same identifier twice
    - custom types on the other hand, are typically defined in header files
        => BECAUSE compiler cant allocate MEM for a class or check its member functions unless it sees the full definition insde that TU (hence you have to define the custom type in the .h file & not separate .cpp)
        => forward declarations is used when you are just using a pointer of that type (since a pointer is always the same size no matter its type)

- `#pragma once` - is implementation specific
    - most prefer it now because it is easier & less error-prone
    - is however not defined by the C++ standard & is possible that some compilers dont implement it


## chp 2.13: design program (skip)