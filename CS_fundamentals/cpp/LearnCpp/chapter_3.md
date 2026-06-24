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

## chp 3.6: using an integrated debugger

debugger - a computer program that allows the programmer to control how another program executes & examine the program state while the program is running
    - allows precise control of the execution of the program
    - ability to view (& modify) the program's state

_for vscode users_

## chp 3.7: 
## chp 3.8: 
## chp 3.9: 
## chp 3.10: 