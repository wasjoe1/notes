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

# GDB

file <program_name/filepath>
catch throw => pauses execution when an exception is throw (not very reliable when execution is spawned off in a separate thread)
break __cxa_throw => more reliable
info b      => returns all breakpoints
delete      => deletes all breakpoints

to restart a debugging session:
kill    => kill the current process running under this gdb session
quit

to catch the real exception from `rethrow` in coroutines:
b __cxa_throw
run
bt

* if you bt without setting breakpoint on `cxa_throw`, then the exception is only caught at the main thread

`b __cxa_throw` vs `catch throw`
- `catch throw` - works by hooking into a probe point (DTrace/ SystemTap static tracepoint) [GDB-level]
    - libstdc++ optionally embeds these probe points
    - whether these probe points exists depends on how libstdc++ was compiled => might not always work
    * i.e. exceptions originating from non-main thread, execution will just skip these catchpoints
- `b __cxa_throw` - actual c++ ABI function [ABI-level]
    - actual c++ ABI function that every single throw expression in c++ compiles down to calling, regardless of exception type, thread, compiler flags or libstdc++ build options
    - is defined in `libstdc++abi` => always present
    - GDB patches a `INT3` (x86 trap instruction) at that address & execution must stop there (how GDB implements `__cxa_throw`)
    - on other platforms, GDB/ LLDB patches a breakpoint at wtv platform's trap instruction is (ARM64 uses `BRK #0` instead of `INT3`)
    * ABI (application binary interface) for c++ defines how compiled code (functions, classes & variables) interacts at the machine level
        (i.e. name mangling - how it encodes parameteres into unique binary names, calling conventions, obj layout, exception handling - low level mechanics of throwing & catching exceptions etc.)