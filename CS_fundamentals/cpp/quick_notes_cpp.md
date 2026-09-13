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
    - cmake --preset => runs cmake to read CMakePresets.json & passes values into CMakeLists.txt to create the build files for the build system
    - cmake --build build => actually runs the build system (cmake, ninja) to compile & link binaries to produce the executable; doesnt use anything from CMakeLists.txt anymore
    - vcpkg.json => config file to include dependencies
    
- private variables
    - are made private when you want to restrict external manipulation, yet you want certain member functions (actions) to access/ modify it
- generally there are 3 ways to avoid duplicate symbol errors
    1. split declaration & definition into .cpp & .h files
    2. merge definitions across all TUs => `inline`
    3. make variable a constant expression => `constexpr`
- static class member variables & functions => class member variables & functions
- be very careful working with floating point numbers! (always assume they are not exact values)
    - rounding errors
    * stems from the fact that we are tying to use binary to represent fractional numbers
- external / internal linakge + TUs
    - adding new class/ functions into a header file
        => #include in the TUs that u want to use those class/ functions
        => update CMakeLists.txt to have that include path for the target
    - adding new functions into a .cpp file
        => ensure new TU is linked with ur current TU 
        => forward declare the function (ensure the compiler can find the symbol's definition)
    - add new function into .hpp file
        => ensure to declare with inline if you define the function inside the header file
        => if not inline, forward declare the function, then define it elsewhere
- ADL + friend methods
- template function definitions must be inside header files
- CMakeLists.txt syntax (target_include_directories, target_link_libraries, include(...))
- GTest + ctest

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# template metaprogramming
- parameter pack
- variadic arguments (via variadic templates & variadic functions)


# ellipsis token `...`
can either use it as a _parameter pack_ OR consume it via _expansions_

## parameter pack
- template/ function parameter that can hold 0, 1 or more args => core language feature making varidaic template possible
- declared with `typename... Name` or `class... Name` => same thing, `class` was just the predecessor as `typename` keyword hadnt exist
```cpp
template<typename... Args>   // Args is a template parameter pack => pack of types declared with `typename... Args`
void foo(Args... args) { // args is a function parameter pack => pack of Values, declared using a template parameter pack as its type, with ... b4 its name
    ...
}
```
- Call foo(1, 2.5, "hi")
    - Args deduces to the type-list int, double, const char*
    - args deduces to the values 1, 2.5, "hi"
- checking sizes
    ```cpp
    template<typename... Args>
    void foo(Args... args) {
        std::cout << sizeof...(Args) << "\n"; // number of types
        std::cout << sizeof...(args) << "\n"; // same number, values this time
    }
    ```

## expansion
- `...` written after a pack name is called an expansion
- "unpacks" the pack into comma-separated arguments
`cpp print(rest...);` => expands rest into however many individual arguments it holds

## summary
`typename... Args` - declares a _template parameter pack_
`Args... args` - declares a _function parameter pack_
`rest...` - expands an existing pack
`args + ...` - fold expression => expand + combine with operator

# variadic arguments
- allow a function to accept arbitrary number of arguments
    => c++ has 2 ways to do this
    => 1. variadic templates(type-safe, compile-time) ; 2. C-style variadic functions (unsafe, runtime)
- 2 techniques to handle variadic templates:
    1. fold expressions (c++17)
        - compiler magic/ compile-time trick (done in templates), not recursion
        - 1 function, no recursion + base case
        - expands arguments into a single expression at compile time
            ```cpp
            template<typename... Args>
            auto sum(Args... args) {
                return (args + ...); // right fold expression => expands to (a + (b + (c + d))) with args a, b, c, d
                // return (... + args); // left fold epxression => expands to (((a + b) + c) + d)
            }
            ```
    2. recursive (c++11/14)
    - chain of function instantiations, 1 per pack size
    - longer compile time: coz compiler needs to genereate N distinct functions that the compiler parsed, deduced, instantiated & emit code for
    - i.e. print(1,2,3) instantiates print<int, int, int>, then calls print<int, int>, then calls print<int>, & finally non-template print() [base case]
    - can put side effects inside function call
        ```cpp
        void print() {std::cout << '\n';}
        template<typename T, typename... Args>
        void print(T first, Args... rest) {
        cout << first << " ";
        print(rest...);
        }
        ```
- C style variadic functions
    ```cpp
    #include <iostream>
    #include <cstdarg>

    // need atleast 1 named arg (i.e. count)
    void printNumbers(int count, ...) {
        va_list args;
        va_start(args, count); // says to start tracking after 'count'
        for (int i = 0; i < count; ++i) {
            // manually tell compiler that args are int type
            // danger: if accidentally pass a double here during runtime, UB!
            int val = va_arg(args, int);
            cout << val << " ";
        }
        va_end(args); // tell the compiler that end of args
        cout << '\n';
    }
    printNumbers(3, 10, 20, 30);
    ```

# non-type template parameter pack/ compile-time integers
- doesnt have to be types, can be compile-time values
- template <int... I> // doesnt take types, takes a list of compile-time integers, each distinct list of ints produces a distinct type
    ```cpp
    template<typename T, int N>
    T multiplyBy(T x) { return x * N; }
    ```
- call it via: `multipleBy<int, 10>(5);` // T is int, N is 10, returns 50

# passing a vector<...> to a template function + returning a compile-time value
```cpp
#include <cstddef> // for size_t

// Vector declaration
template <int... I>
struct Vector { };

// primary template
template <typename V>
struct size;

// specialization: matches any Vector<I...>
template <int... I>
struct size<Vector<I...>> // I... resolves to 1, 2, 3 if it was Vector<1,2,3>
{
   ... // use I... where its 1,2,3 (or wtv was brought in) => can pack expand
   static constexpr std::size_t value = sizeof...(I);
   using result = Vector<I...>; // result is declared here inside specialization, unpack I (expansion of an already bound pack)
}

// ::value -> compile time function that finds size of vector
static_assert(size<Vector<1,2,3>>::value == 3);
static_assert(size<Vector<1,2>>::value == 2);
static_assert(size<Vector<>>::value == 0);

// ::result
size<Vector<1,2,3>>::result // instantiate size with V = Vector<1,2,3>, returns the result of Vector<1,2,3>
```

- why is specialization required?
    - with just the primary template, V is an atomic type, has no way of reaching the compile-time integers
    - even if we gave it a body, it doesnt change that we cant access the values inside `V`
    ```cpp
    template <typename V>
    struct size {
        static constexpr std::size_t value = 0;  // just a placeholder, can't do better
    };
    ```
- specialization, does 2 things
    1. pattern match => detects the Vector<...> pattern
    2. destructures the pattern into a usable pack => I becomes usable

# std::same compile time helper
`std::is_same<typeA, typeB>::value` & `std::is_same_v<typeA, typeB>`
are compile time helper that returns T/F if both types + qualifiers are same/ diff

```cpp
// Old way (C++11)
bool check1 = std::is_same<int, const int>::value; // false

// New way (C++17)
bool check2 = std::is_same_v<int, const int>;      // false
bool check3 = std::is_same_v<int, int>;            // true
```

# -------------------------------------------------------------------------------------------------
# evaluation order
- `,`, `||`, & `&&` are some operators where u'd eval everything on the left first (including side effects) before eval-ing the right side
- `((f() + g()) + h())` // or however it's grouped, compiler was free to execute however it wants => h() 1st then f()

# -------------------------------------------------------------------------------------------------
# aggregate struct

- is a struct that
    - has no user-declared or inherited constructors
    - no private or protected non-static data members => non -static data members must be public
    - no virtual functions
    - no virtual, private, or protected base classes
    - no explicitly deleted constructors
- example:
    ```cpp
    struct Point {
    int x;
    int y;
    };
    // Aggregate initialization
    Point p = {10, 20}; 
    ```

## initializing aggregate struct
- in c++11/ 14/ 17, to inicialize an aggregate struct, must use braces `{}`
    - i.e. `Point P1{1, 2}`
    - can only use paranthese `()` if custom constructor was defined
    - `emplace_back(...)` - constructs object in-place using parantheses construction syntax
        => fails if ur constructing an aggregate struct
        => to achive true emplacement, use nested braces
        => i.e. `emplace_back({1, 2})` => creates Point with x=1, y=2

# -------------------------------------------------------------------------------------------------
# int: passing by value or reference

- int is typically 4 bytes
- reference is typically implemented under the hood by a pointer, which is 8 bytes (on 64 bit system)
- hence passing by value is typically cheaper or identical

# -------------------------------------------------------------------------------------------------
# const auto& vs template

context: when writing functions that take in a few types of arguments, u might face the dilenma
of declaring the argument of the function using `const auto&` or `template<typename T>` to take
in different types of arguments

considerations:
- knowing the concrete shape of argument u are passing in
- what `auto&` compiles down to

## const auto& compiles down to
- `const auto&` in a function parameter desugars to a fully _unconstrained template parameter_ `template<typename T> void f(cosnt T& t)`
- it accepts anything

## decision
_template better_
- `void accumulate_levels(const auto& levels, std::size_t max_levels, std::string& out);` vs
    ```cpp
    template <typename Compare>
        void accumulate_levels(const std::map<Price, PriceLevelVector, Compare>& levels,
                        std::size_t max_levels,
                        std::string& out)
    ```
- the explicit version constraints exactly what should vary, while telling the compiler what could be flexible
* the template function says the key type is always `Price` & value type is always `PriceLevelVector` but the ordering can differ
    => template in this case is better
    => error is immediately raised, instead of being embedded deep inside template instantiation backtrace

_const auto& T better_
- right tool when the function is truly a generic algo


# -------------------------------------------------------------------------------------------------
# qualified expression & ADL

# qualified expression
a qualified name is an identifier that includes an associated scope
most commonly using the scope resolution operator(::) with a namespace or class
i.e. `std::cout`
qualified `std::abs()` vs unqualified `abs()`

# ADL (argument-dependent lookup)
- aka kenig lookup, allows compielr to find
- allows compiler to find & call a function without its namespace prefix by looking inside
    the namespaces of the arguments passed to that function
- i.e.:
    ```cpp
    std::cout << "Hello"; // what the compiler actually sees operator<<(std::cout, "Hello");
    ```
    * ADL runs because it looks into the `std` namespace, & finds a method operator<< with the correct signature
- order of execution:
    1. normal lookup => checks current scope, then global scope. if nothing matches,
    2. ADL => looks at argument, sees it belongs to `std` namespace, searches it & find friend operator<<

# friend
- allows you to access the private members of the class (inside the method you defined)
- if friend not used, you will encounter `error: 'int N::Point::x' is private within this context` error
    when trying to access a private member of the class

# -------------------------------------------------------------------------------------------------
# json parsing

## mapping enum class
there are a few ways to map enum class values to strings:
1. native way: nlohmann/json lib provaides special macro `NLOHMANN_JSON_SERIALIZE_ENUM`
    - example:
        ```cpp
        // inside the header file (i.e. color.h)
        #pragma once
        #include <nlohmann/json.hpp>
        enum class Color {Red, Green, Blue };
        NLOHMANN_JSON_SERIALIZE_ENUM(Color, {
            {Color::Red,    "red"},
            {Color::Blue,    "blue"},
            {Color::Green,    "green"},
        })

        nlohmann::json j = "red";
        Color my_color = j.get<Color>(); // .get<Type>() invoke's macro's conversion function
        ```
    - under the hood implementation of `NLOHMANN_JSON_SERIALIZE_ENUM`
        ```cpp
        inline void from_json(const nlohmann::json& j, Color& e) {
            static const std::pair<Color, nlohmann::json> m[] = {
                {Color::Red,    "red"},
                {Color::Blue,    "blue"},
                {Color::Green,    "green"},
            }
            for (const auto &value : m) {
                if (value.second == j) {
                    e = value.first; // assign to e where e is the variable Color variable created
                    return;
                }
            }
            e = m[0].first;
        }
        ```
    - explanation:
        - relies on ADL(argument-Dependent lookup) c++ feature
        - linear search: O(n)
        - cache locality advantage, less CPU cycles used to find matching type
2. custom unordered_map



# -------------------------------------------------------------------------------------------------
# c++ test framework (Gtest)

claude suggestions: /Users/joechua/.claude/plans/warm-moseying-moore.md
resource: https://google.github.io/googletest/
primer: https://google.github.io/googletest/primer.html
with cmake: https://google.github.io/googletest/quickstart-cmake.html

## building & executing Gtests

`cmake -S . -B build` => build using src dir `.` and build files into `/build`
`cmake --build build` => build executable
`cd build && ctest` => cd to `/build` & run `ctest`
`ctest --test-dir /path/to/build` => run the ctest command from anywhere

## preprocessor macros

`ASSERT_EQ` - checks if 2 values are equal; fails immediately
    => `ASSERT_EQ(x.size(), y.size()) << "Vectors x & y are of unqueal length";`
    => logs failure & custom message

`EXPECT_EQ` - checks if 2 values are equal; continue running the rest of the test
    => `EXPECT_EQ(x[i], y[i]) << "Vectors x & y differ at index" << i;`
    => logs failure & custom message

## boilerplate code (GTest)
example from my 1st cpp test

```cpp
// unit test for kraken_orderbook.cpp + kraken_orderbook.hpp
// friend class of KrakenOrderbook

// from searching online:
// - declaration is done in KrakenOrderbook class (production code)
// - definition is done in a separate .cc file

// from google style guide:
// - generally, .cc files should have an associated .h file, but common exceptions include unit tests & small .cc files containing just main()
// - its common to make a unit test class (KrakenOrderbookTest) a friend of the class it tests (KrakenOrderbook)
// - for technical reasons, `protected` data members are allowed for a test fixture in .cc files

// TSET_F - is a macro, not function
//        - expands into a class defn during preprocessing
// TEST - 

// ASSERT_* - fails and immediately returns test
// EXPECT_* - fails but continue test

#include <gtest/gtest.h>
#include "kraken_orderbook.hpp"
// #include "kraken_order.cpp" // include this? NO => will cause double compilation?
// to make the test executable, we compile this test file + "kraken_order.cpp" but dont link it with main
    // if we link with main, "duplicate symbol: main" error error will be thrown
    // swap it with GoogleTest's main
// full compilation command: g++ -std=c++17 --Wall kraken_orderbook.cpp kraken_orderbook_test.cc /path/to/gtest_main.a /path/to/gtest.a -pthread -o run_tests
    // -pthread - tells compiler to support multi-threading => GTests rely on multi-threading internally
    // run_tests - executable name
// when using vcpkg, need to change the command accordingly
    // -I vcpkg_installed/x64-linux/include \
    // vcpkg_installed/x64_linux/lib/libgtest_main.a
    // vcpkg_installed/x64_linux/lib/libgtest.a
// if using cmake, update CMakeLists.txt that produces 2 executables:
    // find_package(GTest CONFIG REQUIRED)
    // if (GTest_FOUND)
        // add_executable(run_tests
            // kraken_orderbook_test.cc
            // kraken_orderbook.cpp
        // )
            // target_link_libraries(run_tests PRIVATE GTest::gtest GTest::gtest_main)
        // # include `src/` directory so `test/` files can include src files
        // # this is idiomatic fix over relative imports; tests files dont require remembering relative paths even when they change subdirectories in the future
        // # CMAKE_SOURCE_DIR is built-in CMake variable => derived from the file containing project()
        // target_include_directories(run_tests PRIVATE ${CMAKE_SOURCE_DIR}/src)
    // endif()


// :: is global scope resolution operator => accesses a global variable over local names; protect against name conflicts with custom namespaces
// ::testing is a namespace (namespace => scope region that acts as a container to prevent name collisions)
// ::testing::Test - is the base class for all google tests
// KrakenOrderbookTest : public ::testing::Test - creates a test fixture class => provides related tests with a common + repeatable env
class KrakenOrderbookTest : public ::testing::Test {
protected:
//     void SetUp() override{...} // code that runs b4 every single test
//     void TearDown() override{...} // code that runs after ever test

    KrakenOrderbook book{30};
    
// TEST(TestSuiteName, TestName)
    // TestSuiteName - is just a name chosen for related tests
    // TestName - name of specific test
    // - inherits from ::testing::Test
    // - shares no variables => doesnt inherit from the fixture class, so no global variables
    // - used for basic test without a set env
// TEST_F(FixtureClass, TestName) macros auto create C++ classes bts
    // - these classes inherits from fixture class (KrakenOrderbookTest)
    // - methods should be made avail to child classes, but not used outside of tests (no need public)
// TEST vs TEST_F
    // TEST_F resets state of env for every single test
    // TEST doesnt have a base state

    // OTHER methods here:
};


// test cases to be writen here:
// TEST_F(KrakenOrderbookTest, PlaceholderExample) {
    // ASSERT_* fails and returns immediately from this test.
    // EXPECT_* fails but lets the rest of the test body keep running.
//     ASSERT_TRUE(true);
// }
```

## comparing values example code

```cpp
// good way to compare:
// - no need equality function
// - declarative style, know exact test that fails
TEST_F(KrakenOrderbookTest, ParseMessageWiresFieldsCorrectly) {
    std::string raw = R"({"channel": "level3", "type": "update", "data": [{"checksum": 2753097282, "symbol": "BTC/USD", "timestamp": "2026-07-07T22:22:09.618135048Z", "bids": [], "asks": [{"event": "add", "order_id": "OL45ED-RT7DI-GVJ7C4", "limit_price": 63433.6, "order_qty": 0.00126168, "timestamp": "2026-07-07T22:22:09.618135048Z"}]}]})";
    L3Message parsed = parseMessage(parseRaw(raw));
 
    EXPECT_EQ(parsed.type, MessageType::Update);
    EXPECT_EQ(parsed.symbol, "BTC/USD");
    EXPECT_EQ(parsed.checksum, 2753097282u);
    ASSERT_EQ(parsed.ask_orders.size(), 1u);
    EXPECT_EQ(parsed.ask_orders[0].order_id, "OL45ED-RT7DI-GVJ7C4");
}


// bad way && unsure which test fails
TEST_F(KrakenOrderbookTest, parse_message) {
    json msg = parse_raw(add_ask_str);
    L3Message parsed_msg = parse_message(msg);

    // create order: {"event": "add", "order_id": "OL45ED-RT7DI-GVJ7C4", "limit_price": 63433.6, "order_qty": 0.00126168, "timestamp": "2026-07-07T22:22:09.618135048Z"}
    L3Order order{
        EventType::Add,
        "OL45ED-RT7DI-GVJ7C4",
        6343360000000,
        126168,
        1'783'462'929'618'135'048
    };

    // compare parse_message with accurate message
    EXPECT_EQ(parsed_msg, (L3Message{
                              MessageType::Update,
                              "BTC/USD",
                              2753097282,
                              1'783'462'929'618'135'048,
                              std::vector<L3Order>{},
                              std::vector<L3Order>{order}
    }));
}
```

# -------------------------------------------------------------------------------------------------
# cmake

rsource: https://cmake.org/cmake/help/latest/guide/tutorial/index.html

## cmake operations

- FetchContent(lib) - downloads the library
- find_package(lib) - looks for the package on the computer
- include(module_name) - looks for module_name.cmake in CMAKE_MODULE_PATH
    _include(GooglTest)_ - looks for GOogleTest.cmake in CMAKE_MODULE_PATH
    => cmake searches for file named GoogleTest.cmake since CMake ships 1 bundled in its own `Modules/` dir
    => `GoogleTest.cmake` is not a Find module (different from `FindGTest.cmake`)
    => its a utility module that defines `gtest_discover_Tests()` function
    => `gtest_discover_Tests()` - runs ur test binary with `--gtest_list_tests` which registers each test individually with CTest
    => FindGTest.cmake -> locates GTest, defines GTest::gtest targets (used via `find_package`)
    => GoogleTest.cmake -> defines helper functions for CTest integration (used via `include`)
- enable_testing() - enables testing for the current dir & below (allows CTest to find your tests)
    => sets up testing machinery & generates `CTestTestfile.cmake` so that CTest reads & know where tests are (without this, `gtest_discover_test` wont discover any tests)
    => CTest is the built-in test driver thats part of the CMake suite of programs
    => https://cmake.org/cmake/help/latest/command/enable_testing.html
- `include(GoogleTest)` & `gtest_discover_test(executable_name)`
    - `include(GoogleTest)` loads the module that defines `gtest_discover_test`
    - `gtest_discover_test(executable_name)` registers executable_name's individual tests with CTest
    => ctest can now find & run tests individually

## compile_commands
- -isystems - adds a dir to the include search path (like `-I`), but the diff is that they are treated as system headers
    => warnings are typically suppressed(even with `-Wall -Wextra`) => becoz u didnt write the code, cant fix it & it clutters build output
    * note: none of the compiler flags help include the default include path. its that compiler's 1st search step is to look in the dir containing the file with `#include`
- -iquote - adds dirs to quote-search behavior (for `""`-style includes, not `<>`)

## cmake `find_packages` + `CONFIG / REQUIRED`

- `REQUIRED` - means "hard-fail configure if not found"
- `CONFIG` - controls how find_packages search:
    - module mode (default, tried first) - cmake looks for FIND<NAME>.cmake script => either bundled with cmake OR supplied in the project
    - config mode - cmake looks for FIND<NAME>.cmake (or <name>-config.cmake), a file that the pckg installs alongside headers + libs => describes its own targets

_behaviors_
find_package(package_name REQUIRED)         - module mode 1st (default), then fall back to config mode if no find module exists
find_package(package_name CONFIG REQUIRED)  - config mode only
find_package(package_name MODULE REQUIRED)  - module mode only

_GTests_
* special case: `find_package(GTest CONFIG REQUIRED)` CONFIG is mandatory
- cmake ships its own bundled `FindGTest.cmake` (predates modern Gtest's own exported targets & can define things differently)
- vcpkg also installs GTest which shipds its own `GTestConfig.cmake` with proper `GTest::gtest` + `GTest::gtest_main`
- since a Find module exists, it gets picked up first & may not resolve to vcpkg installed ones correctly
- forcing CONFIG mode ensures cmake uses installed config file & not cmake's bundled module

* module mode is quite legacy, where cmake used to update `Modules/` dir (installed alongside CMake binary) containing a set of Find<Name>.cmake scripts for
    libs that were popular in C/C++ b3 native cmake config-file export was common (i.e. Boost, OpenSSL, GTest, ZLIB, Threads, PNG, Python etc.)

## cmake inheritance: `target_include_directories` * `target_link_libraries` + `PUBLIC / PRIVATE / INTERFACE`
resource: https://leimao.github.io/blog/CMake-Public-Private-Interface/

- in cmake, u define an executable or lib target b4 linking it
- some files have `#include` preprocessor directives that require pulling code not from the standard include directories
- cmake has `INCLUDE_DIRECTORIES` & `INTERFACE_INCLUDE_DIRECTORIES` internal variables which has similar behavior to using `-I` compiler option
- `target_link_libraries` & `target_include_directories` populates all such directories to `INCLUDE_DIRECTORIES` &/or `INTERFACE_INCLUDE_DIRECTORIES` variables depending on the keyword specified
    * cmake keywords `PUBLIC`, `PRIVATE` & `INHERITANCE` are used in `target_include_directories` & `target_link_libraries`

_target_xxx_
- `target_include_directories` tells the compiler where to find the .h or .hpp files
- `target_link_libraries` tells the linker where to find pre compiled binary lib files (.a, .lib or .so) => .a .lib files are basically a bundled file of .o object files aka library files
* when using libs, u need to provide header files that contain the interface (target_include_directories) but also link libs to the target for its defn (target_link_libs)

_PUBLIC/PRIVATE/INTERFACE_
PUBLIC - all dirs following PUBLIC will be used for current taget & other targets that have dependencies on the current target
    => append directories to `INCLUDE_DIRECTORIES` & `INTERFACE_INCLUDE_DIRECTORIES`
PRIVATE - all dirs following PRIVATE will only be used for current target
    => append dirs only to `INCLUDE_DIRECTORIES`
INTERFACE - all dirs following INTERFACE will not be used for current taget, but is accessible for other targets
    => append dirs only to `INTERFACE_INCLUDE_DIRECTORIES`
* basically, INTERFACE is usually for other programs to use currently-being-compiled-program's methods
    then PUBLIC is for both
    and PRIVATE is when the currently-being-compiled-program needs access to some header/ lib

_target_link_libraries_
`target_link_libraries(<target> <PUBLIC/PRIVATE/INTERFACE> <item>)`
- CMake would append `INTERFACE_INCLUDE_DIRECTORIES` of <item> to `INCLUDE_DIRECTORIES` of <target>
    * => basically when we link an item to the target
      => we want to be able to use the methods from the <item> inside the <target>
      => hence we need to #include those header files into the <target>'s include dirs

_header only libs_
add_library(my_lib INTERFACE)   => define the lib as INTERFACE meaning it has no .cpp
target_include_directories(my_lib INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/include)    => tell cmake directory for header files
add_executable(program main.cpp)    => create executable
target_link_libraries(program PRIVATE my_lib)   => "link" the header-only lib to executable

* special case for nlohmann:
add_executable(program main.cpp)    => create executable
target_link_libraries(program PRIVATE nlohmann_json::nlohmann_json)     => passes the header location to main.cpp

(because nlohmann_json's src code contains another CMakeLists.txt file)
inside nlohmann_json's CMakeLists.txt:
add_library(nlohmann_json INTERFACE)
target_include_directories(nlohmann_json INTERFACE)

## cmake commands
- `cmake --preset <preset_name> --fresh`
    => discards cache & regenerate makefiles from scratch
    * do this when there are changes to `CMakeLists.txt`

- `cmake --build <path/to/build_dir> --clean-first`
    => --clean-first runs the equivalent of `make clean`
    => but `make clean` doesnt remove the cache from cmake --preset (i.e. CMakeCache.txt) as those are config files; not already compiled binary


# -------------------------------------------------------------------------------------------------
# template functions in header
Q. why template function definition is done in header, & not separate .cpp file

normal function definitions in separate .cpp file:
- normal function gets compiled into machine code once the compiler sees its defn
- g++ compiles definition.cpp & produces definition.o (blob of machine code + symbol table)
- linker later just finds 1 compiled symbol & uses that

templates:
- template is not a function, its a recipe for generating a function (when the typename is specified for e.g.)
- nothing gets compiled until an instantiation happens
- a definition of the template function in a separate .cpp file will not result in a blob (refer to nex point for further expln)
    - i.e. add_order's defn lives in a separate .cpp file (impl.cpp). that file gets compiled on its own. the compiler looks at template<...< void add_order(...){...} but sees no call-site, so it generates 0 code. its skipped over. another file (other.cpp) gets compiled, sees add_order(...) I& resolves it to add_order<std::greater<Price>>, & now requires the defn. but it only sees the declaration without a recipe & hence fails to compile, emitting "unresolved symbol, please find it" error
- compiler requires 1 of 2 things:
    1. full template definition(recipe) at the call site, hence #include <header.hpp> with the definition inside allows any .cpp file to see the full recipe
        (basically needs the recipe to generate machine code for specific instantiation)
    2. already generated machine code (not able to have this since its a template function & not normal function)

# -------------------------------------------------------------------------------------------------
# std::unorder_map
- do `auto it = orders.find(order.price);` and not `auto& it = orders.find(order.price);`
- coz `.find()` returns a value type `Iterator`, and not a reference to an already existing object

## bad ways to retrieve/ get value (string_view)
```cpp
OrderBook books_for(std::string_view symbol) {
    return book.symbol_to_books_.at(std::string(symbol));
};

// bad ways to access keys that are string when taking in a string_view
- book.symbol_to_books_[symbol.data()]; // bad: because .data() could return a non null-terminated string (.data() is not guaranteed to be null-terminated)
- book.symbol_to_books_[std::string(symbol)]; // still bad: [] is used; could silently defauly construct a brand-new empty OrderBook => use at(), find()
```
- std::string(...) => does a safe copy into a string

## retrieve/ get value from key-value pair
`auto it = m.find(key)` vs `T val = m.at(key)`
- `find()` cost is free after
    - answer is already sitting in a register/ iterator
    - compare iterator to end() is a single branch
    - branch predictor typically predicst it => more common to hit than miss
- `at()` + `try`
    - non-throwing path is same as `find()`
    - throwing path needs to
        1. allocate exception object (typically heap allocations via `__cxa_allocate_exception`)
        2. call `__cxa_throw` => needs to walk down call stack frame by frame
        3. at each frame, runs "personality routine" to check whether a matching catch exists
        4. if no match, calls destructors for every local obj in that frame
        5. once a matching catch is found, transfer control
- `contains()` + `at()`
    - does the work twice since `contains()` finds key & checks `if != end()` essentially
* if needing to check + value, just do `find()`

- example code:
    ```cpp
    // find()
    auto it = m.find(key);
    if (it != m.end()) {
        // it->second is the val
    } else { } // not found

    // at()
    auto val = m.at(key); // throws std::out_of_range error if missing
    // can either do try-catch
    try {
        auto value = m.at(key);
    } catch (const std::out_of_range& e) {
        std::cout << "key doesnt exist";
    }
    // or do if (m.contains(key)) => c++ 20 feature
    if m.contains(key) {
        auto val = m.at(key);
    }
    ```

## combine lookup & branch
- is an init-statement; 
- only allowed in c++17 onwards
- `auto it = m.find(key); it != m.end()` returns the bool from `it != m.end()`
- WARNING: cant use it outside the scope of the statement
    - only within the if-else blocks
```cpp
if (auto it = m.find(key); it != m.end()) {
    auto val = it->second;
} else { } // key dont exist

// CANT USE it HERE!
```

# -------------------------------------------------------------------------------------------------
# std::vector

# delete
    auto it = std::find(v.begin(), v.end(), value)
    if (it != v.end()) { v.erase(it); }
* erase takes everything after the erased pos & shifts it 1 slot left via `memmove`
* erase never triggers reallocation (only growth does); need to explicitly call `shrink_to_fit()` => only push_back/ insert/ resize

# -------------------------------------------------------------------------------------------------
# std::list

## roughy layout
- has a Node that is contained by the iterator class

struct ListNode {
    T value;
    ListNode* prev;
    ListNode* next;
}
class ListIterator {
    ListNode* n;
public:
    T& operator*() cosnt { return n->value; } // dereference the node ptr
    ListIterator& operator++() { n = n->next; return this; }
    etc.
}

## insert
2 ways to get `it` when inserting a node into a linked list:
1. 
orders.push_back(order)
auto it = std::prev(orders.end()) // iterator to the element u just added
2. 
auto it = orders.insert(orders.end(), order); // insert() returns the iterator to the inserted ele directly

## delete

```cpp
// std::list version
void KrakenOrderbook::delete_order(const L3Order& order, std::map<Price, PriceLevelContainer>& orders) {
    auto lookup_it = order_id_to_order_.find(order.order_id);
    if (lookup_it == order_id_to_order_.end()) {
        return; // or throw — order doesn't exist, shouldn't happen on a valid feed
    }

    const OrderLocation& loc = lookup_it->second;

    // jump straight to the price level — no scanning
    auto level_it = orders.find(loc.price);
    if (level_it != orders.end()) {
        level_it->second.erase(loc.it); // O(1) if PriceLevelContainer is std::list
        if (level_it->second.empty()) {
            orders.erase(level_it); // clean up empty price levels
        }
    }

    order_id_to_order_.erase(lookup_it);
}
```

# -------------------------------------------------------------------------------------------------
# adding <bits/stdc++.h> to include path

- code found here: https://github.com/khaveesh/macOS-stdc.h
- cd to include search path/ include path: `/Library/Developer/CommandLineTools/usr/include`
- create `bits` folder
- in bits folder, create file `stdc++.h` & copy contents from the repo

* compilers contain default header files inside the _include search paths_, where they append that with the path of the lib ur trying to include

# -------------------------------------------------------------------------------------------------
# checking compiler's base include paths

`clang++ -x c++ -E -v /dev/null 2>&1 | grep -A20 '#include <...>'`
- `-x c++` execute file as cpp no matter the extension
- `/dev/null` default empty file that all unix dir has
- `-E` means to stop after preprocessing
- `2>&1` redirects stream 2 (stderr) into stream 1 (stdout)
- `| grep -A20` pipes output into grep command, searches for literal line '#include <...>', then A20 is to print 20 lines even after the match
    clang's diagnostic message prints out the actual header paths

* will notice that 1 of mac's path is: `/Library/Developer/CommandLineTools/usr/include`

# -------------------------------------------------------------------------------------------------
# installing gcc compiler on mac
- main reason: to be able to use headers specific to gcc compiler (i.e. #include <bits/stdc++.h>)
- codeforces thread: https://codeforces.com/blog/entry/70957
- video that helped: https://www.youtube.com/watch?v=-edTHKZdkjo
    - created symlink to g++ binary, so vscode now uses that binary instead of clang
# -------------------------------------------------------------------------------------------------
# runtime variable used in array declaration

you might think this should work right:
int d;
cin >> d;
array<int, d> min_time_arr {};

but generally this is not allowed:
- compiler requires the int value to be a compile-time constant becoz the size is part of the type itself

generally this is discouraged becoz:
- potential unbounded stack growth during runtime => stack overflow error
- templates need to know size to generate code

* generally, if size is only known during runtime, need to use vector

# -------------------------------------------------------------------------------------------------
# reading text (cin)

- cin ignores leading whitespace
- getline(cin, storage_var) consumes line + \n BUT doesnt ignore leading whitespace
- std::ws helps to ignore leading white space

```cpp
int age;
std::string name;
int zip;
std::string city;
std::string town;

std::cin >> age; // no matter "\n\n   \n 15", this will just return 15
std::getline(std::cin >> std::ws, name); // but getline reads leading whitespace, use std::ws

std::cin >> zip;                         // Automatically skips any whitespace left by 'name'
std::getline(std::cin >> std::ws, city); // Needed: Clears newline left by 'zip'
std::getline(std::cin, town); // this is now fine, no \n leftover
```

# -------------------------------------------------------------------------------------------------
# if else & switch statements

## if else UTH
- c++ has no `else if` keyword
- its just if & else, parser lets a single statement follow else without braces
- if is a statement, this is actually what happens:
    ```cpp
    if (a) {
        // ...
    } else if (b) {
        // ...
    } else {
        // ...
    }

    // same as:
    if () {

    } else
        if () {

        } else {
        
        }
    ```

## advantages of switch

- usecase: _single value equality checks_
- exhaustiveness wanrings: if new enumerator added, & forgot to handle in switch, most compiler will warn u at compile time
- slightly better codegen potential: compilers can sometimes generate a jump table instead of sequence of comparisons

## advantages of if else

usecase: checks compound/ range conditions

## common gotchas
- switch dont work on `std::string`, but works on `enum class`es
    - switch is designed to compile to a jump table or comparison tree, not runtime comparisons
    - an array of label addresses indexed by x's value, & at runtime it computes jump_table[x] => O(1)
    - no sequential comparisons (std::string cant do this; its operator== does runtime byte comparison)
    - enum class values are compile-time constants, hence can be used
- remember to break after every case!
```cpp
switch (side) {
    case Side::Buy:
        do_buy();
        // no break! falls through to sell case too
    case Side::Sell:
        do_sell();
        break;
}
```

# -------------------------------------------------------------------------------------------------
# bad pointers (dangling pointer, null pointer)

- dangling pointer - points to MEM that was once valid but has been freed (still holds the address)
- null pointer - explicitly points to nullptr

# -------------------------------------------------------------------------------------------------
# C-style arrays vs std::array

## std::array misconception

misconception: allocates MEM On the heap
correct: storage depends on where you declare them (just like C-style arrays)

```cpp
// C-style arrays
int a[10]; // (stack)
static int b[10]; // static storage (data segment)
int* c = new int[10]; // dynamic storage (heap)

// std::array
int a[10]; // (stack)
static int b[10]; // static storage (data segment)
int* c = new int[10]; // dynamic storage (heap)
```

## std::array design & advantages

MAIN ADVANTAGE: safe & has 0 runtime overhead (doesnt affect performance)

_design_
- designed with no extra storage behavior
- just adds bounds-aware member functions (.size(), .at(), iterators etc.)
- 0 runtime overhead (no pointer indirection, no allocation)

_advantages_
1. no decay when passed around
    C array decays to a pointer; lose the length silently
    ```cpp
    void f(int arr[10]) { sizeof(arr); }   // arr is now int*, size info GONE
    void g(std::array<int,10> arr) { arr.size(); }  // still 10
    ```
2. copyable & assignable
    C arrays are not copyable, assignable & cant be returned by value from a function
    C's guiding principle is to not silenty generate expensive ops
    given that array is not a first class obj, programmer has to explicitly do the copy
    ```cpp
    // C arrays
    int a[5] = {1,2,3,4,5};
    int b[5];
    b = a; // ERROR
    memcpy(b, a, sizeof(a)); // ok, explicitly do the copy, visible cost
    
    // std::array
    std::array<int, 5> a = {1,2,3,4,5};
    std::array<int, 5> b;
    b = a; // does element-wise copy
    ```
3. bounds check
    C arrays 
    `operator[]` is both unchecked for speed, but std::array allows u to check if u want
    ```cpp
    int a[5] = {1,2,3,4,5};
    std::array<int, 5> a2 = {1,2,3,4,5};
    a[10]; // undefined behavior, silently corrupts memory or crashes
    a2[10]; // undefined behavior
    a2.at(10);   // throws std::out_of_range
    ```

## implementation notes

how was C arrays returned in the past?

1. _heap allocation_
```cpp
int* makeArray() {
    int* arr = new int[5]{1,2,3,4,5};
    return arr
}
```
- manual lifetime management pattern observered, bad! (c++ avoids this)
- ez to forget to free it, ez to leak

2. _passing buffer_
```cpp
void fillArray(int (&out)[5]) {
    for (int i = 0; i < 5; ++i>) { out[i] = i + 1; }
}
int b[5];
fillArray(b);
```
- this is traditionally whats done, with no heap allocation

3. _struct_
```cpp
struct ArrWrapper {int data[5];};
ArrWrapper makeArray() {
    return ArrWrapper{{1,2,3,4,5}};
}
```
- structs are copyable/ returnable
- works, & is essentially what `std::array` does (with a few other stuff)
- concern: because arr is copy, wouldnt this function be very expensive?
    expln: NRVO helps elide copies & URVO (as of c++17) mandatory copy elision if u use prvalue

* note that in arrays, there is no difference between size & capacity
    std::arra<int, 5> has 5 ints ALWAYS constructed

# -------------------------------------------------------------------------------------------------
# casting & rounding

initial attempt (but its wrong):

`Price price = static_cast<int64_t>(val * 100'000'000.0);`
- floating point multiplication might not return exact integer
    i.e. `60371.5 * 100000000.0` could = `6037150000.0000001` or `6037149999.9999999`
- a plain `static_cast` _truncates toward zero_ (anything that is supposed to round up is wrong)
- hence, you round first (since u already expect an int), then truncate

* best practice: round b4 casting

`Price price = static_cast<int64_t>(std::llround(val * 100'000'000.0))`

std::llround - rounds to the nearest long long (half-away-from-0)

# -------------------------------------------------------------------------------------------------
# default arguments

## include in header or .cpp files?

rule: default arg values live in the header declaration, not in .cpp definition

why?
- they are default args part of the function interface
- tells users that they can omit that arg & use the default val; .cpp should only contain body, displaying the implementation of the fn
- if default are placed in both places, the compiler sees 2 specifications of the same default & rejects; violates ODR rule
    - if default was placed in the .cpp file, it might be missed by the user when referring to the interface (header)

```cpp
// orderbook.hpp — default value goes HERE, in the declaration
class KrakenOrderbook {
public:
    explicit KrakenOrderbook(std::string symbol, size_t depth = 10);  // default here
};

// orderbook.cpp — NO default value in the definition
KrakenOrderbook::KrakenOrderbook(std::string symbol, size_t depth)    // no default here
    : symbol_{std::move(symbol)}
    , depth_{depth} {}
```

# -------------------------------------------------------------------------------------------------
# include header files

- when CMake compiles .cpp files, it pass `-I/path/to/src` as a compiler flag
- include compiler flag(`-I`): this tells compiler to look in the src directory when `#include` preprocessor directive is encountered
- 2 types of include:
    1. quotes "" => searches same dir as the file doing the including, also searches folder that was included via `-I`, then finally fallbacks to same paths as <>
        * `quote-include same-dir rule` even without `-I` flag, header files in the same dir as the .cpp file being compiled can be found
    2. angle brackets <> => searches system/ external paths (vcpkg installed paths, system headers)
        => skips "relative to current file" check & immediately checks `-I` & `-isystem` search paths
- typically, header files in the same directory can be included without extra keywords
    - (i.e. `#include "something.hpp"` inside `something.cpp` when both are in `src/` dir is fine)
    - BUT `#include "something.hpp` or even `#include "src/something.hpp` fails when inside a diff dir like `test/` coz compiler doesnt search up that directory for header files


## using pragma once (header guard) & separate .cpp file for definition

(recap: # Memory regions & transaltion units)

_#pragma once_
- used as a header guard
- ensure that nested header files that include this dont re-declare the same declaration

_separate .cpp file_
- a separate .cpp file is used for function definition
- this ensures that between TUs, the same function is not defined twice (only their declarations are made; forward declared)

### #pragma once or #ifndef?

Traditional #ifndef guard:
- c++ standards-compliant (technically #pragma once is a compiler extension, not in the C++ standard)
- Guaranteed to work on every C++ compiler
- BUT need to invent macro name, more verbose

#pragma once:
- simple, one line, no macro name to invent or typo
- No risk of macro name collision (if two different headers accidentally use the same guard macro name, 1 silently never gets included; hard-to-debug this)
- Slightly faster compilation on some compilers since the compiler can skip opening the file entirely once it's seen it, rather than opening it, reading the macro, then deciding to skip

* generally use #pragma once when using gcc + linux (supported for many years already)

### separate .cpp file or inline for definition

how the error comes about:
- if 2 (or more) .cpp files include the same function body via the same header, compiler will process the files separately
- linker tries to combine both `.o` files into 1 executable & finds a repeat definition
- this violates ODR (1 definition rule) => linker error: error: multiple definition of `some_function`

_separate .cpp file_
- forward declares identifier using header file
- definition is written in .cpp for linker to use
- doesnt force re-compilation for every file that requires that definition

_inline_
- tells compiler to pick 1 of the definition (the assumption is that all are the same)
- convenient if its a simple method/ function

* guideline:
trivial (just initializer list, empty body) => inline in header, fine
non-trivial (any real logic in the body) => define in .cpp
* if alot of files use that definition, better to just place it in a separate .cpp so all those files dont have to get re-compiled

# -------------------------------------------------------------------------------------------------
# .c, .cpp, .h, .hpp

- .cc - preferred at google (google's c++ style fuide explicitly recommends it) comes from the C-with-classes era
    - .cpp was initially adopted as the convention but "cpp" already existed as the name of the c preprocessor program, there were changes of mistaking the ..cpp file with the .i file
    - hence it was change to .cc
    - but both can be used, .cc stuck in unix descended eco systems
    - while .cpp became the defacto standard especially in Windows envs with VS historically defaulting to .cpp for new c++ projs
- .cpp - most common, used by most Open sourced c++ projs in MSVC / VS projects
- .h - historically associated with C headers (kind of signifies that this header could be C compatible)
- .hpp - signals this is specifically c++ (uses classes, templates, namespaces, etc.); unambiguouosly not C
    * these are purely conventions

# -------------------------------------------------------------------------------------------------
# size_t

```cpp
#include <cstddef>
#include <cstdlib> // also defines size_t
KrakenOrderbook(size_t depth = 10) {}
```
- `size_t` is used to represent non-negative integers -- unsinged integrer types
- isnt a built-in keyword (unlike int), its a typedef type defined in the C std lib headers

# -------------------------------------------------------------------------------------------------
# cant bind a non-const lvalue reference to a temporary obj

```cpp
int func() {
  result = 3;
  return result;
}
int& test = func(); // compiler ERROR here
```

- `return result` copies or moves the value out into a temporary obj
- the local variable is destroyed
- when the expression func() is evaluated, the temporary will be destroyed, & hence the compiler
    throws the error

## temporary object is rarely created

```cpp
Foo f() {
   Foo local(42);
   return local         // move/ copy elision directly, no temp (both cases)
}

FOo g() {
    return Foo(42)      // prvalue, mandatory elision, no temp
}

Foo h(Foo param) {
    return param        // named object, move/ copy elision, no temp
}
```

- even in the "worst case" NRVO fails, move operation is done directly from the local into the caller's slot
    => no temp created
- note that "return slot" is the "caller's slot"
    - so the 1st 2 cases, both Foo objects r constructed in the return slot, which is also the caller's slot
    - the last case, params have fixed storage due to calling convention, but is moved to the return slot / caller's slot

## when temporary object is created

```cpp
// CASE 1: type mismatch forcing conversion
Foo f() {
    Bar b;
    return b;   // Bar -> Foo conversion needed
    // 1. if Foo has converting constructor Foo(const Bar&), a temp Foo is created from b
    // 2. temp Foo is then moved into return slot
}

// CASE 2: temp object created to be binded to
void take(const Foo& f) { /* ... */ }
take(Foo(42)); // Foo(42) is a prvalue; an obj needs to exist for f to bind to; temp is destroyed at the end of the full expression
```

## return by reference (bad)

```cpp
const Foo& make() {
    return Foo(42);   // returns a reference to a temporary
}                     // temporary dies here, at end of full expression
                      // caller's reference is now dangling
const Foo f = make(); // dangling reference (copy attempt on a dead object)
// const Foo& f = make(); // dangling reference (no copy on dead object; reference just set on it)
```
- no life time extension applies
- becoz temporary isnt bound to a reference variable at its point of creation (like in parameters)
- its bound to a function's return type; & the rule doesnt reach through that
- undefined behavior occurs

# -------------------------------------------------------------------------------------------------
# (const T& x) variable / parameter type

`const T& x = __;`
or `void func(const T& x)` - can bind to anything that can produce an object of type T (or something convertible to T)

- accepts `T`
- accepts `const T`
- accepts `T&&` (rvalue)
* least restrictive reference type as it promises not to modify the object (at its source)

# -------------------------------------------------------------------------------------------------
# parameter & argument (recap; refer to LearnCpp.com chp 2.4)

- _parameter_ - variable used in the header of a function; variable declared in the function's signature - placeholder that exists at the point of definition;they are initialized with a value provided by the caller of a function
- _argument_ - value that is passed from the caller to the function when function call is invoked

i.e. in an error message:
```bash
"no known conversion for argument 1 from ‘const boost::asio::io_context’ to ‘const boost::asio::basic_stream_socket<boost::asio::ip::tcp>::executor_type&’ {aka ‘const boost::asio::any_io_executor&’}"
```

this means that the compiler tried to convert your arg's type X into the parameter's declared type Y -> arg 1 cant convert to the necessary type.
i.e. the object being passed into the function is of type string, but the function parameter is an int
the compiler would then return: `no known conversion for argument 1 from ‘std::string’ to ‘int`

# -------------------------------------------------------------------------------------------------
# git

recap:

- rebase - has to pull in the changes from the remote repo, apply it to my local branch, then replay my changes on top of that (forcing devs to resolve conflicts locally before pushing)
- merge - creates a new commit where differences are resolved by comparing the latest commit and my changes

* both will retain the original commits from the respective "feature" branches

`git pull --rebase origin master`
this means to execute rebase using my changes on to the remote repo "origin" on the master branch
by pulling the changes down to my local repo, applies local changes on top of them
- executes `git fetch origin master` first - fetches changes
- then does the rewind(rolls back to moment before new changes), catch up(applies remote changes), rebase(applies local changes - requires you to de-conflict conflicts)

# -------------------------------------------------------------------------------------------------
# which

`which` command on the command line - searches for binary files or script that can be found through the physical directory paths listed in my system's $PATH variable, which matches the name given

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
# copy & move constructors (implicit generation & deletion)

## implicit copy constructor generation [learncpp.com chp14.1]

(when no move constructor / assignment oeprator is declared) copy constructor is implicitly declared

```cpp
// implicit copy constructor
Class(const Class& other)
    : m_member1(other.m_member1) {}
    , m_member1(other.m_member1) {}
    ...
```
- it does memberwise copy
- if member is a pointer, it will just copy the address of that pointer

## deleting copy constructor manually (= delete) [learncpp.com chp14.1]

- can manually declare copy constructor as deleted
    `Class(const Class& other) = delete;`
- and delete copy assignment constructor too 
    `Class& Class(const Class& other) = delete;`
- this goes from "compiles fine, breaks at runtime" to "compiler refuse to build"

## shallow vs deep copy [learncpp.com chp21.1]

## move constructor / move assignment [learncpp.com chp22.3]

if user-declare a move constructor / move assignment operator, the compiler implicitly declares copy constructor as delete

## rule of 5 [learncpp.com chp22.3]

resource management guideline states - if a class explicitly defined / delete any of the 5 special member functions, it should explicitly define or delete all 5

when manually managing a resource, the compiler's default behvior is often not enough; need to provide custom implementations for:
1. destructor: ~Class()                                                 => frees up the resource when object goes out of scope
2. copy constructor: `Class(const Class& obj)`                          => creats a new object by creating a deep copy of an existing resource
3. copy assignment constructor: `Class& operator=(const Class& obj)`    => safely _updates_ an existing object by copying another object's resource
4. move constructor: `Class(Class&& obj)`                               => creates a new object by stealing the underlying resource of a temporary object
5. move assignment constructor: `Class& operator=(Class&& obj)`         => _cleans up an existing object's_ current resource and steals the resource of a temporary object.

* the main difference between _assignment_ & pure _construction_ is that pure construction just requires creating a new resource without MEM being allocated yet, whereas assignment has MEM already allocated with an old value that needs to be deleted
* _single ampersand(&)_ creates a _standard reference_ that binds to a permanent _lvaule_
* _double ampersand(&&)_ creates an _rvalue reference_ that binds to temporary _rvaule_ => specifically for temporary objects
    * lvalues - objects that have name & persistent MEM
    * rvalues - temporary, nameless values that exist only on the right side of an assignment expression

## OVERALL

if nothing defined, copy constructor assumed
if move constructor defined, no copy constructor

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



## different files

- vcpkg.json - include dependencies here; read by vcpkg to download packages
- CMakePresets.json - declare presets here; `cmake --presets preset` replaces the command `cmake -S . -B build -G Ninja -DCMAKE_TOOLCHAIN_FILE=vcpkg/scripts/buildsystems/vcpkg.cmake ...`
    - this basically generates the build files (.ninja files) for ninja to run later during `cmake --build build`

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

## better re-write of string concatenation

_bad version_
```cpp
// do asks
auto& asks = it->second.asks;
std::string checksum_string = "";
int i{};
for (auto level_it = asks.begin(); level_it != asks.end(); ++level_it) {
    auto& level_vector = level_it->second;
    for (const auto& order : level_vector) {
        // leave the parsing in here so that validate_orderbook could be something thats called separately not in the hot path
        std::string order_string = generate_order_string(order.price_str, order.qty_str);
        checksum_string += order_string;
    }
    
    // break after max of 10 levels
    ++i;
    if (i >= 10) { break; }
}

// do bids
auto& bids = it->second.bids;
i = 0;
for (auto level_it = bids.begin(); level_it != bids.end(); ++level_it) {
    auto& level_vector = level_it->second;
    for (const auto& order : level_vector) {
        std::string order_string = generate_order_string(order.price_str, order.qty_str);
        checksum_string += order_string;
    }
    
    // break after max of 10 levels
    ++i;
    if (i >= 10) { break; }
}
```

_good version_


## SRP (single responsibiltiy principle)
- states that a class / module should have only 1 reason to change
- misconception: only do 1 thing
    * it can do multiple things just it should change only due to 1 reason

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
# Memory regions & transaltion units

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

_class_
## member functions vs normal functions
- normal functions have to be declared inline for compiler to follow ODR
- member functions are implicitly inline
    * inline is used to ensure function is defined once between multiple TUs
    * pragma once is used to ensure header is only included once, hence only 1 defn
    => 1 definition ALWAYS program-wise

## others
- member variable - not applicable (1 copy per obj)
- virtual member function - implicitly inline
- static member function - implicitly inline
- `static constexpr` member variable
    - pre c++17: `int MyClass::counter = 0; // Separate definition required`
    - c++17 onwards: implicitly inline
- `static` member variable - NOT inline; provide 1 defn in a separate .cpp file
    - if not, every TU (.cpp) that includes this header, will have this definition
    1. old way: write definition in separate .cpp file `int MyClass::counter = 0; // Separate definition required`
    2. modern way: use `inline static int var_name = 0;`


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
