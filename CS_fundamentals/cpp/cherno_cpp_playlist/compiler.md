# how the cpp compiler works?

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