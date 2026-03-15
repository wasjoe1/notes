# notes
Random unorganised notes taken while learning cpp

# Initializations (default, direct, copy, list)
# container.insert()
# insert() efficiency (pre-allocate vs allocate on the fly)

# quick setup for new cpp proj
# cpp dev setup
# Re-build
# styling cpp code
# implicit instantiation of undefined template
# name shadowing

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
# quick setup for new cpp proj
aim is to not waste time setting up & figuring out how i should organise my cpp projects

below is the exact steps i do to init a new cpp proj: (using CMake, vcpkg, ninja, c++20)

1. project folder structure
    root
    │
    ├── CMakeLists.txt
    ├── CMakePresets.json
    ├── vcpkg.json
    ├── vcpkg-configuration.json
    │
    ├── src
    │   └── main.cpp
    │
    └── build                       -> dont touch this
2. update dependencies in files:
    - CMakeLists.txt
    - vcpkg.json
    - main.cpp

3. build project via
    - (optional) `rm -rf build` -> if build isnt working for weird cases
    - `cmake --preset vcpkg` -> run this if u change depencies + add/ remove files
    - `cmake --build build` -> run this if u only change code logic

4. installing new dependencies
    - if using manifest mode, u dont have to manually install via `vcpkg install _dependency_name_`
    - to know if ur in manifest mode, check if u have `vcpkg.json` => just include dependencies there

# -------------------------------------------------------------------------------------------------
# cpp dev setup
resource to setup CMakeLists, Ninja, : https://learn.microsoft.com/en-us/vcpkg/get_started/get-started?pivots=shell-bash

## virtual env??
=> no virtual env like in python
=> CMake manages compilaation process (build process)
=> keep dependencies & build outputs in `/build` using `Cmake` + `vcpkg or conan` package manager
=> Cmake project files are normally named `CmakeLists.txt` => should contain `project()` call
=> `CmakeLists.txt` & `CmakeList.txt` not the same

* thing is cpp doesnt use virtual env like python. it relies on build systems to create the entire env each time u build the project
* mainly coz virtual envs are used to isolate runtime envs => but cpp compiles each time there is a difference in dependencies
    => CMakesLists already tells it where to look

## Main Components
- CmakeLists -> config file (for Cmake)
- cmake -> meta-build system generators => generates build files
- Ninja -> build system => runs the build files
- vcpkg -> package manager => installs & manages cpp dependencies
- gcc/ clang/ LLVM -> compilers
- clangd -> language server => understands cpp code (AND flags, build cmds etc.) then provides advance features i.e. recognising headers

## fmt red scribbly => issue where clangd doesnt recognise cpp code (BECOZ of build)
1. fmt not actl installed OR not linked to proj
2. IDE's intellisense cant find the header coz include paths/ compiler config are incomplete

* install fmt through pckg manager + let CMake link it
1. install vcpkg => package manager for cpp
~~2. install fmt using package manager~~
2. add dependencies & project files

### 1. install vcpkg
1. `git clone https://github.com/microsoft/vcpkg.git` clone the gh repo
2. `cd vcpkg && ./bootstrap-vcpkg.sh` cd into the new repo & run the shell script
    * bootstrap script does pre-req checks & downloads the vcpg executables
3. run these commands
    `export VCPKG_ROOT=/path/to/vcpkg` => stores a string in the env variable
    `export PATH=$VCPKG_ROOT:$PATH` => prepends the vcpkg folder to the PATH list

    * PATH tells your shell where to look for executables
    => try `echo $PATH`
    => see a list of file paths than contains executables
    => i.e. when u type python & hit enter, OS looks at the 1st dir in the list, & checks if there is a file named python inside the folder; else it moves to the 2nd dir so on & so forth
    * to check `echo $VCPKG_ROOT`
    * export-ed variables are shell variables that have been "exported" => included in the env so when other processes or commands are executed, it can be used
~~4. when running `vcpkg install fmt` => it will look through the executables in `PATH` env variable & eventaully find the vcpkg~~

### 2. add dependencies & project files
1. create manifest file by running `vcpkg new --application` (manifest file is a metadata document) => creates `vcpkg.json`
2. add fmt dependency `vcpkg add port fmt`
* `vcpkg.json` is ur manifest file => vcpkg reads this file & install dependencies from here reqruied by proj
* `vcpkg-configurations.json` is baseline constraints => min. vers of dependencies that proj should use
4. create `CmakesLists.txt`
```bash
cmake_minimum_required(VERSION 3.10) # min. version of CMake to build this project

project(HelloWorld) # sets name of proj

find_package(fmt CONFIG REQUIRED) # looks for fmt using CMake config file => REQUIRED ensures we MUST find the pacakage

add_executable(HelloWorld helloworld.cpp) # creates executable taget with name HelloWorld from src file helloworld.cpp

target_link_libraries(HelloWorld PRIVATE fmt::fmt) # specifies HelloWorld executable should link against fmt lib
# private means that fmt is only needed for building HelloWorld & should not propagate to other dependent projs
```

* 
- CMake => build system generator => reads CMakeLists.txt and generate build files for the system
    - `cmake -B build -S .`
    => read CmakeLists.txt in curr folder => then create build files inside `/build`
- CmakeLists.txt
    - config file describing the proj => tells Cmake what to do (files to compile, libs to link, deps to include etc.)
- vcpkg
    - package manager
    => download libs, build them, store them locally, expose them to CMake etc.

### Proper CMakeLists.txt

XX WRONG EXAMPLE!!! XX
```bash
cmake_minimum_required(VERSION 3.20)
project(orderbook)
set(CMAKE_CXX_STANDARD 20)
include(FetchContent)
FetchContent_Declare(
    fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG 10.2.1
)
FetchContent_MakeAvailable(fmt)
add_executable(orderbook src/orderbook.cpp)
target_link_libraries(orderbook fmt::fmt)
```
=> this example uses fetchContent
    => build time explodes
    => internet required => fetching from online repo
    => dependency versions become messy

    i.e. proj
        -> LIB A reqs fmt v9
        -> LIB B reqs fmt v10 => causes conflict
    => without dependency manager, need to decide manually
    => coz of this, multiple copies of fmt may appear
    => multiple builds, linker conflicts
    => FetchContent(fmt GIT_TAG master) => if master on github changes => build may break

Good Production setup:
```bash
cmake_minimum_required(VERSION 3.20)

project(orderbook)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# find fmt from vcpkg
find_package(fmt CONFIG REQUIRED)

# create executable
add_executable(orderbook
    src/orderbook.cpp
)

# link library
target_link_libraries(orderbook PRIVATE fmt::fmt)
```

### Ninja
- CMake => build generator => creates the build steps inside /build
- Ninja is a build tool => executes the build steps
- clang => actually compiles the code

* ERROR coz i didnt have ninja!!
```bash
Completed submission of vcpkg-cmake:arm64-osx@2024-04-23 to 1 binary cache(s) in 7.5 ms
Waiting for 1 remaining binary cache submissions...
Completed submission of fmt:arm64-osx@12.1.0 to 1 binary cache(s) in 69 ms (1/1)
All requested installations completed successfully in: 4.2 s
-- Running vcpkg install - done
CMake Error: CMake was unable to find a build program corresponding to "Ninja".  CMAKE_MAKE_PROGRAM is not set.  You probably need to select a different build tool.
CMake Error: CMAKE_C_COMPILER not set, after EnableLanguage
CMake Error: CMAKE_CXX_COMPILER not set, after EnableLanguage
-- Configuring incomplete, errors occurred!
joechua@r-61-104-25-172 cpp_orderbook % 
```

i.e. for real projs:
- have multiple cpp files
    src: orderbook.cpp, trade.cpp, matching.cpp, insclude: orderbook.h, trade.h etc.
- compiler need to compile & produce obj files (.o) => not able to execute them directly tho, coz they lack starting point etc.
    i.e. orderbook.o, trade.o, matching.o
- then eventually need to link them
    i.e. orderbook.o, trade.o, matching.o -> executable
exact command:
```bash
clang++ -c orderbook.cpp
clang++ -c trade.cpp
clang++ -c matching.cpp
clang++ orderbook.o trade.o matching.o -o orderbook
# if have dependencies
clang++ orderbook.cpp -I/path/to/fmt/include -L/path/to/fmt/lib -lfmt
```
Cmake helps to include all the src files, dependencies, compile flags & include directories BUT DOESNT compile anything

* This is where ninja comes in
=> runs the actual build

flow:
source code
    ↓
CMake (generate build instructions)
    ↓
Ninja (execute build)
    ↓
clang++ (compile code)

THEREFORE, to install ninja

```bash
brew install ninja
```

* with ninja now installed, can re-run the commands:
`cmake --preset vcpkg` => was the one that failed just now
`cmake --build build`

### FINALLY: resolving the red scribbly lines
- need to add `"CMAKE_EXPORT_COMPILE_COMMANDS": "ON"` into `CmakePresets.json`
    - so that Cmake will output the compile commands into the `build` folder
    - (the file contains the actual compile commands for each source file)
    - it outputs in to `compile_commands.json`
- after u have built successfully again (including compilation via `cmake --build build`)
- go to settings.json to include `clangd.arguments` => because we are using clangd language server
    - it needs to know to look inside the build folder
    - it refers to the `build/compile_commands.json`
    - if `ls build/compile_commands.json` returns nth, it means u didnt include the 
    ```bash
    "clangd.arguments": [
        "--compile-commands-dir=build"
    ]
    ```
- then run: `ctrl + shift + p`, and `clangd: Restart Language Server`
- the red scribbly lines will finally have resolved since intellisense is able to pick up on what is linked to the project...

* note that `cmake --preset vcpkg` technically just runs cmake build with all the presets u had
    - equivalently: `cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON`
    => runs Cmake configure using all preset settings, generates files in build/ (1 of them being build/compile_commands.json)
* then `cmake --build build`
    - runs the actual build
    - compiles src code (using clang/ gcc) then links the executables (uses Ninja if Ninja was chosen as the generator)

# -------------------------------------------------------------------------------------------------
# Re-build
to rebuild, just run:
1. `cmake --preset vcpkg` => only if u changed CMakesLists.txt (i.e. add new src files, changed dependencies, changed presets, build folder doesnt exist etc.)
2. `cmake --build build`

# -------------------------------------------------------------------------------------------------
# styling cpp code
common cpp style
- (1) closing brace should align with the constructor
- (2) body should be indented 1 lvl 
- (3) comments to not be indented
- * just a note that sometimes u see the comments move by 1 space => its coz clang format enforces `SpacesBeforeTrailingComments: 2` and is generally practiced by the industry to make comments more readable
- * sadly my .clang-format for the curly brace formatting is executed after the save

```cpp
class SomeClass{
public:
    OrderBookLevelInfos(const LevelInfos& asks, const LevelInfos& bids)
        : bids_(bids),  // initialize bids => (3)
          asks_(asks) { // (1)
        // test (2)
        some_function();
    }
};
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
# ninja (check which compiler + cpp ver)
after building my project, i was curious to find out which compiler it used + what version of cpp did it compile with

1. which compiler?
2. cpp ver?

## context on what went on during the build process
- wanted to check via ninja; to check if i have ninja installed:
    `which ninja`
- ninja builds project by looking at build.ninja (generated by CMake)
    - usually from a command like `cmake -S . -B build -G ninja`
        - `-S .` -> use current dir as src tree
        - `-B build`-> put all generated build files in `./build`
        - `-G ninja` -> generate build files for ninja
    - or `cmake --preset vcpkg` => uses configs from `CmakePresets.json`
        - reads `CMakePresets.json` => contains (generator, build dir, toolchain(vcpkg), cacheVariables)
            then runs `cmake -S . -B build -G Ninja -DCMAKE_TOOLCHAIN_FILE=vcpkg/scripts/buildsystems/vcpkg.cmake`
        - then these files are referenced in order: `CMakeLists.txt` -> loads vcpkg -> vcpkg reads `vcpkg.json` -> dependecies installed -> CMake generated ninja build files
        - `CMakePresets.json` - defines how to configure the project
        - `CMakeLists.txt` - actual build specs (what to compile, libs to link, std to use)
        - `vcpkg.json` - dependency manifest
        - `vcpkg-configuration.json` - where dependencies come from
    - then `cmake --build build` actually runs `ninja -c build`

## 1. find out which compiler
* run `grep CMAKE_CXX_COMPILER build/CMakeCache.txt`
    -> this greps any line that contains `CMAKE_CXX_COMPILER` in the file `build/CMakeCache.txt`
    -> `CMAKE_CXX_COMPILER:FILEPATH=/usr/bin/c++`
        - `/usr/bin/c++` is usually a symlink to the real compiler (not in our case though)
        ```bash
        joechua@Chuas-MacBook-Air-3 bin % ls -l c++
        -rwxr-xr-x  78 root  wheel  118880 Feb 25 11:41 c++
        ```
        symlinks have 1st letter `l` instead of a - (e.g., lrwxr-xr-x).
    -> its a wrapper

## 2. find out cpp version
- `set(CMAKE_CXX_STANDARD 20)` cpp 20 was set in CMakeLists.txt
