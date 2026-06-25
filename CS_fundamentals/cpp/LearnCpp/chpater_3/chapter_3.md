# chapter 3: debugging

## chp 3.1: skip
## chp 3.2: skip
## chp 3.3: skip
## chp 3.4: basic debugging tactics

- use `std::cerr` instead of `std::cout` => `std::cerr` is unbuffered & will immediately print debug message

## chp 3.5: more debugging tactics

- conditionalizing debug statements using preprocessor directives:
    ```cpp
    #include <iostream>

    #define ENABLE_DEBUG // comment this out to disable debugging

    int getUserInput() {
        #ifdef ENABLE_DEBUG
        std::cerr << "getUserInput() called\n"; // is only printed when ENABLE_DEBUG is defined
        #endif
    }
    ```
- use logger & log files. C++ contains an output stream `std::clog` intended for writing logging info (by default writes to std error stream `std::cerr`)
    can also use plog logger, implemented as a set of header file so its ez to include it anywhere

- use debuggers (explained in upcoming chapters)

## chp 3.6: using an integrated debugger

debugger - a computer program that allows the programmer to control how another program executes & examine the program state while the program is running
    - allows precise control of the execution of the program
    - ability to view (& modify) the program's state

_for vscode users_
open command palette > `c/c++: add debug configuration` (need intellisense engine enabled; created a shortcut for it) > choose `c/c++: build & debug active file`

run - run the program (F5)
step over - executes the next statement in the normal execution path of the program (F10)
step into - enter function calls and execute them line by line (F11)
step out - executes all remaining code in the current function (shift + F11)

## chp 3.7: running & breakpoints

- run to cursor - runs program until a statement;
    can be accessed while already debugging a program;
    right-click a statement in the code & choose `run to cursor`
- continue (F5) - continues running the program until termination
- start(F5) - same as continue but starts from the beginning of the program;
    can only be invoked when not already in a debug session
- breakpoints - special market that tells debugger to stop execution of the program at the breakpoint
    notice that in the breakpoints panel/ toolbar there is blue checkboxes to disable/enable specific breakpoints
    then there is the red circle that enables / disables ALL breakpoints in 1 click
    you can clear all breakpoints in 1 click as well
- set next statement - jump to execute some other statement by skipping some code;
    right-click & click on `jump to cursor`

## chp 3.8: watching variables

watching a variable - process of inspecting the value of a variable while the program is executing in debug mode
quick watch - know the value of a variable at a particular point in time
watch window - window to add variables where you'd like to continually inspect
    on vscode, its docked on the left above the call stack
    typically 2 ways to add variables to the watch window:
    1. in the watch window, type in the variable name
    2. in the code window, right click on the variable & choose `add watch`

- set breakpoint on watched variables
some debuggers allow this, & this causes the program to stop execution whenever the value of that variable changes

- watch window can evaluate expressions
watch window allows you to evaluate simple expressions

## chp 3.9: call stack

call stack - list of all active functions that have been called to get to the current point of execution
    it includes:
    - an entry for each function called
    - line of code to return to when the function is done
    when new function is called, its added to top of the call stack
call stack window - debugger window showing the current call stack

- line numbers after the function names
they show the next line to be executed in each function
top entry(current executing function) - displays next line to execute when execution resumes
remaining entries - line number represents the next statement that will execute after the current executing function is returned to

## chp 3.10: finding issues: methods

refactoring code - process of making structural changes without changing its behavior
defensive programming - practice where programmer tries to anticipate all the ways the SW can be misused & mitigate them
static analysis tools / linters - programs that analyze src code to identify semantic issues
    static means it analyzes without executing the code
    some recommended tools include:
    (free)
    - clang-tidy
    - cpplint
    - cppcheck => already integrated into Code::Blocks
    - SonarLint
    (paid)
    - Coverity
    - SonarQube
