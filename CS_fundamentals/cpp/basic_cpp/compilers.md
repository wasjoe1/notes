# Example code
# Syntax to compile & execute code
# What a C++ compiler does?
# g++ vs clang++
# C++ debuggers (gdb/ lldb)


# Example code that prints out hello world
#include <iostream>  // lets us use std::cout

int main() {
    std::cout << "Hello, world!" << std::endl;
    return 0;  // optional, but good practice
}

# Syntax to compile & execute code
```bash
# clang
clang++ _filename_.cpp -o _executable_filename_
./_executable_filename_

# g++
g++ _filename_.cpp -o _executable_filename_
./_executable_filename_
```

# What a C++ compiler does?
- parses cpp code
- checkes types, templates, errors
- optimizes code
- generates machine code
- links everything into an executable

* there are multiple c++ compilers available to be used, but ones that are popular on macOS are g++ & clang++

# g++ vs clang++
clang++ is the default compiler on macOS => apple ships Clang with macOS/Xcode
g++ --version => on macOS, this is Clang pretending to be g++; unless u manually install GCC via homebrew
```bash
joechua@Chuas-Air-3 notes % which g++
/usr/bin/g++
joechua@Chuas-Air-3 notes % which clang
/usr/bin/clang
joechua@Chuas-Air-3 notes % g++ --version           # use g++ version to really check the underlying compiler of g++ (in this case clang is still the underlying compiler)
Apple clang version 14.0.3 (clang-1403.0.22.14.1)
Target: arm64-apple-darwin22.5.0
Thread model: posix
InstalledDir: /Library/Developer/CommandLineTools/usr/bin
```

clang
- error msgs: more readable error msgs; easier to understand
- compilation speed: often compiles faster, esply for large projs
- performance of generated code: slightly faster on macOS (macOS ARM i.e. M1, M2, M3)

GCC
- error msgs: more cryptic (difficult to understand) & verbose
- compilation speed: GCC's optimizer is sometimes slower
- performance of generated code: sometimes faster on linux, HPC workloads

- std lib implementation: both use libc++ (apple's C++ std lib) on macOS
- C++ std support: both support modern C++ (C++17/20/23)

* use GCC if (1) compiling linux-specific code; (2) building smt specifically requiring GCC; (3) require GCC speed measurements
* use clang (1) better error msgs; (2) better optimized for ARM macs; (3) built into macOS & no need to download GCC

# C++ debuggers (gdb & lldb)
gdb (GNU debugger)
lldb (low-level debugger)

gdb
- Part of the GNU toolchain (like GCC)
- Used mostly on Linux
- Older but still widely used
- Not pre-installed on macOS; Hard to install on macOS because of Apple’s code-signing restrictions

lldb
- Works perfectly with Clang; Part of the LLVM toolchain (same family as Clang)
- Default debugger on macOS; Created by Apple
- Integrated into Xcode and VSCode’s C++ extensions

* lldb is what you should use on macOS!!
