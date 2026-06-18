# LLDB

`clang++ -g -std=c++17 seg.cpp -o prog`     -g flag tells the compiler to debug in debug mode
`lldb ./executable`                         execute with lldb

help    - see help menu
run     - launch execution in the debugger/ run program (gives stop reason; points to filename & line number where it crashed)
target create <program_name/filepath>       - create a target for the debugger to run
b <line>      - insert breakpoint at line of (1) current src file assuming the file of the stack frame ur currently at, or (2) file containing main if the program hasnt started, or (3) set at all files at line 10 if its ambigious
                parameters will already have values initialized
b <function>      - insert breakpoint at the entry point of the function 
b <file.cpp:line_num>    - inserts breakpoint at the line number in that file
* note to insert breakpoint after `target create`, but before running
list / l <line_number>        - list lines of code from that line number
list                        - each time u click this, it displays a continuation of lines of code from where the debugger left off
bt              - backtrace (see function call stack)
frame select / f    - prints the current frame with meta data (surrounding code)
frame variable
p       - print
p *this     - print member variables of current instance
expr <code>     - executes code using the current active frame / evaluates expression in the acive frame
finish          - run remaining lines of current function, execute return, pause at the next line after the function call in the parent function
gui 