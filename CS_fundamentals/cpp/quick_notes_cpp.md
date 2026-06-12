# Quick notes

Below are unorganised notes taken while learning cpp which i have yet to categorise properly into respective folders.

# Initializations (default, direct, copy, list)
# container.insert()
# insert() efficiency (pre-allocate vs allocate on the fly)
# Threads
# implicit instantiation of undefined template
# name shadowing

# -------------------------------------------------------------------------------------------------
# things to keep in mind

- setup
    - cmake - meta build system
    - cmake --presets => runs cmake to read CMakeLists.txt & CMakePresets.json to create the build files for the build system
    - cmake --build build => actually runs the build system (cmake, ninja) to compile & link binaries to produce the executable
    
- private variables
    - are made private when you want to restrict external manipulation, yet you want certain member functions (actions) to access/ modify it
- generally there are 3 ways to avoid duplicate symbol errors
    1. split declaration & definition into .cpp & .h files
    2. merge definitions across all TUs => `inline`
    3. make variable a constant expression => `constexpr`
- static class member variables & functions => class member variables & functions

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# false sharing fix = cache alignment + padding

_false sharing_ - is the issue where 2 threads writing to different variables (i.e. core A & core B each writing to int x & int y)
    that happen to sit on the same cache line. this causes the cache coherence protocol (MESI) to bounce between cores
    => increasing latency of writing data to the cache line

_cache line_ - smallest unit of data that a HW cache can transfer & manage (fixed size block that cores read from / write to)
_MESI protocol_ - HW-level cache coherence protocol used in multi-core processors => it ensures that all processor cores see the same view of data blocks across local caches
    - 4 states: M(Modified), E(exclusive), S(shared), I(invalid)
    => i.e. if cache-line-1 is in state A, core A & core B when wanting to work on cache-line-1, should both see *compatible states*
        *compatible states*
        MESI states are local to each core's cache, not a single global status
        - so core A has a cache line in _moddified state_, then B will have that same line in _invalid state_
        - when B wants to work on it, A will have to write back the changes, change its state to shared, then B's state will be updated to modified and A's state to invalid
        - _shared state_ - data matches main memory but copies of it might exist in other cores' caches
        - _exclusive_ - data is valid, matches main memory exactly & exists only in this single cache
    => if core A modified cache-line-1, then core B wants to make chnages to cache-line-1, then A needs to flush the changes first, then let B work on it (if other cores want to work on the same cache line, they cant do so in parallel)
    => whereas if core A is modifying cache-line-1, and core B is modifying cache-line-2, they dont have to flush the cahnges nor wait for 1 another to finish since they are different blocks of caches 

_cache alignment + padding_ - ensure data chunks never overlap inside the same 64-byte block
    => Core A can keep its line in Modifed state
    => core B can keep its line in the Modified state SIMULTANEOUOSLY
    => avoid flushing BUT requires more RAM (wasted memory)

# -------------------------------------------------------------------------------------------------
# CPU Memory

- the CPU cache consists of only: SRAM(static RAM) L1 L2 & L3 - all on chip
L1 is for specific processing units on the chip
L3 is shared between all processing units on the chip

- On-Chip Storage (Flash/ROM): For microcontrollers (like Arduino) or system-on-a-chip (SoC) hardware, this is non-volatile memory. It permanently stores the device's firmware, operating instructions, and boot code so they aren't lost when the device is powered off.
    => The Flash/ROM chip that holds your computer's BIOS/UEFI firmware is physically located off-chip (on the motherboard), but it is a special case [en.wikipedia.org].
    => hence this Flash/ ROM MEM depends on the hardware you are using

- off chip storage: DRAM (system RAM) - is physically located off CPU chip
much slower than CPU cache but cheap to make
is typically what we refer to as MEM/ RAM

- off chip storage (Permanent): Flash
i.e. SSD or HDD

## boot process

UEFI/ BIOs - located off-chip => stored on dedicated ROM/ Flash chip soldered directly to the computer's mother board
MBR (master boot record) - located off- chip => first 512 bytes of physical hard disk (SSD/ HDD)
VBR  (volume bootrecord) - primary bootloader; located off chip => sits at beginning of specific partition on that same hard disk
OS bootloader(i.e. GRUB/ BOOTMGR) - secondary bootloader; located off chip => stored as a standard file inside the folder structure of your hard disk's file system

1. CPU powers on, looks at motherboard ROM chip & runs the BIOs
2. hard-off. BIOs searches hard disk (SSD/ HDD) & grabs the first 512 bytes (MBR) & copies it into system RAM (DRAM) so the CPU can start processing it
3. find VBR (primary bootloader) - MBR code runs from RAM & reads disk's partition table, finds active partition containing the VBR (primary bootloader) & jumps to load the VBR
4.launching  OS bootloader - VBR code now has enough code to read the disk's filesystem layout. looks into files on the disk & finds heavy-duty OS bootloader (i.e. GRUB or inwdows bootmanager) & loads it
5. launching kernel - OS bootloader now takes over, handles the menus, loads core drivers & launches the OS kernel into system RAM

* note: _active partition_ refers to a physical partition on disk memory, not the virtual partitions concept created later by a running OS

# -------------------------------------------------------------------------------------------------
#  vscode for cpp (CMake: configure / cmake --presets)

you'll realise when opening vscode it will ask you for 3 things:

1. preset config (if `CMakePresets.json` exist)
    - if it doesnt exist vscode depends on kit selection & vscode settings (`.vscode/settings.json`)
    - it then runs the traditional command `cmake -S . -B ./build -G "Ninja" -DCMAKE_BUILD_TYPE=Debug`
2. choice of CMakeLists.txt
    - if this doesnt exist, CMake cant do anything => will not see CMake icon on the left sidebar, will not see "build" or "configure" buttons on the bottome status bar
    - if you try to run `CMake: Configure` via comman palette the command will throw an error
3. choice of kit (apple's clang)

* these occur because we have the cmake extension installed

- this is all part of the `configure step`
- is the equivalent of `cmake --presets`
- there are 3 steps to the `build process`:
    1. configure - reads `CMakeLists.txt`, checks compiler ("kit"), downloads dependencies via FetchContent, generates raw build files
    2. build - runs compiler (GCC, clang, MSVC), compiles .cpp files into machine code, compiles the downloaded dependencies' source code; equivalent of `cmake --build`
    3. link - combines compiled code & donwloaded libs, outputs an executable

# -------------------------------------------------------------------------------------------------
# clang vs clang++

- when running clang++ and clang, they both pass code to the same compilation engine
- clang++ then injects `-lstdc++` (or `-lc++` on macos) telling the system's linker to attach the C++ std lib
- clang doesnt inject this flag & assumes you are writing standard C code -- it uses `libc` std lib

* clang is a multi-language compilation engine & it parses code base on the file's extension (.cpp or .c)

# -------------------------------------------------------------------------------------------------
# type deduction with direct initialization / list initialization

direct initialization `int x(3)` - introduced at the beginning of language (cpp98)
list initialization `int x{3}` - introduced in (cpp11)

in cpp11 & 14:
`auto x = 3;` => deduced as int
`auto x(3);` => deduced as int
`auto x = {3};` => deduced as std::initializer_list<int>
`auto x{3};` => deduced as std::initializer_list<int>, not int

* modern type deduction for `auto var{value};` was finalized in (cpp17) i.e we could finally do `auto x{3};` returns int

* `std::initializer_list` is a lightweight, temp proxy obj that is passed into most cpp containers, & used to populate container types

# -------------------------------------------------------------------------------------------------
# rule of 5

it is a resource management guideline which states - if a class explicitly defined or delete any of the 5 special member functions, it should explicitly define or delete all 5

when manually managing a resource, the compiler's default behvior is often not enough; need to provide custom implementations for:
- destructor: ~Class()                                  => frees up the resource when object goes out of scope
- copy constructor: `Class(const Class& obj)`           => creats a new object by creating a deep copy of an existing resource
- copy assignment constructor: `Class& operator=(const Class& obj)`  => safely _updates_ an existing object by copying another object's resource
- move constructor: `Class(const Class&& obj)`             => creates a new object by stealing the underlying resource of a temporary object
- move assignment constructor: `Class& operator=(const Class&& obj)`  => _cleans up an existing object's_ current resource and steals the resource of a temporary object.

* the main difference between _assignment_ & pure _construction_ is that pure construction just requires creating a new resource without MEM being allocated yet, whereas assignment has MEM already allocated with an old value that needs to be deleted
* _single ampersand(&)_ creates a _standard reference_ that binds to a permanent _lvaule_
* _double ampersand(&&)_ creates an _rvalue reference_ that binds to temporary _rvaule_ => specifically for temporary objects
    * lvalues - objects that have name & persistent MEM
    * rvalues - temporary, nameless values that exist only on the right side of an assignment expression

# -------------------------------------------------------------------------------------------------
# CTAD (class template argument deduction)

before cpp17, compiler required types to be specified inside the container `vector<int> v{26, 0}`
with CTAD, compiler looks at the values passed inside the curly braces `vector v{26, 0}` & auto deduces that they are vector of ints


# -------------------------------------------------------------------------------------------------
# array

creating standard arrays in cpp

```cpp
int arr[5]; // default initialization (garbage values)
int arr[5] = {}; // zero initialization
int arr[5] {1,2,3,4,5}; // list initialization 
```

# -------------------------------------------------------------------------------------------------
# defining multiple variables in the same statement

```cpp
int a;
int b;

// same type (in 1 statement)
int a, b; // correct 
int a, int b; // WRONG

// different types (NOT ALLOWED to do so in 1 statement)
int a, double b; // WRONG
int a; double b; // correct but not reccomended
int a;
double b; // reccomended
```
# -------------------------------------------------------------------------------------------------
# creating tuples

std::make_tuple(var); // uses copies
std::tie(var); // uses references

```cpp
// TUPLE OF COPIES
#include <iostream>
#include <tuple>

int main() {
    int age = 25;
    
    // This COPIES the value 25 into the tuple
    auto my_tuple = std::make_tuple(age); 
    
    // Changing the tuple value
    std::get<0>(my_tuple) = 40; 
    
    std::cout << age << '\n';            // Prints 25 (Original did NOT change!)
    std::cout << std::get<0>(my_tuple);  // Prints 40
}
```

```cpp
// TUPLE OF REFERENCES
#include <iostream>
#include <tuple>

int main() {
    int age = 25;
    
    // std::tie creates a tuple of references pointing to 'age'
    auto my_tuple = std::tie(age); 
    
    // Changing the tuple value via std::get
    std::get<0>(my_tuple) = 40; 
    
    std::cout << age << '\n';            // Prints 40 (Original DID change!)
    std::cout << std::get<0>(my_tuple);  // Prints 40
}
```


# -------------------------------------------------------------------------------------------------
# structured binding

structured binding - unpack objects (ie. tuples, pairs, structures, arrays etc.) into individual named variables in a single line of code

```cpp
std::tuple<std::string, int , double> getEmployee() {
    return {"Alice", 30, 75000.0};
}

// older: std::tie - just creates a tuple
#include <tuple>
#include <string>

std::string name;
int age;
double salary;

std::tie(name, age, salary) = getEmployee(); // this create a tuple that stores references of name, age & salary, hence values are assigned to each variable

// cpp17: structured binding (need auto keyword which was already introduced in cpp11)
#include <tuple>

auto [name, age, salary] = getEmployee(); // unpacked into 3 separate variables
```

# -------------------------------------------------------------------------------------------------
# value-initialization

process whereby it resets a variable to default state (i.e. 0 for int OR empty for strings) when no explicit starting value is provided

occurs when:
- empty paranthese or braces(manual initialization)
- std lib containers
- dynamically allocated arrays
- member initialization/ intializer lists

```cpp
// empty paranthese or braces(manual initialization)
int x{}; // init-ed to 0
double y = double(); // init-ed to 0.0
int* ptr{}; // ptr init-ed to nullptr
int arr[5] = {}; // or int arr[5]{};    all values initialized to 0

// std lib containers
std::vector<int> v(10); // creates 10 ints, all init-ed to 0

// dynamically allocated arrays - new keyword
int* arr = new int[5]{}

// member initialization/ intializer lists
```

## default initialization vs value initialization

```cpp
int x; // default initialized; contains unpredictable garbage MEM
int arr[5]; // default initialized; (still allocates MEM)
int y{}; // value-initialized; guaranteed to be 0
```

# -------------------------------------------------------------------------------------------------
# std::unordered_map

container that stores unique key-value pairs using a hash table implementation

```cpp
std::unordered_map<key_type, value_type> dict;
std::unordered_map<std::string, int> initialized_dict = { {"apple", 10}, {"banana",20} };

initialized_dict["orange"] = 15; // insert new key
initialized_dict["apple"] = 12; // update apple key

// default values?
initialized_dict["un_existent"]++1; // value-initialization
initialized_dict["un_existent"] += 1;

// iterate through keys?
// cpp11: std::pairs
for (const auto& pair : dict) {
    int key = pair.first;
    int val pair.second;
}
// cpp 17: structured binding
for (const auto& [key, value] : dict) {
    // use key & value here
}
```

- deafult value: uses _value-initialization_ - process whereby it resets a variable to default state (i.e. 0 for int OR empty for strings) when no explicit starting value is provided
- iterate through keys & values: structured binding (cpp17 & up)

# -------------------------------------------------------------------------------------------------
# reverse iterators

to iterate an array in reverse, use reverse iterators (`rbegin()`, `rend()`)

```cpp
std::vector<int> vec = {1,2,3,4,5};
for (auto it = vec.rbegin(); it != vec.rend(); ++it) {
    int x = *it // returns elements
}
```

- `rbegin()` - starts from the last element, not the capacity

# -------------------------------------------------------------------------------------------------
# range-based for loop

```cpp
// cpp11 & up
std::vector<int> vec = {1,2,3,4,5};
for (auto x : vec) {
    // use x here
}

// index i included

// cpp11 & up
int i = 0
for (auto x : vec) {
    // use x here
    i++;
}

// cpp20 & up: init statement
for (int i = 0; auto x : vec) {
    // use x here
    i++; // still need to increment i
}

```

# -------------------------------------------------------------------------------------------------
# pre-increment vs post-increment

pre-increment(++i) - increments the variable then returns new value; increment *pre* returning value
post-increment (i++) - returns current value then increment; increment *post* returning value

```cpp
int i = 5;
int a = ++i // a is 6, i is 6

i = 5;
int b = i++ // b is 5, i is 6
```

## in for loops

pre-increment(++i) is preferred

```cpp
for (int i = 0; i < 10; ++i) // preferred
for (int i = 0; i < 10; i++) // incurs overhead
```

i++ - requires returning the OG value of i before being incremented; compiler creates a temp copy of i, increments the OG i, then returns temp
++i - no temp created, just increment i & return

* in general, use pre-increment(++i)

# -------------------------------------------------------------------------------------------------
# std::endl vs \n

std::endl - adds newline character & flushes output buffer (for immediate ouptut visibility); slower
\n - adds newline character

```cpp
std::cout << "test1"; // no new line character
std::cout << "test2" << std::endl;
std::cout << "test3\n";
```

# -------------------------------------------------------------------------------------------------
# arrow operator(->)

`->` - is used to access members of a class, struct or union through a pointer

# -------------------------------------------------------------------------------------------------
# dereference a pointer

```cpp
int number = 42;
int* ptr = &number;

int current_value = *ptr; // dereferenced pointer, returns value

*ptr = 100; // dereference pointer to change value
```

# -------------------------------------------------------------------------------------------------
# namespace pollution & include std library

## include std library
this is considered bad practice and is just a deonstration of how to include everything from the cpp standard lib

```cpp
#include <bits/stdc++.h>

int main() {
    std::vector<int> v;
    std::string s;
    std::cout << "everything is included...\n"
}

// cpp20 & newer (modules)
import std;
int main() {...}
```

## namespace pollution

this is also considered bad practice as it causes *namespacee pollution*
it dumps all the standard names into current scope (global scope)

```cpp
#include <iostream>
#include <vector>

using namespace std;

int main() {
    vector<int> v; // No std:: needed
    cout << "Hello World!"; // No std:: needed
}

// ---------------------------------------------
// or if you only want to include specific tools
#include <iostream>

using std::cout; // Only make cout a shortcut
using std::endl; // Only make endl a shortcut

int main() {
    cout << "This is safe!" << endl;
    // std::vector would still require the prefix here, keeping the rest clean.
}
```

# -------------------------------------------------------------------------------------------------
# download & include a cpp library in your project

1. install boost-asio via vcpkg (optional: done for classic mode)

```bash
vcpkg install boost-asio
```

- this is only required in classic mode
- in manifest mode
    - cmake configure command (cmake --preset) calls the vcpkg toolchain script
    - it auto reads vcpkg.json file
    - detects boost asio is missing from the project directory
    - then downloads, compile & setup automatically

2. add it to `vcpkg.json`

```json
// enforce minimum version
{
  "name": "market-infra",
  "version": "0.1.0",
  "builtin-baseline": "3426db05b996481ca31e95fff3734cf23e0f51bc",
  "dependencies": [
    "fmt",
    {
      "name": "boost-asio",
      "features": [ "ssl" ],  // include ssl feature flag to enable ssl connections
      "version>=": "1.82.0"
    }
  ]
}

// lock exact version
{
  "name": "market-infra",
  "version": "0.1.0",
  "builtin-baseline": "3426db05b996481ca31e95fff3734cf23e0f51bc",
  "dependencies": [
    "boost-asio"
  ],
  "overrides": [
    {
      "name": "boost-asio",
      "version": "1.81.0"
    }
  ]
}
```

- `CMakePresets.json` was what instructed cmake to use vcpkg (as the toolchain);
    `CMAKE_TOOLCHAIN_FILE` forces cmake to load `vcpkg.cmake` script before it processes `CMakeLists.txt`
    `vcpkg.cmake` then looks for `vcpkg.json` to determine if project is in *manifest mode*; if absent, it falls back to *classic mode*
    `vcpkg.cmake` redirects find_package() to look inside your project's manifest folder `vcpkg_installed` instead of global mac directories
    `vcpkg_installed` contains project specific dependencies
- i.e. git commit `3426db05b996481ca31e95fff3734cf23e0f51bc` baseline uses Boost version `1.80.0`
    vcpkg then auto downloads, compiles & installs boost 1.82.0 directly into your project's `vcpkg_installed` folder

* toolchain lets cmake know to use vcpkg
* vcpkg.json tells vcpkg to run in manifest mode

3. once vcpkg finishes downloading boost, add it to your project via `CMakeLists.txt`

```bash
find_package(Boost REQUIRED COMPONENTS system)
find_package(boost-asio CONFIG REQUIRED)

target_link_libraries(project_name PRIVATE boost_asio::boost_asio)
```

4. re-run CMake:configure


# -------------------------------------------------------------------------------------------------
# std::string

```cpp
#include <string>
std::string hello = "hello";
```

- literal text "hello" is created directly inside the executable's file's binary, data segment (.rodata segment) => persists throughout the entire program
- creates a control block (contains pointer, size & capacity) on the stack
- std::string constructor runs & reads "hello" out of the read-only binary section & copies it into the stack variable
    => this is coz hello is only 5 characters long (small) hence SSO(small string optimization) is done
    [STACK MEMORY]
    hello Object Control Block:
    ┌───────────────────────────────────────────────────────────────┐
    │ internal_buffer: [ 'h' ][ 'e' ][ 'l' ][ 'l' ][ 'o' ][ '\0' ]   │ 
    │ size: 5                                                       │
    └───────────────────────────────────────────────────────────────┘
- if large 100-character sentence, constructor requests MEM from the heap, then copies the text from .rodata to the new heap address, pointer inside the stack is then set to target that heap MEM

# -------------------------------------------------------------------------------------------------
# construction, initialization, assignment, declaration, definition

SomeClass obj; // object construction => default constructor called
SomeClass obj(); // most vexing parse error
SomeClass obj{}; //object construction, constructor without args called
int x; // uninitialized variable, variable contains garbage value

the SomeClass object is constructed
the obj variable is then initialized with the object constructed by the default constructor (not assignment)
int x was *declared* AND *DEFINED*. it was never initialized. => MEM was allocated to x, just value was not initialized

- `construction` is when class constructor is called
- `initialization` is giving a variable a value at the moment it was created
- `assignment`  is giving a variable a value after the variable already exists
- `declaration` tells the compiler a name exists & what type it is, but doesnt allocate MEM or provide a value
- `definition` creates the thing, allocates MEM & provides full implementation ("creates the thing" means allocating MEM for it)

* assignment =/= initialization     => either or, they are mutually exclusive
    - assignment occurs after the variable already exists
    - initialization occurs at the point of definition
    ```cpp
    int x;    // definition
    x = 5;    // assignment — happens after, not part of definition
    int y = 5 // definition + initialization (not assignment)
    ```

# -------------------------------------------------------------------------------------------------
# assignment with references

```cpp
double x = v[0] // where v[0] retuns double&
    // since double& is assigned to a variable that is of plain double type
    // value is just copied over to x

int a = 5;
int& ref = a; // ref contians a reference of a
int b = ref; // same thing occurs where value is copied over

```

# -------------------------------------------------------------------------------------------------
# const object & const member functions

golden rule: __const object can only call const member functions__

```cpp
class vec3 {
public:
    ...
    double operator[](int i) const { return e[i]; } // (1) remove this
    double& operator[](int i) { return e[i]; } // (2) remove this
    ...
}

const vec3 v(1,2,3);
v[0]; // (1) COMPILE ERROR!

vec3 v_another(1,2,3);
v_another[0]; // (2)
```

- (1) const object
    => const objects can *only* call *const member functions*!!
    => without the const member function, the object has no function to call for the `[]` operator
- (2) non-const object
    => are allowed to call both *non-const member functions* & *const member functions*
    => preference is to call *non-const member functions*
    => without the non-const member function, it will call the const member function & return a copy of e[i]

* importantly: a *constant* object (i.e. `const vec3 v(1,2,3);`) has *constant internal state*/ is *not immutable*, hence values inside it cant be changed
    => is only allowed to call const member functions
    => non-const member functions have potential of changing internal state

# -------------------------------------------------------------------------------------------------
# generating random double

```cpp
// version 1: C style, not good
#include <cstdlib> // legacy function inherited from C
inline double random_double() {
    // random real double in [0, 1)
    return std::rand() / (RAND_MAX + 1.0); // ensure that its less than 1 => force floting point number
}
// random real double in [min, max)
inline double random_double(double min, double max) {
    return min + (max - min) * random_double();
}

// version 2: canonnical cpp way
#include <random>
inline double random_double() {
    static std::uniform_real_distribution<double> distribution(0.0, 1.0);
    static std::mt19937 generator; // larger range of random values to choose from
    return distribution(generator);
}
```
# -------------------------------------------------------------------------------------------------
# name vs symbol

- name - variable written in source code => exists only for the dev & compiler
- symbol - entry in the compiled object file that the linker needs to resolve across translation units (TU)

# -------------------------------------------------------------------------------------------------
# constexpr

tells the compiler that the value is *known* & *fixed* at compile time

## constexpr mechanism

- its not plain text substitution like `#define` by the preprocessor
- compiler evaluates the expression at compile time & folds result directly into the instructions => constant folding
- instead of having the value in MEM, it gets directly compiled as a value inside the instructions

* re-cap: constant folding occurs for arithmetic operation between constant variables as well

## why not just use #define?

cons of using #define:
- handled by preprocessor -- no type info
- cant be scoped => cant contain it in a namespace or class
- hard to debug => debuggers often cant see #define names, just the raw substituted values

pros of constexpr:
- has name but "no symbol" benefit
- type safety
- scoping
- debuggability

* constexpr variables can have a symbol BUT only when an action forces it to have one (i.e. accessing address of var `&MAX`)

# -------------------------------------------------------------------------------------------------
# cmake vs make vs ninja

* `CMake` - meta build system (generator) => instead of compiling the code itself, it reads a config file (`CMakeLists.txt`) & generates the build files for other build systems like Make/ ninja
    * definition: a cross-platform, open-source meta-build system (or build generator)
* `Make/ ninja` - build system (executor) => directly executes commands to compile & link code (follows instructions in a file called MakeFile/ build.ninja)
    * runs the compiler & linker to actually create the final executable files
    * ninja was designed to be faster than older tools (`make`)

* `toolchain file` - config script used by (meta) build systems (typically `CMake`) to define specifc env & tools like compiler, path to headers & libs etc.
* `manifest file` - metadata doc (typically JSON, XML, YAML; i.e. `vcpkg.json`) that outlines structure, contents & config settings of a software app

# -------------------------------------------------------------------------------------------------
# cpp project structure

## Canonical way of structuring a project?

dont nest a project folder inside another project folder.

i.e.
WRONG structure:
project_name/
    ├project_name/
        ├── CMakeLists.txt          # build target: src/main.cpp → RayTracer executable
        ├── CMakePresets.json
        ├── vcpkg.json              # package manager config
        ├── vcpkg-configuration.json
        ├── image.ppm               # last rendered output
        ├── src/                    # active source (chapters 1–13)
        ├── assets/
        ├── drafts/
        ├── build/

CORRECT structure:
project_name/
    ├── CMakeLists.txt          # build target: src/main.cpp → RayTracer executable
    ├── CMakePresets.json
    ├── vcpkg.json              # package manager config
    ├── vcpkg-configuration.json
    ├── image.ppm               # last rendered output
    ├── src/                    # active source (chapters 1–13)
    ├── assets/
    ├── drafts/
    ├── build/

## what to commit?

INCLUDE:
- `src/` + `include/`                           => src code & header files
- `CmakeLists.txt` + `CMakePresets.json`        => build system configs; helps config cmake according to project requirements
- `vcpkg.json` + `vcpkg-configurations.json`    => package manager files; tells build system which external libs to include
- `.clang-format` + `.clangd`                   => style format to follow + config for clangd(language server); helps other devs to follow the current style im using

EXCLUDE:
- `build/`
- `assets/`
- `.cache/`

# -------------------------------------------------------------------------------------------------
# scopes

* while working on my ray tracer, i encountered a slight bug. can you spot it here:

```cpp
double root = (h - sqrt_discriminant) / a; // potential ERROR: if ray direction was 0, a will be 0; bad divide by 0 occurs here
if (!ray_t.surrounds(root)) {
    double root = (h + sqrt_discriminant) / a;
    if (!ray_t.surrounds(root)) {
        // doesnt exist
        return false;
    }
}
```

- noted that root was re-declared and this is actually allowed
- new root was declared in another scope and hence once it came out of that inner scope, the remaining code was referencing the wrong root
    => the inner scope can use variables from the outside scope
    => the inner scope can overwrite names (shadow) from the outside scope
- once scope finishes, the inner names do not persist => destructors are called

# -------------------------------------------------------------------------------------------------
# move semantics vs copy elision

- *copy ellision* - compiler technique that eliminates unnecessary copying of objects [feature]
    => URVO
    => NRVO
- *move semantics* - optimization that allows us to transfer ownership of data memberes from 1 object to another [optimization]

## HISTORY

- cpp11 & onwards, *move semantics* used during compilation [move_semantics]
    => if the compiler cant use RVO, it will auto attempt to move the resource instead of copying
- b4 cpp17, *RVO (copy elision)* was just an optimization [URVO/NRVO]
    => if ur class had no copy constructor, compilation fails even if compiler was smart enough to elide the copy (coz the compiler recognises that u cant return by value)
- cpp17 & onwards, *URVO* became a language feature [URVO]
    => temporary values will never request copy constructor to be called
    => now u can return non-copyable, non-movable types by value safely

## COPY ELISION & URVO / NRVO

copy elision - compiler technique of omitting copy & move constructors
URVO / NRVO - specific mechanisms used to achieve copy elision when returning values from functions

### types of copy elision (URVO & NRVO)

1. unnamed RVO(URVO) / mandatory elision (cpp 17) - guarantees that returning a temporary nameless value (PRvalue) never copies, making Unnamed RVO(URVO) a language feature rather than an optimization
    * PRvalue (pure Rvalue) - a transient, temporary value returned not stored in MEM; cant take address of prvalue using &

2. RVO / NRVO - returning an object that has a variable name (Lvalue)
    * Lvalue (locator value) - persistent object with a designated location in MEM (stack or heap)

```cpp
// 1. unnamed RVO (mandatory)
VectorBackup createVector() {
    return VectorBackup(100); // Unnamed temporary (prvalue)
}

// 2. named RVO (optional)
VectorBackup createNamedVector() {
    VectorBackup local_vec(100); // Named variable (lvalue)
    local_vec.data[0] = 5;       // You do work on it
    return local_vec;            // NRVO kicks in here
}

int main() {
    // Zero copies, zero moves. 
    // The vector is constructed directly inside 'v'.
    VectorBackup v = createVector(); 

    VectorBackup v = createNamedVector(); 
}
```

### URVO mechanism (unnamed)

URVO is used when PRvalue is returned from the function. it passes a hidden pointer from the caller to the callee

- caller allocates uninitialized MEM on its stack frame
- caller passes address of this MEM (as a hidden ptr argument)
- callee constructs the return object directly inside that MEM
- no copy operation

### NRVO mechanism (named)

NRVO is used when Lvalue is returned from the function. it rewrites the function by passing a hiddenpointer representing the MEM address provided by the caller

```cpp
std::vector<int> get_numbers() {
    std::vector<int> result = {1, 2, 3}; // The named local variable
    result.push_back(4);
    return result; 
}
std::vector<int> main_vec = get_numbers();
```

- compiler rewrites funciton signature & passes a hidden pointer to the destination memory[main_vec] variable into the function
- instead of allocating space for result on its own stack, get numbers uses hidden pointer
- local variable result is alias-constructed directly inside main_vec's MEM slot
- any ops called on the vector happens directly inside that caller-owned MEM slot
- when function returns, function exits
- no copy

### patterns that break NRVO

#### NRVO failure scenario 1: multiple paths

* NRVO fails when it cant mathmatically prove which variable will be returned at compile-time
    => it fails not because of amount of space allocated (compiler definitely knows how much space base on the return type)
    => it fails because it doesnt know which local variable's MEM to substitute with the destination MEM

```cpp
std::vector<int> get_conditional_vector(bool condition) {
    std::vector<int> v1 = {1, 2};
    std::vector<int> v2 = {3, 4};

    if (condition) {
        return v1; // NRVO fails here
    } else {
        return v2; // NRVO fails here
    }
}
```

#### NRVO failure scenario 2: parameters

* NRVO fails when return value is the parameter

```cpp
VectorBackup processParam(VectorBackup param) {
    // Modifications to param happen here...
    return param; // RVO impossible! Triggers MOVE constructor.
}
```

why? cant we just substitute the param's MEM with the destination's MEM?
    -> according to cpp standard, function parameters are explicitly excluded from NRVO eligibility
- *MEM Layout issue*: before __process_param__ even executes, *caller* already determines where __param__ will live in based on the platform's ABO (Application binary interface)
- *Coflict*: slot A (RETURN SPACE of hidden pointer) vs slot B (PARAMETER SPACE, separate MEM block where data is copied / moved into it => becomes param variable inside fn)
    - paramter space is allocated when function is invoked
    - hidden pointer mem is created when function is invoked
    - the compiler then cant retroactively merge these 2 memories

    * note that parameters are typically located in the caller's stack frame (or in CPU regs), NOT the callee's stack frame

* [visualization]

[ Caller's Stack Frame ]
 ├ *Slot A: Secret Return Space (Empty)*  <───┐
 ├── Function Argument 2                      │
 └ *Slot B: 'param' Storage (Data Here)*      │
                                              │ Pass Hidden Pointer
[ Callee Function: processParam ]             │
 ├── Uses Slot B for modifications            │
 ├── Return Address (Where to go back to)     │
 ├── Saved Frame Pointer                      │
 └ *At return statement, writes data to* ─────┘

#### NRVO failure scenario 3: std::move Pessimization

```cpp
VectorBackup brokenByMove() {
    VectorBackup obj(500);
    
    // You think you are optimizing, but you just destroyed NRVO.
    return std::move(obj); // Forced MOVE constructor instead of ZERO-COPY elision.
}
```

## MOVE SEMANTICS

move semantics is a runtime optimization that falls back when copy elision is impossible;
    => allows an __object__ to *steal resources from* a __temp object__ instead of making a deep copy

### Move Semantics mechanism

```cpp
#include <iostream>
#include <utility>

class ResourceManager {
public:
    int* data;

    // Constructor allocates memory
    ResourceManager() { 
        data = new int[100]; // memory on the heap
    }

    // Destructor frees memory
    ~ResourceManager() { 
        delete[] data; 
    }

    // 1. MOVE CONSTRUCTOR
    ResourceManager(ResourceManager&& other) noexcept {
        data = other.data;       // Steal the pointer (extremely fast)
        other.data = nullptr;    // Clear the old object so it doesn't delete the memory
    }
};

int main() {
    ResourceManager a; 
    // std::move turns 'a' into an rvalue, allowing 'b' to steal its memory
    ResourceManager b = std::move(a); // actually a construction, not assignment
}
```

- Rvalue references(&&) type modifier that tells the compiler - this variable points to a temp object that is about to die
- move constructor is executed & finished first (to transfer data to b)
    - other.data is set to nullptr, so that the memory at data will not be deleted
    - deleting a nullptr in cpp does absolutely nothing
- destructor for a & b are called once the main function is done executing
    - a deletes nullptr => which does nothing
    - b's destructor deletes the memory storage for data => memory on the heap is removed

* `ResourceManager b = std::move(a);`
    - is actually a construction, not assignment, for b => new object b is being created using a
    - thus, b' constructor (move constructor) is actually being called, by taking in a as an rvalue

### why do we need rvalue refernce (&&)

Q. why do we need rvalue reference when i can just use a normal reference to take in a variable for `move semantics`?
ANS.
    because (1) we want to accept only temporary objects (2) prevent thief constructors

(1) temporary objects

    ```cpp
    // Function declaration 1: const used
    VectorHolder(const VectorHolder& other) {
        data = other.data;
        other.data = nullptr; // (A), COMPILER ERROR: 'other' is const! You cannot modify it.
    }

    // Function declaration 1: const NOT used
    VectorHolder(VectorHolder& other) {
        data = other.data;
        other.data = nullptr;
    }

    // Inside main:
    VectorHolder vec(VectorHolder{}); // (B), COMPILER ERROR! Temporary objects cannot bind to 'VectorHolder&'
    ```

- to accept a temp object, `const` reference is required as mutation of a temp object is not allowed in cpp (A)
- a non-const standard reference (other) refuses to bind to a temporary object => compilation will fail

(2) thief constructors

    ```cpp
    class VectorHolder() {};

    VectorHolder x; 
    VectorHolder y = x; // You think you are copying x into y, but the compiler is actually constructing y using x
                        // x.data is now nullptr! x was secretly destroyed.
    VectorHolder x; 
    VectorHolder y; // default constructor called
    y = x; // copy assignment operator (the bad copy) occurs => same bad op occurs here!
    ```

- if you bypass the temp issue by using non-const reference & a variable, the copy constructor is overriden with a bad one
    => basically replaced the copy constructor with a destructive constructor

### return value from function?

* how is move semantics used when returning a value from a function then?
    (using example from `#### NRVO failure scenario 1: multiple paths`)

```cpp
// using 
VectorBackup runtimeChoice(bool condition) {
    VectorBackup optionA(100);
    VectorBackup optionB(200);
    if (condition) {
        return optionA; // Automatic Move! Compiler treats optionA as an rvalue.
    } else {
        return optionB; // Automatic Move! Compiler treats optionB as an rvalue.
    }
}

VectorBackup externalObj = runtimeChoice(true); // moved to the externalObj variable
```

- no special keyword is required actually
- in the example, when the compiler fails to do NRVO, compiler auto calls your *move constructor* to shift the data out of the function
    - u dont need to type `std::move`
- the *return variable* is treated as an *rvalue*
    (`b = std::move(a)`)
    - externalObj's move constructor is called
    - compiler passes inside variable (optionA) as an rvalue referece(&&) into the outisde variable (externalObj)
    - externalObj steals the heap memory pointer
    - optionA.data is set to nullptr
    
    * note that even if a is moved, it can still be re-used & doesnt get destroyed until you manually do so OR it goes out of scope

    (when the function ends)
    - optionA's destructor is called
    - FUNCTION SCOPE then finishes, stack frame is popped
    
    * destruction vs popping from stack frame
        - destructors of each variable on the stack is called first, in the reverse order of their creation
        - stack pointer is then moved => effectievly popping the frame
        - once stack frame is popped, the MEM area is invalidated & can be overwritten immediately by next fn call


## OVERALL

### hierarchy of efficiency (copy elision :> move :> copy)

BEST: copy elision      => compiler modifies the MEM layout so no data transfers at all
MID: move semantics     => if elision is blocked, compiler swaps pointers cheaply
WORST: copy semantics   => if move constructors are missing or disabled, compiler duplicates data

language feature means that there is guarantees rather than just faster more efficient optimizations?
whats the difference between an optimization vs a feature?

### modern compiler decision tree

                Is it a temporary (prvalue)?
                           /       \
                    [Yes] /         \ [No: Named Object]
                         v           v
    [1. URVO] MANDATORY COPY ELISION      Can the compiler match the local 
          (Zero copies/moves.        name to the hidden pointer?
          Language feature.)              /            \
                                   [Yes] /              \ [No: Broken RVO] => [3. move semantics]
                                        v                v
                            [2. NRVO] OPTIONAL NRVO    Implicit Move Attempt
                                 (Zero copies/moves. (Falls back to Move Constructor)
                                  Compiler Opt.)         |
                                                         v
                                                    Copy Constructor    => [4. copy constructor]
                                                    (Worst case fallback)

by priority:
1. URVO => prvalue
2. NRVO => lvalue
3. move semnatics => not possible to elide copy (copy & move pointer address) => rvalue
4. copy constructor => not possible to elide copy (copy value)

### returning value from callee function flow

- small data => *register passing* 
    => for small data types like ints, floats or pointers, CPU doesnt use MEM to pass value
    => value of local variable is copied into a register (rax on x86-64 systems)
    => when function exits, variable is destroyed
    => caller function then reads the value out of that register

- large data => *return value optimization (RVO)* => a type of __copy elision__
    (refer to URVO & NRVO mechanisms)

- no RVO => *move semantics* [IMPT!!] => refer to the 3 *patterns that break NRVO*

## TERMINOLOGIES / GLOSSARY

* callee - function that gets called by the caller
* caller - function calling the callee
* PRvalue (pure Rvalue) - a transient, temporary value returned not stored in MEM; cant take address of prvalue using &
* Lvalue (locator value) - persistent object with a designated location in MEM (stack or heap) [permanent]
* rvalue (xvalue; expiriing value) - object that used to be an lvalue, but is actively expiring because it was explicitly cast to be moved
    - could also stand for "right value" which means a value that could only appear on the right-hand side of an assignment operator (=) [temporary]
* language feature - is a behavior that must be obeyed by the compiler; cant be turned off as it is part of how the language parses code
* optimization - the compiler tries to optimize but is not always guaranteed; can also be turned off via compiler flags

# -------------------------------------------------------------------------------------------------
# initializer list: member initializer list vs std::initializer_list

member initializer list vs std::initializer_list

```cpp
// member initializer list - initializes class members during construction
class Player {
private:
    std::string name;
    const int id;
    int& teamRef;
public:
    Player(std::string pName, int pId, int& pTeam) 
        : name(pName), id(pId), teamRef(pTeam) {
        // Constructor body runs AFTER members are initialized
    }
}

// std::initializer_list - initializes vectors with values 1 to 5
vector<int> vector1 = {1, 2, 3, 4, 5};
```

# -------------------------------------------------------------------------------------------------
# member initializer list vs curly brace initialization

* this is just a mental note as i always forget whats the terminology names for these even though
    i know what im trying to refer to

```cpp
// member initializer list
metal(const color& albedo, double fuzz) : albedo(albedo), fuzz(fuzz < 1 ? fuzz : 1)

// curly brace initialization
point3 new_point{0, 0, 0};
```

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
# smart pointer (shared_ptr & make_shared)
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
    - BUT compiler sees that its const & treats that memory as completely private, specific to that TU (other TUs cant refer to this static variable)
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
    - (1) you can assign it to a non-const variable (copy operation)
    - (2) BUT assignment to a reference variable, requires the reference variable to be const
        * CANT bind a non-const reference to a const variable
    - (3) can bind a const reference to a const variable
    - (3) can bind a const reference to a non-const variable
* semantically, const variables are strictly const (references are just aliases, so they have to be const)

i.e.
```cpp
const int x = 1;
int y = x; // (1) fine, copies x's value to y, but not the reference to it
int& z = x; // (2) ERROR, coz z is a reference/alias to x (just another name), it HAS to be const; error msg: error: binding reference of type 'int' to value of type 'const int' drops 'const' qualifier
const int& z = x; // (3) fine
const int& a = y; // (4) fine, even thought y is non-const
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
# inline & static(global) & extern

_extern_ - tells the compiler that a variable exists somewhere else & dont worry about it (forward declaration)
_static (global)_ - makes variable declared as static in global scope hidden from the linker (other.cpp cant use extern to access it)
_inline_ - a directive to the linker telling the compiler that a function or variable can be defined in multiple TUs without causing a "multiple definition" linker error
    => doesnt replace code with constants

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
