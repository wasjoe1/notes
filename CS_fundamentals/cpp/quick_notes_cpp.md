# Quick notes

Below are unorganised notes taken while learning cpp which i have yet to categorise properly into respective folders.

# Initializations (default, direct, copy, list)
# container.insert()
# insert() efficiency (pre-allocate vs allocate on the fly)
# Threads
# implicit instantiation of undefined template
# name shadowing

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# conditional member initializer list

```cpp
class metal : public material {
public:
    metal(const color& albedo, double fuzz) : albedo(albedo), fuzz(fuzz < 1 ? fuzz : 1)
    ...
```

# -------------------------------------------------------------------------------------------------
# class vs struct default access

class is default private
struct is default public

# -------------------------------------------------------------------------------------------------
# configure presets

```yaml
{
  "version": 3,
  "configurePresets": [
    {
      "name": "base",
      "hidden": true,
      "generator": "Unix Makefiles",
      "binaryDir": "${sourceDir}/build/${presetName}"
    },
    {
      "name": "debug",
      "displayName": "Debug Config",
      "description": "Unoptimized build with full line debugging symbols",
      "inherits": "base",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug"
      }
    },
    {
      "name": "release",
      "displayName": "Release Config",
      "description": "Max speed optimized production build",
      "inherits": "base",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release"
      }
    }
  ],
  "buildPresets": [
    {
      "name": "debug",
      "configurePreset": "debug"
    },
    {
      "name": "release",
      "configurePreset": "release"
    }
  ]
}
```

```bash
# 1. Instantly configures the project as Release
cmake --preset release

# 2. Instantly builds the Release binary
cmake --build --preset release

```

# -------------------------------------------------------------------------------------------------
# debug cpp

* when writing code, i encountered a segmentation fault error. to debug this:

1. configure CMake to use debug flag
```bash
cmake -S . -B build -DCMAKE_BUIL_TYPE=Debug # this just tells cmake: -S to find the CMakeLists.txt in current folder, then -B create build files in build folder
# or
cmake -B build -DCMAKE_BUILD_TYPE=Debug # this is just a shorter more modern way of writing it (assume CmakeLists.txt is in the current folder)

# to change it back to release
cmake -B build -DCMAKE_BUILD_TYPE=Release
# this is a config of cmake. it is stored in build/CmakeCache.txt
```

2. recompile binary (remove old optimized binaries)

```bash
cmake --build build --clean-first # lean-first ensures that old optimized object files are completely deleted & overwritten
# or
cmake --build build # if ur confident that no older optimzed files are there
```

3. run debugger

```bash
lldb ../build/RayTracer
```

4. in lldb:

```bash
(lldb) bt
frame #13400: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
frame #13401: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
frame #13402: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
frame #13403: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
frame #13404: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
frame #13405: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
frame #13406: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
frame #13407: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
frame #13408: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
frame #13409: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
frame #13410: 0x0000000100003564 RayTracer`camera::render(hittable const&) + 352
frame #13411: 0x0000000100003040 RayTracer`main + 688
frame #13412: 0x00000001919f5d54
```

- note that these frames are stack frames
    => each time a fn is called a stack frame is added onto the stack
    => frame holds specific function's local variable & remembers where to return after the function is done
    add frame:
        => everytime function is called CPU pushes a new frame onto a stack
        => CPU saves a hidden variable, return address OR link register, which points to the exact memory location of the next line of code in the parent function
    pop frame(fn done):
        => CPU looks inside current frame to read hidden return address
        => current frame's MEM is removed & popped off the stack
        => function it returns to becomes the active frame (index 1 shfits up to index 0)
        => CPU jumps to that return address & continue executing

i.e. Debugger View (Top of the Stack is always #0):
[ Frame #0 (Earliest/Base): main ]           -> Knows to return to the OS
[ Frame #1 (Middle):       camera::render ] -> Knows to return to main
[ Frame #2 (Latest/Top):   ray_color ]      -> Knows to return to camera::render

## actual debugging
```bash
(lldb) bt 20
* thread #1, stop reason = EXC_BAD_ACCESS (code=2, address=0x16f603ff8)
  * frame #0: 0x00000001000041a8 RayTracer`vec3::vec3(double, double, double) + 12
    frame #1: 0x0000000100003234 RayTracer`vec3::vec3(double, double, double) + 52
    frame #2: 0x00000001000069b0 RayTracer`operator*(double, vec3 const&) + 76
    frame #3: 0x000000010000a89c RayTracer`ray::at(double) const + 40
    frame #4: 0x000000010000a710 RayTracer`sphere::hit(ray const&, interval, hit_record&) const + 368
    frame #5: 0x0000000100003864 RayTracer`hittable_list::hit(ray const&, interval, hit_record&) const + 224
    frame #6: 0x000000010000650c RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 168
    frame #7: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
    frame #8: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
    frame #9: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
    frame #10: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
    frame #11: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
    frame #12: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
    frame #13: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
    frame #14: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
    frame #15: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
    frame #16: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
    frame #17: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
    frame #18: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
    frame #19: 0x0000000100006590 RayTracer`camera::ray_color(ray const&, int, hittable const&) const + 300
(lldb) 
```

- use `bt 20` to limit output
- looking through the trace
    ray_color executes, then it calls world.hit(...)
    hittable_list::hit lops through scene objects& calls sphere::hit(...)
    sphere::hit(...) tries to calc the exact intersection point on the sphere using record.p = ray.at(double) => which creates a new vector
    but because the stack doesnt have enough space, it returns segfault error

* segmentation fault: stack overflow
    - __EXC_BAD_ACCESS__ - program tried to touch a MEM slot it wasnt allowed to
    - __code=2__ - OS sub-flag meaning *MEM protection violation*, it means the address is a real location but was locked down by OS as a *stack guard page*
    - if it was __code=1__ instead, it means *Missing page/ segmentation fault* where maybe a null pointer or random garbage data was access
    - also apple start its main thread stack MEM around `0x16fxxxxxx` so it would end around `0x16f603ff8` for an 8Mb stack window


# -------------------------------------------------------------------------------------------------
# smart pointer (shared_ptr)
```cpp
// (1) raw pointers: Old, unsafe way of dynamically allocated objects
lambertian* material_ground = new lambertian(color(0.8, 0.8, 0.0));

// (2) outdated anti-pattern
std::shared_ptr<lambertian> mat = std::shared_ptr<lambertian>(new lambertian(color(0.8, 0.8, 0.0)));

// (3) newest best approach
shared_ptr<lambertian> material_ground = make_shared<lambertian>(color(0.8, 0.8, 0.0)); shared_ptr<lambertian> material_center = make_shared<lambertian>(color(0.8, 0.8, 0.0));
```

- a shared pointer is a smart pointer that manages dynamically allocated object through ownership
- different ways of handling dynamically allocated objects:
    (1) => unsafe
    (2) => less performant & potential safety risk
    - syscall 1: `new lambertian(...)` is executed first by the program, heap MEM allocated for the object, raw pointer returned
    - syscall 2: raw pointer is then given to `shared_ptr`, smart pointer constructor then allocates heap MEM for the *control block* (entirely separate OS call)
    * 2 syscalls && potential that after raw pointer is created, error occurs, then is never cleaned up
    (3) more performant & avoids safety risk
    - syscall 1: `std::make_shared` calcs the combined size of lambertian object && hidden control block. it makes 1 req for a contiguous block of heap MEM containing both structures right next to each other
    * 1 syscall => faster to allocate MEM
    * cache locality => faster MEM lookup times when referencing counter

## elaboration on safety risk

* *new inside a function call* cna cause silent memory leaks

```cpp
process_scene(
    std::shared_ptr<lambertian>(new lambertian(color(1,1,1))),
    potential_err_function()
);
```

- compiler can reorder evaluation of function arguments
- if `new lambertian(...)` executed first, then `potential_err_function()` is executed
    => the lambertian allocation is left hanging in MEM
* this `new` keyword is very dangerous

# -------------------------------------------------------------------------------------------------
# std::abs

```cpp
bool near_zero() const {
        // auto threshold = 1e-8f => this would have returned float because of the f suffix, but we are comparing double
        double threshold = 1e-8;
        // std::fabs => returns floating point absolute value, strips away -ve sign
        // std::abs => in old cpp, we cant use this as cmath did not allow for method overloading. but modern cpp updated std::abs to have specialized version for int, long, float, double, & long double

        // is true if vector is close to 0 for all components
        return (std::abs(e[0]) < threshold) && (std::abs(e[1]) < threshold) && (std::abs(e[2]) < threshold);
    }
```

# -------------------------------------------------------------------------------------------------
# class hoisting & forward declaration

## context

- `main.cpp` includes `material.h` (`material.h` has the material class declaration & definition)
- `material.h` includes hittable.h (hittable.h uses material class)

Q. if class hoisting exists, there would be no error for hittable.h using material class
since its technically jsut delcared & defined later? but will be hoisted to the top?

Ans: Cpp *DOES NOT* have class hoisting unlike lnaguages like JS or python
    compiler reads code strictly from top to bottom

Q. what about function hoisting?

Ans: also *DOES NOT* have function hoisting

## resolve: forward declaration

```cpp
// in hittable.h
// forward delcaration
    // cpp has no class hoisting
    // forward declares the class so that current header can use it first & tells compiler to trust that definition will be provided later on
class material;

class hit_record {
public:
    point3 p;
    vec3 normal;
    shared_ptr<material> mat; // forward declared
    ...
}

// in material.h
#include hittable.h

class material {
    // (actual defn)
}

// in main
#include material.h

... code
```

in this case
- hit_record => has material pointer
- class material => takes in hit_record

* there is slight recursive relationship BUT cpp's forward declaration enforces that
with forward declarations, you can only hold the type but not do anything concrete with it
    => this makes it such that you can only start doing anything concrete once you have the actual definition

# -------------------------------------------------------------------------------------------------
# this keyword

```cpp
// normal methodd
double sphere_deg_to_rad(Sphere* const this, double deg) {...}
```

- this keyword argument is declared with const to ensure that the this pointer doesnt change what it points to

# -------------------------------------------------------------------------------------------------
# range of floating point numbers (float, double)

## float (32 bits/ 4 bytes)

## double (64 bits / 8 bytes)
What Values to Expect on Your 64-Bit Screen

code to verify:

```cpp
#include <iostream>
#include <limits>

int main() {
    // Force the console to print full floating-point precision, not rounded decimals
    std::cout.precision(std::numeric_limits<double>::max_digits10);

    // 1. Smallest POSITIVE NORMAL double (Maintains full precision)
    std::cout << "Smallest normal double: " 
              << std::numeric_limits<double>::min() << "\n";

    // 2. Absolute smallest POSITIVE SUBNORMAL double (Lowest non-zero number)
    std::cout << "Absolute smallest double: " 
              << std::numeric_limits<double>::denorm_min() << "\n";
              
    // 3. Most NEGATIVE double (Largest absolute magnitude below zero)
    std::cout << "Most negative double: " 
              << std::numeric_limits<double>::lowest() << "\n";
}
```

- Smallest Normal Double (2.22507e-308)Represented by std::numeric_limits<double>::min(). This is the smallest positive floating-point number that can be expressed with a normal lead bit in its binary significand. Any math dropping below this entry point experiences "gradual underflow," losing precision bits one by one.
- Absolute Smallest Subnormal Double (4.94066e-324)Represented by std::numeric_limits<double>::denorm_min(). This is the absolute physical limit of a 64-bit float. If a ray-sphere intersection calculation or a vector length yields a number smaller than this (e.g., 1.0e-325), the computer hardware rounds it down to an absolute 0.0.
- Most Negative Double (-1.79769e+308)Represented by std::numeric_limits<double>::lowest(). Note that std::numeric_limits<double>::min() does not mean the lowest negative number (which is a common point of confusion for beginners). If you want the negative boundary opposite to positive infinity, use .lowest().

# -------------------------------------------------------------------------------------------------
# dangerous static function

common dangerous static function trap in a single header file:

```cpp
// MyHeader.h
#pragma once
#include <iostream>

static void counterFunction() {
    static int count = 0; // local static variable to each TU
    count++;
    std::cout << "Count: " << count << "\n";
}
```

- static keyword in global function gives it internal linkage => every .cpp file that includes MyHeader.h
    will receive its own counterFunction
    => this means that `count` variable is also local to the TU, and increments in different TUs will increment separately

# -------------------------------------------------------------------------------------------------
# incomplete type error

incomplete type error - when a type is used, yet definition is not yet finished; occurs when a type that the compiler has seen a declaration but not full definition

```cpp
// common error exmple
class Node {
    Node next; // ERROR - compiler doesnt know the size of Node yet coz its still in the midst of definition
    Node* next; // fine - pointer is always fixed size (8 bytes)
}

// static member being the exception!!
class interval {
    static const interval empty, universe; // fine, static
    interval next; // ERROR - not static, will be infinite size
    interval* next; // fine, pointer
}
```

Q. why is static variable fine?
Ans:
- static class members are not part of the object's MEM => its just a blue print
- THUS they dont contribute to the size of the class instance at all => live in separate memory location
    => compiler doesnt need to know the size of interval to define the class layout

# -------------------------------------------------------------------------------------------------
# class variable (static in class)

- declaring static member (variable / method) in a class makes them a class member (variable / method)

```cpp
// test.h
class test {
public:
    double var_1, var_2; // uninitialized members
    double var_3 = 0.0; // initialized members

    static int max_value = 3; // ERROR! (1) creating static without const inside a class defn is not allowed. 
    static const int max_value = 3; // fine, (1.5)
    inline static int max_value = 3; // fine, (2)
    static int max_value; // fine, (3)

    static const interval empty, universe;

    test(double var_1, double var_2) : var_1(var_1), var_2(var_2) {} // constructor to initialized the uninitialized members
}

// test.cpp
int interval::max_dimensions = 3 // definition & initialization
```

- (1) WRONG error!
    - a static member variable is shared across all instances of a class & exists in a single memory location for the entire program
    - every TU that includes this header file would try to allocate & initialize the same variable, causing duplicate symbol errors at link time
        => rmb that even when using `#pragma once` or `ifndef`, TUs can still repeat the header files, hence static variable might be duplicated 
        => why class definition is not considered duplicate? BECOZ class defn is considered a *type defn* (no allocation of physical MEM)
            whereas a static member variable defn is a *data object defn* (has allocation of physical MEM)
- (1.5)
    1st: inlining
    - when const used, compiler sees it as a compile-time constant expression (constexpr)
    - compiler doesnt actually allocate MEM for the variable (not in runtime global MEM), compiler just search & replaces the variables with values in src code
    2nd: internal linkage => if u do smt that requires the variable to need a physical MEM address (i.e. taking its address &max OR passing by reference)
    - compiler has to assign MEM now
    - BUT compiler sees that its const & treats that memory sa completely private, specific to that TU (other TUs cant refer to this static variable)
    - this is internal linkage

    * the above explanation is for integral types(int, char, bool, etc.) -- `static const interval empty = interval{...}` will still not work
        => integral types are subset of primitive types. some e.g. of primitive types that arent integral types are: floating-point (float, double, long double), void, null_ptr etc.
        => doesnt work because non-integral class type needs actual memory & cant just substitute at compile time
- (2)
    - is basically (1.5)'s inlining explanation
- (3)
    - ensures that class static variable is only defined & initialized once across all TUs

# -------------------------------------------------------------------------------------------------
# declaration vs definition

Misconception:
- declaring `int x;` means that x is auto-initialized to 0. NO!!
- inside functions: leaves the variable uninitialized => random value is returned if u try to access it
- global variables: auto-initialized to 0
- static variables: auto-initialized to 0

* ALWAYS initialize variables explicitly during declaration!!
    => use int x = 0 to guarantee 0
    => use int x{} for value-initialization to set to 0

# -------------------------------------------------------------------------------------------------
# .clangd & .cland-format

.clangd - configures the language server (i.e. enables auto complete, go-to defn, etc. via telling it path to look for compilation etc.)
    * compile_commands.json - is the file that clangd refers to to better your project's compilation flags & tie in dependencies 
.clang-format - configures code formatting (indentation, brace style, line length, spacing etc.)
    => is the thing that runs during `Format Document` / `clang-format` 

# -------------------------------------------------------------------------------------------------
# update file's format

some common files (i.e. .clangd & .clang-format) are not recognised by the IDE
& will not have default formatting for it

1. use vscode's command palette (cmd+shift+p) + open user settings(JSON)
2. then add:
```json
"files.associations": {
    ".clangd": "yaml" // example of file ".clangd" setting it to yaml format
}
```


# -------------------------------------------------------------------------------------------------
# compilation database (compile_commands.json)

a compilation database(a json file containing compilation details) is helpful for
your language server (clangd, intellisense, etc.) to know the full include chain
(i.e. when clangd looks at a .cpp file main.cpp, & it includes `vec3.h`,
the editor looks in standard system paths but cant find vec3.h
since its installed in a custom directory.
the `compile_commands.json` file tells the language server
which paths to look to find header file, since compilation was successful)

how to generate a compilation database:
[cmake]
- Add `set(CMAKE_EXPORT_COMPILE_COMMANDS ON)` to CMakeLists.txt
    => ensure `compile_commands.json` (compilation database) is created in build folder during compilation
- re-run CMake
    => for compilation to happen
    => and for `compile_commands.json` to be generated
- point clangd to compile_commands.json by symlinking it in the project root
    => `ln -s build/compile_commands.json`
    => why? clangd searches for `compile_commands.json` by walking up directory tree from the current file you are editing (most likely in `/src`)
    OR
    => include CompileFlags in a `.clangd` file at the project root
    ```yaml
    CompileFlags:
        CompilationDatabase: build/
    ```

* go to `OUTPUT` tab and change to `clangd` in the drop down
* find the line that says compilation db was loaded (i.e. `I[09:39:43.941] Loaded compilation database from /Users/joechua/Desktop/DEV/projects_for_fun/cpp_ray_tracer/build/compile_commands.json`)

## issue resolve?

no, while the IDE is now able to recognise & resolve it for the __.cpp__ files
header files are still compiled in isolation, making no surrounding context available
    (i.e. `ASTWorker building file .../src/color.h with command inferred from .../src/main.cpp`)
    this means that clangd has no real compile command for `headers`, only for `.cpp` files

- color.h uses vec3 but never includes vec3.h
- it relies on common.h to pull it in (main.cpp includes common.h & color.h => hence color.h is able to use common.h)
- clangd anaylyzes color.h independently as compile_commands.json only has entries for .cpp files (.cpp files wont show error since it knows what its including)

* work around is just to include this in `.clangd`: `Add: [-include, /Users/joechua/Desktop/DEV/projects_for_fun/cpp_ray_tracer/cpp_ray_tracer/src/raytracer_common.h]`
    => this basically includes the common header file into every single file opened for editing (not during the actual compilation)
    => note that in production codebases, a "God header" is bad practice & should typically not be used

[g++]
- use bear to intercept your build
    => `bear -- g++ -o output main.cpp`
    => genereates compile_commands.json automatically


# -------------------------------------------------------------------------------------------------
# lldb debugger

- lldb is part of the LLVM project (for apple mac)
- native debugger for clang
- can also be used for code compiled by the GCC compiler (GNU project)

## reference material

1. beginner debugging: https://www.youtube.com/watch?v=v_C1cvo1biI
    - debugs a segfault in a simple program
    - no involve of cmake (uses raw -g flag)
2. advance debugging: https://www.youtube.com/watch?v=y3zdCa08Ndw
    - debugs a shader program
    - uses cmake
    - debug assembly

## beginner debugging

(refer to code in [debugger.cpp](./basic_cpp/debugger.cpp) to test this out)

```bash
cd /Users/joechua/Desktop/DEV/notes/CS_fundamentals/cpp/basic_cpp/

# 1. attempt without lldb
clang++ -g -std=c++17 debugger.cpp -o build/prog # aha! u'll get an error but read below to learn more
./build/prog # segfault returned

# 2. attempt with lldb
lldb ./build/prog

# (in program with lldb now)
help # see all lldb's commands
run # start running the program

target create prog # re launches the program
b main # add breakpoint at main function => stop execution before executing main()'s body

# from here we can:
    # add another brekapoint ('b'),
    # next command ('n'/ 'next'),
    # step into a command('s'),
    # list 10 (list _line_num_), => shows 10 to 20 lines of src code surrounding your target line
    # bt => (branch tree) see the call stack
```

* -g => debugging symbols
    - compiler will insert additional debugging symbols into program
    - (i.e. name of functions, what line their on etc.)

* -o build/prog => outputs the program as `prog` at `build` directory
    - build directory is relative to your current working directory (not the .cpp file's directory)
    - need to create the directory first! => during my attempt, i didnt create the directory & encountered an error
    ```bash
    joechua@MacBookAir basic_cpp % clang++ -g -std=c++17 debugger.cpp -o build/prog  
    ld: can't open output file for writing: build/prog, errno=2 for architecture arm64  => errno=2 means no such file/ dir exists
    clang: error: linker command failed with exit code 1 (use -v to see invocation)
    ```
    - run this instead: `mkdir -p build && clang++ -g -std=c++17 debugger.cpp -o build/prog` uses the parent flag to create intermediate directories

* lldb ./build/prog - lldb attaches to the program & monitors for specific events




# -------------------------------------------------------------------------------------------------
# const

just some quick notes about `const` keyword => common usages

## const variable & reference

- upon creating a const variable,
    - you can assign it to a non-const variable (copy operation)
    - BUT assignment to a reference variable, requires the reference variable to be const

* semantically, const variables are strictly const (references are jsut aliases, so they have to be const)

i.e.
```cpp
const int x = 1;

int y = x; // fine, copies x's value to y, but not the reference to it

int& z = x; // ERROR, coz z is a reference/alias to x (just another name), it HAS to be const; error msg: error: binding reference of type 'int' to value of type 'const int' drops 'const' qualifier

const int& z = x; // fine
```

## const variable & pointer

- upon creating a const variable,
    - you can assign it to a non-const variable (copy operation)
    - BUT assignment to a pointer variable, requires the pointer variable to be const (w.r.t immutability of value at address space, not the pointer's value itself)
        => can see that expected type is `const int *`
* semantically, const variables are strictly const (pointers dereference to the variable's MEM, so the dereferenced MEM have to be const!)

i.e.
```cpp
const int x = 1;

int* ptr = &x; // ERROR, coz ptr's dereferenced value is not const => can see that expected type is `const int *`
    // actual error message: error: cannot initialize a variable of type 'int *' with an rvalue of type 'const int *'

int* const ptr = &x; // ERROR, coz only ptr's value is const (cant change address it points to) BUT the pointee is still mutable
    // actual error message: error: cannot initialize a variable of type 'int *const' with an rvalue of type 'const int *'

const int* ptr = &x; // fine, coz `const int ...` means that the int value at the address referenced by the pointer has to be constant
                     // u cant dereference and change the value at that MEM region via ptr
```

* pointee = pointer's referenced value

# -------------------------------------------------------------------------------------------------
# Memory regions

text     => code
data     => global variables, static variables
    .data (initialized)
    .bss (uninitialized)
heap     => dynamically allocated (i.e. malloc, new, )
stack    => local variables (i.e. function)

## namespaces & scope, translation units & directives

- namespace - name space is a special container that holds a group of names, & help prevent name collisions when a codebase includes multiple libs with identical identifier names; formally: declarative region that provides a scope for its identifiers (names of types, functions & variables)
    * identifiers declared inside a __namespace block__ belong to that __namespace scope__
- scope - formally: the region of program text where a specific identifier (like variable or function name) is visible & can be used
    * block scopes, function scopes, namespace scopes, class scopes,
    * scope :> namespace: namespace just creates namespace scope, but there are other scopes as well
- translation unit - basic unit of compilation of source code
    => after preprocessor expands all preprocessor directives (i.e. #include, #define, etc.)
- directives - special instruction that tells compiler, assembler or preprocessor how to handle src code before actual compilation
    => preprocessor directives is specific to preprocessor commands
    => 1 translation unit = 1 object file =/= 1 .cpp file (have unit builds where u include multiple cpp files => avoid redundant parsing of headers, global optimization (inlining allows compiler to inline functions without slow Link time optimization[LTO]))

## data segment (uninitialized) vs BSS (initialized)

- both hold static & global variables
- Data (.data) - contains global & static variables explicitly initialized by the programmer with non-0 values
- BSS(.bss) - contains global & static variables uninitialized OR initialized to 0
- execution behvaiour - OS initializes .bss to zero at runtime, while .data values are copied from the executable file

* separated for optimization; .bss segment doesnt need to store 0 values in the executable file on disk, making binary smaller
    - .data variable stores their initial values directly inside the executable file

## why it matters (static)

__namespaces & scope__

- static variables in global namespace are local to its TU (not used across linkage)
- a normal variable would have name collision since they belong to the global namespace & hence global scope
- BUT static variable doesnt have name collision because its local to TU => during linkage no name collision even though same global namespace

## why it matters (function)

__translation units & directives__

Understanding:
- common misuse of `#pragma once` without placing function definition in a separate file
    - if i have #pragma once in the header, and my header includes both declaration & definition
    this means that the function is declared & defined once in the TU,
    - when other headers use it (within the same TU), it wouldnt be re-declared & defined.
        => THIS IS OK, no error yet
    - however if i have other TUs that use the same header file,
    functions will be re-declared & redefined for that TU because, during compilation,
    the preprocessor directives of a TU is specific to that TU's compilation
    
    - hence the function definition's source code will be subbed in again during that TU's compilation
    and, during linkage there will be a name re-definition error

    * i.e. A.cpp -> TU A -> declares & defines `int test() {}` => no compilation error
           B.cpp -> TU B -> declares & defines `int test() {}` => no compilation error
           during linkage => LINKAGE ERROR!!

Good practices:
- header files have either `#pragma once` or `ifndef`
    => ensures function is only declared once within a TU (prevent header from being declared twice in same TU)
    => avoids redefinition error (can technically have multiple declarations)
    => [compile-time]
- typically functions declared in header files have its definition in a separate `.cpp`
    => ensures function is only defined once across all TUs
    => all TUs using that file will get function definition during linkage
    => [linkage-time]

* note that making separate TUs is when creating executables, u include the .cpp file separately in CMakeLists.txt
    * if u include 1 .cpp file (i.e. B.cpp) in to another .cpp file (i.e. A.cpp) then just put A.cpp in the CMakeLists.txt
    then you will only get 1 translation unit for both .cpp files

## why it matters (member variables)

- *static* members are stored in the data segment
- *non-static* members are stored in the same MEM segment as the object instance

non-static - depends on how you created the object:

- Stack
    - local object (i.e. `MyClass obj;`)
    - object & its members are stored on the stack
- Heap
    - allocate an object dynamically (i.e. `MyClass* obj = new MyClass();`)
- Data
    - declare object globally or as __static__
    - object & its members (both static & non-static) are stored in the data segment(initialized) or BSS (uninitialized)

# -------------------------------------------------------------------------------------------------
# static

the static keyword has 3 meanings, based on where their defined:

1. outside a class/ struct & function [global namespace]
2. inside a class/ struct [class/ struct]
    - static member variable & method
3. inside a function

## 1 (global) vs 2 (class): outside vs inside class/ struct

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

## class's static method (static method in class)

* we understand that __static class member variables__ require extra effort to make it *internal linkage* / *dedupe from other TUs*
* also understand that __static functions in global namespace__ require extra effort to make it *internal linkage* / *dedupe from other TUs*

but what about __static methods in class__?

=> general aim of the *static* keyword is to make the symbol be defined once while being able to use/ refer to it from all TUs
    - my undestanding is that the reason you'd have static variable in a function is that so its shared across all function calls in all TUs
    - reason that you'd have static variable in a class is that so its shared across all instances of a class from all TUs
    - static thing declared in global namespace allows any TU that uses the header to use that variable (though no the exact same symbol throughout all TUs, but thats the idea)

so, static method in class means that all instances of that class should be able to use that method
* its a class method! => just like a static member variable (a class variable)
    - its implicitly *inline* if defined in the class => to ensure theres only 1 definition across all TUs enforced during linking
        * actually all methods in a class is *inline* to ensure definitions are deduped

* then whats the point of a static method (its essentially the same as a non-static method)?
    - it can be called without an instantiation
    * the only difference is that there is no hidden *this* pointer passed to the method

```cpp
// normal methodd
double sphere_deg_to_rad(Sphere* const this, double deg) {...}

// static method (class method)
double sphere_deg_to_rad(double deg) {...}
```

## Memory?

* [IMPT!!] static variable for all 3 scenarios is actually stored on the __data segment__!!
    - they are stored on the data segment for the entire duration of the program
    - never popped off the stack & never dynamically allocated during runtime

    * THUS static w.r.t `TU` & `linkage` is about visibility of values,
        vs memory management is about where the memory is stored

# -------------------------------------------------------------------------------------------------
# extern keyword

```cpp
// test.h
int x;  // ERROR => if more than 1 .cpp uses this .h file
extern int x; // fine, anyone that includes this header file will know the existence of x, but not assign MEM yet

// test.cpp
#include "test.h"

// definition of x
// this must happen exactly in 1 .cpp file in the whole project
int x = 0;

// another.cpp
#include "test.h" // includes header for variable

void level_up() {
    x += 100 // modifies the shared global variable
}
```

- both have external linkage
    => variables can be used across TUs (external linkage) & both in the global namespace
    => linker exposes symbol to the entire project
- int x;
    => is a declaration & definition
    => actual MEM allocated
    => can only be included in 1 file => if in 2, duplicate symbol error due to ODR violation
- extern int x;
    => allocates 0 MEM
    => purpose: forward-declaration; promises compiler that this name will exist with external linkage, to enable current file to use the variable
    * functions are implicitly extern
* ODR - one definition rule

# -------------------------------------------------------------------------------------------------
# vscode clangd glitch

sometimes clangd extension does not pick up on latest cpp features & has red scribbly lines for valid code

1. after compilation -> check that ther eis compile_commands.json -> cmd + shift + p -> type: "clangd: Restart language server"

# -------------------------------------------------------------------------------------------------
# multiple executables in 1 project

in CMakeLists.txt:

```md
# create executable
add_executable(project_name_1 src/main.cpp)
add_executable(project_name_2 src/main.cpp)
```

- adding multiple executables in 1 single CMakeLists.txt means: 1 project with multiple programs (executable files)
- this is commonly done when u have main program, then test program that uses same dependencies
- also to create unified environment:
    - same version dependencies (i.e. fmt, Boost) => prevents dependency hell
    - shared Presets & flags => uses same toolchain, cpp standard, compiler flags etc.
    - shared lib linking => compile a lib once(.cpp), use it for linking in multiple executables without recompiling

# -------------------------------------------------------------------------------------------------
# Initializations + Constructions

## Initializations
```cpp
class MarketDataClient {...};
MarketDataClient client;   // already constructs the object => calls the default constructor
// client = MarketDataClient(); // this is not required => infact this creates a temp MarketDataClient obj then moves it into client
// MarketDataClient client = MarketDataClient(); // same thing => copy elision helps to prevent creating the temp MarketDataClient though; effectively same as MarketDataClient client;
```
- default initialization: `MarketDataClient client;` -> obj is created without args => calls the default constructor
- direct initialization: `std::thread t(worker);` -> construct t directly by calling the std::thread constructor with args (worker)
- copy initialization: `std::thread t = std::thread(worker);` -> construct t in a temp then move created thread into t
    equivalently:
    1. std::thread tmp(worker);
    2. std::thread t(std::move(tmp));
    * note that this is still considered copy initialization PURELY coz of the syntax & not because of the inherent steps under the hood
    * but what happens here is actl considered `move construction`!!
- list initialization (Brace Initialization)
    avoids narrowing conversions
    std::vector<int> v{1,2,3};
    int x{3.14}; // ❌ compile error (narrowing)

## Constructions
- Move Construction
    - `std::vector<int> ans = std::move(nums);`
    - so now nums is empty
    
    * internally:
    * (b.ptr = a.ptr, b.size = a.size) __-becomes->__ (a.ptr = nullptr, a.size = 0)
* transfer ownership of internal resources => faster coz its not copying!!

Assignment (not construction)
MarketDataClient client;
client = MarketDataClient();
operator=(MarketDataClient&&)
assignment happens after construction.


## copy initialization e.g.
what does vector<int> ans = nums; do?
```cpp
std::vector<int> ans = nums; // copy initialization syntax BUT => compiler after cpp17 will do vector(const vector&) => copies over the elemnts to the actual storage place rather than a temp
std::vector<int> ans(nums); // direct initialization

// both creates a new vector by COPYING nums!!
// 1. allocate MEM for ans
// 2. copy each element from nums to ans
```

is it because its copy by value, so when i change the element in ans, it doesnt change it in nums
[cling]$ nums
(std::vector<int, allocator<int> > &) { 2, 2, 3 }
[cling]$ v
(std::vector<int> &) { 1, 2, 3 }
[cling]$ 
as can be seen from here?
<!-- can see that OG array is not affected since it is just COPY-ing elements over!! -->

## Consolidation of confusing terms
1. default initialization: `MarketDataClient client;` -> obj is created without args => calls the default constructor
2. direct initialization: `std::thread t(worker);` -> construct t directly by calling the std::thread constructor with args (worker)
3. copy initialization: `std::thread t = std::thread(worker);` -> construct t in a temp then move created thread into t
    equivalently:
    1. std::thread tmp(worker);
    2. std::thread t(std::move(tmp));
    * note that this is still considered copy initialization PURELY coz of the syntax & not because of the inherent steps under the hood
    * but what happens here is actl considered `move construction`!!
4. list initialization (Brace Initialization)
    avoids narrowing conversions
    std::vector<int> v{1,2,3};
    int x{3.14}; // ❌ compile error (narrowing)
5. Move Construction
    - `std::vector<int> ans = std::move(nums);`
    - so now nums is empty
    
    * internally:
    * (b.ptr = a.ptr, b.size = a.size) __-becomes->__ (a.ptr = nullptr, a.size = 0)
* transfer ownership of internal resources => faster coz its not copying!!

6. declare
7. definition

8. initialize
9. assign
10. construct

11. member initialization
    * not to be confused with list initialization -> which is to initialize an object with values and avoid (1) narrow conversion & (2) most vexing parse
```cpp
// example 1: direct initialization [paranthese ()]
class Point {
private:
    int x;
    int y;
public:
    Point(int a, int b) : x(a), y(b) {
        std::cout .... // body code
    }
}

int main() {
    Point p(10, 20);
    return 0;
}

// example 2: list initialization [curly brackets {}]
class Point {
...
    Point(int a, int b) : x{a}, y{b} {
        // body code
    }
}
```

- more preferred modern way

# -------------------------------------------------------------------------------------------------
# container.insert()
what does container.insert() do?
```cpp
ans.insert(ans.end(), nums.begin(), nums.end()); // insert adds elements into a container at a specified position
// iterator insert(iterator pos, InputIt first, InputIt last);
// return value of insert => iterator

// insert into ans
// at position ans.end() => the end of the ans vector
// copy elements from range nums.begin() to nums.end() => if u think about it, its just elements from the nums vector
// key word is COPY
```

# -------------------------------------------------------------------------------------------------
# insert() efficiency (pre-allocate vs allocate on the fly)
This 2 version when compared, why is the 1st one faster?
## version 1
```cpp
vector<int> ans;
ans.reserve(nums.size() * 2); // already allocates enough space
ans.insert(ans.end(), nums.begin(), nums.end());
ans.insert(ans.end(), nums.begin(), nums.end()); // just needs to copy/ move elements into the storage space
```

## version 2
```cpp
vector<int> ans = nums; // allocates enough space for nums first & copy those n elements
ans.insert(ans.end(), nums.begin(), nums.end()); // then continue need to reallocate for this insert method, & shift n elements from the first buffer first
return ans;
```

# -------------------------------------------------------------------------------------------------
# implicit instantiation of undefined template
ISSUE: encountered the red squibbly error in compilation: "implicit instantiation of undefined template"
std namespace is defined across many headers, not just 1
each header adds specific components into std namespace
i.e. <vector> adds std::vector to std namespace
templates live in headerse coz the compiler must see the full implementation when generating types
but if the <vector> template was not included, the std namespace would not know vector exists maybe `template<class T> class vector { ... };` but not the entire definition

* sometimes there are forward declarations in other header files via `#include <something>` hence it throws the error "implicit instantiation of undefined template"

SOLUTION: #include <vector>

# -------------------------------------------------------------------------------------------------
# name shadowing (this keyword)
when we actually need to use `this` keyword

```cpp
class OrderBook {
    int x;
public:
    void setX(int x) {
        this->x = x;
    }
};
```

# -------------------------------------------------------------------------------------------------
# Threads
1. C style `pthreads`
2. Modern Cpp threading `std:: thread`


## example C code
```c
#include <pthread.h>
#include <stdio.h>

// worker function
void* worker(void* arg) {
    printf("hello from thread\n");
    return NULL;
}

int main() {
    // create thread
    pthread_t thread; 
    pthread_create(&thread, NULL, worker, NULL);
    pthread_join(thread, NULL);

    return 0;
}

```

## questions regarding C threads (pthreads)
- is does thread have default initiailization?
    - NO => C has no constructors (doesnt support classes)
    - so there is no default initialization like in cpp
    `pthread_t thread;` jsut allocate space, but leave variable uninitialized
- for c, why thread address passed into create() but not join()?
    - `pthread_create(&thread, ...)` -UTH-> roughly `*thread = kernel_thread_id;`, basically assigns a kernel thread to our thread variable at this address
    - fn signature: `int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void*(start_routine)(void*), void *arg)`
- what is `void*` in return type & parameter type? `void* worker(void* arg)`
    - `void*` exists coz there is no generics/ templates in C
        - i.e. `void*` was useful when assigning returned space from mallo
        `void* malloc(size_t size_in_bytes);` => since malloc is used to create an array of MEM for any type
        `int* arr = malloc(sizeof(int)*10);`
    - for pthread workers `void* worker(void* arg)`
    ```c
    // allows for any type of arg
    worker(int*)
    worker(struct*)
    worker(CustomObject*) ...

    //i.e.
    typedef struct {
        int a;
        int b;
    } Params;

    void* worker(void* arg) {
        Params* p = (Params*) arg // cast the arg to use the params properly; if u dont cast, compilation error as compiler cant recognise that there is a & b member variables
        printf("%d %d\n", p->a, p->b);
    }

    // then
    Params params = {1,2};
    pthread_create(&thread, NULL, worker, &params);
    ```
    - compiler doesnt know the layout of the memory => "layout of the memory" -> struct memebers are accessed by offsets in MEM
    ```c
    typedef struct {
        int a;
        int b;
    } Params;
    ```
    memory layout:
    Params
    +--------+
    | a (4Bytes) |
    +--------+
    | b (4Bytes) |
    +--------+
    a → offset 0
    b → offset 4 == `p->b` == `*(p+4)`
    * thus when compiler doesnt know the type, its not able to compute the offsets & retrieve the correct member variables

## example Cpp code
```cpp
#include <thread>
// #include <iostream> // for std::cout
#include <fmt/core.h>

// free function
void worker() {
    fmt::print("Hello from thread\n");
}
int main() {
    std::thread t(worker); // creates thread with direct initialization
    t.join();
}

// member function
class MarketDataClient {
public:
    void connect() {
        ws_thread_ = std::thread(&MarketDataClient::websocket_listener, this); // initialize the thread
private:
    void websocket_listener();
    std::thread ws_thread_;
```

## questions regarding cpp code
- why do i need to take in __address__ for member fn & __this__?
    
    __free fn__
    - free function => doesnt belong to any object, thread can call it directly
    
    __member fn__
    - thread needs both the __&Class::member_fn__ & __this obj__ to call it on
    - __&Class::member_fn__: why do i pass in __&Class::member_fn__ instead of just __Class::member_fn__
        - `&Class::member_fn` returns a pointer to a member fn => not a normal fn pointer
        - member function pointer type `void (MarketDataClient::*)()` which is what `std::thread(ptr, obj_to_exec_on)` takes in for ptr
        - `void (MarketDataClient::*)()` 1. means pointer to a member fn, 2. belonging to MarketDataClient, 3. that returns void, & 4. takes no params
        - `void (*f)();` <= free fn pointer type
        i.e.
        ```cpp
        void worker() {}
        void (*some_ptr)() = worker;
        some_ptr(); // calls worker
        ```
    - then when thread combines it with __this obj__, it calls `(this->*websocket_listener)()`

    * good to know:
    * member fns have hidden param this: i.e. `void websocket_listener(MarketDataClient* this, ...)` => its like python's self
        - compiler sees `MarketDataClient::websocket_listener(this, ...)` during execution
    * normal functions are not pointers
        -> although, a function name can auto convert(decay) to a fn pointer
        -> type of `worker` is `void ()`, type of pointer pointing to it is `void (*)()`
        -> compiler auto converts worker -> &worker
        - `void (*f)() = worker` == `void (*f)() = &worker`

# Scopes, namespace & MEM mgmt
qns: does scope & namespace mean the same thing in cpp? i.e. if i use the namespace std i am using that scope & can bring invariables from there?
is the memory management also reflective of this?
i.e. if i declare a plain enum, its on the data segment whereas if its for std::, actually they would also be on the data segment just a different scope?

- scope is the region of code where a name is visible
- namespace is a __named scope__ for identifiers (can call types, functions, variables from that scope)
- i.e.
    ```cpp
    namespace math {
        int add(int a, int b) { return a + b; }
    }

    // doesnt change scope, simply tells the compiler when looking up names, also search the `std` namespace!
    using namespace std;
    // allows u to write
    cout << "hello" // instead of std::cout

    // #include <vector>
    ```
- scope & namespace have nth to do with MEM mgmt
    - x & y are both global variables => both go into data segment MEM
    ```cpp
    namespace A { int x = 10; }
    int y = 20;
    ```
- `enum Color { RED, GREEN, BLUE };` does not allocate MEM at all! => compile-time constants

# -------------------------------------------------------------------------------------------------
# nested functions, member initializer list, static, linker 
- nested functions - dont exist in cpp
    - have to use lambda functions

- member initializer list (initialize vs construct)
    - initialization

- `static` keyword (external vs internal linkage)
    - static can exist in global scope .cpp files, class & function
    - if in .cpp file, its local to the translation unit (internal linkage)
    - else class & function are external linkage

- linker
    - requires entry point to link obj files into executable
    - takes compiled object files & piece them tgt, finds symbol `declarations` & match with `definitions`
