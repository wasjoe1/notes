# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------

TODO
- code
DOING

DONE
- read book to understsand structure + content & create plan for execution
- create simple readme
- download latest version of book (.zip file) for offline reference
- download cppreference.com archive for offline reference

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
# linear interpolation

- also called LERP - linear interpolation
    - technique commonly used in computer graphics, game dev, & animation to smoothly transition between 2 values
- the process of calculating new data points within the range of a discrete set of known data points (ur start & end values)

=> basically draw a line between the 2 values & use discrete values in the range as values

# -------------------------------------------------------------------------------------------------
# type promotion

less precise type is promoted to more precise type

- 1- 0.5 = 0.5 // double is returned
    - due to *type promotion* rule
    - when performing math on 2 different types, cpp promotes the smaller type to match the larger more precise type

* cpp is still strong & static type
    - __strong__ => wont let u add string to an int
    - static => variables are typed & holds a value of that type (dynamic is like python where x = __ can be any type)
             => variable types are determined & checked at compile time
             => once a variable is declared as a specific type, it remains that for its entire lifetime (unless casted?)
* type promotion is just implicit conversion
    - compiler implicitly converts type of a value during calculation

* argument:
    - some people describe cpp as a statically typed language with some weakly typed charactersitics

# -------------------------------------------------------------------------------------------------
# viewport & pixel grid

- pixel grid will be inset from teh viewport edges by half the px-to-px distance
    * inset means to shift inwards
    * now we see that the center of the px is marked
- viewport is then evenly divided into width & height identical regions

pixel grid for 7x 5 resolution image
vector Vu
vector Vv   => viewport vectors
delta u
delta v     => pixel delta vectors

* pixel delta - is the amount of viewport units per px ("step size")
* camera center - initialized to (0,0,0)

# -------------------------------------------------------------------------------------------------
# Camera center

- all scene rays originate from
- camera center aka eye point
- vector V, from the camera center to the viewport center, will be orthogonal to the viewport
    * this is a simplified scenario => typically ur camera center is almost never locked to the center of the viewport


# -------------------------------------------------------------------------------------------------
# rendered image setup (image & viewport: height & width)

```cpp
auto aspect_ratio = 16.0 / 9.0;
int image_width = 400;

// image height
int image_height = int(image_width / aspect_ratio)
image_height = image_height > 1 ? image_height : 1; // image_height if image_height > 1 else 1

// viewport
auto viewport_height = 2.0; // some arbitrary value (range is -1.0 to 1.0) // would return double or float
// auto viewport_width = int(viewport_height * (image_width / image_height)); attempt: BAD example!!
    // 1. casting int for viewport will cause image distortion
    // 2. image_width / image_height => int division, so all the decimals will be lost; we want to cast to double to ensure precision is not lost
auto viewport_width = viewport_height * (double(image_width) / image_height);
```

- notice that image height & width has to be *int*, while viewport can be *double*
    why?
    * pixels (image) are atoms of image file => cant have 400.5 px => need to be whole numbers
    * viewport represents physical window. distances are continuous & window can be 3.555... units
    => thus each ray (the number of px) will be shot & represent an X amount of units of the viewport
- aspect ratio not used for viewport?
    - aspect ratio is ideal ratio
    - but in reality, we only can have whole numbers for px

## ternary operator
condition ? value_if_true : value_if_false

# -------------------------------------------------------------------------------------------------
# const function & return const reference

## Common pattern 1 (return const &__)

- function returns `const &__` so that no expensive copy operation is done

```cpp
// this part => const point3&
const point3& origin() const { return orig; }
```

## Common pattern 2 (const function)

- method doesnt change the member variables of the class

```cpp
// this part => ... origin() const { ...
const point3& origin() const { return orig; }
```

# -------------------------------------------------------------------------------------------------
# formatting class (public, protected, private)

- according to the google cpp style guide, it reccomends:
public first
protected second
private last

* public first shows what ur class can do vs private 1st was used in older C-style code bases
    emphasising the building blocks 

# -------------------------------------------------------------------------------------------------
# type alias

`using point3 = vec3` // vec3 is an existing class

- tells the compiler point3 is another name for the vec3 class

# -------------------------------------------------------------------------------------------------
# formatting member initializer lists
```cpp
// K&R style (braces on the same line)
OrderBookLevelInfos(const LevelInfos& asks, const LevelInfos& bids)
    : bids_(bids), asks_(asks) { // (1)
    // test (2)
    some_function();
}

// Allman style (braces on new line)
ray(const point3& origin, const vec3& direction) 
    : orig(origin), 
      dir(direction) 
{
    // Body is usually empty for a simple ray
}
```

- logic (fn & loops): use ALlman to keep t
hm so its okay to mix the allman style for general curly braces like in function declarations & loops, but then can switch to K&R style for member initializer lists?

# -------------------------------------------------------------------------------------------------
# TU(translation unit): class & function definition

## multiple class defns across TUs
- class defn; type definition => compiler __doesnt generate any actual machine instructions__
- function defn: executable code => contains __binary instructions__ to be executed

* unlike function defn, class defn can the same class defn in multiple TUs
    => THUS its fine to define class in header, even though multiple TUs will then define it
    => its however not okay to define the same class, multiple times in 1 TU

## 1 class degn in 1 TU
HOWEVER, cpp forbids multiple same class defn in the SAME translation unit
    so, multiple TUs can share same class defn
    BUT, 1 TU can only have 1 of that class defn

## Rational?
- (imo) within 1 TU, compiler can check for same class definition
    => compiler builds a symbol table, & can look up for the definition => when sees the same name twice, __Redefinition error__
    => hence it will prevent 1 TU from having the same class && function defns
- BUT across multiple TUs, class is just a type & is not "seenable" in binary instructions
    => class definitions are just metadata & as long as linker sees that they are identical, its fine
    => hence cant tell that multiple definitions occured & is fine?

# -------------------------------------------------------------------------------------------------
# namespace, object, class & methods

std::cout vs ray::at(t)

std - namespace => prevents name collision
cout - object
:: - scope resolution operator => used to look inside a namespace OR class
. - dot operator => used to access a method or property of a specific object
i.e. `std::cout.precision(2)` => take the cout object & call its precision method

namespace vs library
- single library can have many namespaces
- many libraries can shre 1 namespace

* its not a 1-1 r/s between namespaces & libraries
* std lib puts almost everything in std

## dot(.) vs scope resolution(::)
* :: when used with class - usually for static methods
    __static method__
    - if `at()` was a __static method__ (no need specific origin), u can use `ray::at(t)`

    NOT __static method__ (member function)
    - still works as long as there is at least 1 instance of ray
    - needs orig & dir of a *specific ray*; `ray::at(t)` will cause compiler error if no instance of ray created => compiler doesnt know which ray's origin to use

* static members = class variables
- vairable marked as static => means there is only 1 copy of that variable in the netire program

```cpp
class ray {
public:
    static int ray_conut; // Class variable (shared by all rays)
    point3 orig           // object variable (unique to each ray)
}

// to access class variable, use :: => can also use . but its bad practice
    // :: cam be called even if 0 ray objects created
    // . requires at least 1 object sitting in MEM to access
// to access member variable, use .
```

# -------------------------------------------------------------------------------------------------
# translation unit

a translation unit:
- result of taking 1 src file & running it through the __preprocess__
- includes OG .cpp file, contents of all header files included by it (.h, .hpp), & any other src files (.cpp or .c)

* generally, each .cpp file is compiled into a translation unit BUT not always the case

## Unity build (Single compilation unit)
- technique where a master .cpp file simply `#include`s other cpp files
- preprocessor does blind copy-paste of any included file, the compiler sees everything as 1 block of code

* faster full compiles => avoids overhead of parsing the same large headers
* better optimization => compiler can see all code at once

## why ifndef/ pragma once still has double definition
- when 2 .cpp files are compiled separatedly,
    they are compiled as separate TUs
- separate TUs
    => have their own header files compiled in together
    => if 2 TUs have same function defn, double defn error!

SOLN:
- place defintion in separate .cpp file, & only declaration in .h file
- this means the actual definition code is only compiled once inside the .cpp file
    & the linker will see many files asking for that definition & finds exactly 1 place where that fn lives in
- no double defn error!

# -------------------------------------------------------------------------------------------------
# double vs floats

- in our example, we use double => but some ray tracers use float
- precision
    - float: single precision, about 7 decimal digits
    - double: double precision, about 15 to 17 decimal digits
    * tiny rounding errors can accumulate as light bounces around leading to speckles in final image => hence most stick to double (more precise)
- space (MEM)
    - float: 4 bytes (1 sign bit, 8 exponent bits, 23 mantissa/ significant bits)
    - double: 8 bytes ()

# -------------------------------------------------------------------------------------------------
# references

## Subscript return reference?
QN: in genereal does subscript return a reference to the memory of an array?

i.e.
```cpp
int[] a = {1,2,3,4,5};
int& b = a[1];
b = 10;
std::cout << a[1]; // should print 10? Yes!
```

(yes this is correct understanding)

## reference by dereferencing pointer?
can I return the reference to a value by dereferencing its pointer? Yes

i.e.
```cpp
int a = 1;
int* ptr = &a;
int& ref = *ptr
```

- when dereferencing the ptr, u get back actual "container" of the value
- assign the container to a reference(alias)
- __NOTE__: actually pointers return a reference

i.e.
```cpp
*ptr = 10;
int new_var = *ptr; // returns a reference, but new_var is an int, so value is copied over
new_var = 20;
std::cout << *ptr; // still prints 10
```

# -------------------------------------------------------------------------------------------------
# Directives

2 main types:
1. preprocessor directives => anything that starts with `#`; runs b4 compilation
2. compiler directive => `using`; runs during compilation

## directive definition
directive is an instruction given to the compiler OR preprocessor to perform specifc instructions b4 the actual compilation of the code begins

## ifndef
`ifndef` - stands for "if not defined" => checks if the name already exists in MEM, else redefines
    * start of a Header Guard
    * prevents including multiple variable declaration twice

## define

```cpp
#define VEC3_H // defines a Macro

// not a variable => has no val
// not a type => cant create VEC3_H x;
// simply a flag/ marker

// other ways to use Macros
#define PI 3.14159
#define IMAGE_WIDTH 256
```

- macros are not created in MEM
- they are text-substitution rules => during preprocessing, preprocessor just subs all the code with the value

## Include header once

older methods:

```cpp
#ifndef MARKER
#define MARKER
// ... some other header code
#endif
```

current (new) method:

```cpp
#pragma once

// does the same thing => prevents multiple includes, but cleaner
```

# -------------------------------------------------------------------------------------------------
# logging & String formatting
## logging
std::cin // stdin, fd=0 => buffered
std::cout // stdout, fd=1 => buffered
std::cerr // stderr, fd=2 => not buffered
std::clog // logging, fd=2 (shares the same fd as err) => buffered

* note that std::cer has 2 special property `unitbuf` && `tie()` flushes
    => `unitbuf`: means after every output operation, it auto calls a flush on its own data(but may not flush `std::clog`'s buffer even tho they share the same fd)
    => `tie()`: its tied to `std::cout`, so calling std::cerr will auto flush std::cout 1st to ensure error msg appears in the correct chronological order relatve to stdout!

* by default both FD1 (output) & FD 2(stderr/clog) are connected to the terminal
    - redirect helps to only display log/ error outputs, & not the data outputs

* carriage return (\r) only moves to the beginning of the current line where the cursor is at (currently)
    - IF std::cout not redirected:
        - \n is used at every ouput line
        - when \r is called for the std::clog line, it will just go to the start of the \n and print (doesnt overwrite any RGB values)
    - IF std::cout IS redirected
        - \r is called on the 1st line at the bottom of the screen (on the terminal)
        - when each line is updated, it will overwrite the current line => "stay in-place" countdown!!

## string format
* \r - carriage return => moves cursor to the left (type is at the start of the lin)
    => used to update the line rather than include a new line
* \n - line feed => on terminal: moves paper up 1 line, on document: appends 1 line to doc

* ghost character
- when printing lines (specifically a progrss bar), `\r` is used & it overwrites the current characters in-place
- extra characters from the previous output might be there & not overwritten as new output is shorter than the old output
    i.e.
    1. print "Scanlines remaining: 100" => 24 characters
    2. print "\rScanlines remaining: 99" => 23 characters
    3. result: "Scanlines remaining: 990" => ghost character '0'
    
    * thus we use ' ' at the end before flush `std::clog << some_words << ' ' << std::flush;`
    * ' ' is used as its 1 byte vs " " which occupies 2 bytes (space characer + end character(`\0`) since its a string literal)
    * in some cases, we use an entire length of 
- rolling eraser
    => context: from 255 to 1
    => qns: how come it can erase 2  digits?
    - from 100 to 99: it erases the 1st 0
    - from 10 to 9: it erases the next 0
    * hence it erases because the value is decremented by 1 each time

# -------------------------------------------------------------------------------------------------
# Building & running project

- CMakeLists.txt                            => the thing that cmake (build files generator) reads => focuses on permanent stuff (files in proj, version of cpp, final program name, libs needed)
- CMakePresets.json                         => presets for building (output folder for finished files, which compiler to use, debug or release mode etc.)
- ~~vcpkg.json~~ [deleted]                  => dependency list
- ~~vcpkg-configuration.json~~ [deleted]    => address of where to get dependency from



# -------------------------------------------------------------------------------------------------
# arithmetic (int & double conversion)

# cast to make (int / int) -> (double / double)

## integer division (int / int)
i.e. `auto r = j / (image_width - 1);`
=> j & image_width are both ints
=> r would be an int, where all decimal was thrown away during __integer division__

## double logic trap
i.e. `double r = j / (image_width - 1);`
=> int / int -> means integer division occurs first (if j is 5 && (image_width - 1) is 10, r will be 0)
=> 0 is assigned to r
=> r is casted to double (from 0 to 0.0)

* right side evaluated first

## integer division (double / double)
i.e. `auto r = double(j) / (image_width - 1);`
=> j is now casted to a double
=> computer treats the whole division as double / double (__floating-point division__)

## re-assignment (value truncation)
i.e.
int a = 5.0 / 2     # floating point division == 2.5
                    # value is truncated since a is int
double b = a;       # a is assigned to b (2 -> 2.0)

* any decimal info is permanently deleted when stored in an int variable

# -------------------------------------------------------------------------------------------------
# Operator overload

there are 2 ways to overload operators. 1 is global operator overload, 2nd is member operator overload

## global operator overload

```cpp
struct Vec3 {
    double x, y,z;
}

// global operator overload
std::ostream& operator<<(std::ostream& os, Vec3 v) {
    os << "Vec3(" << v.x << v.y << v.z << ")";
    return os; // return the same ostream to allow for chaining
}

// usage
Vec3 vector{1.0, 2.0, 3.0};
std::cout << vector << std::endl; // outputs Vec3(1,2,3)
```

## member operator overload

```cpp
struct Vec3 {
    double x, y, z;

    // member operator overload
    Vec3 operator+(Vec3& const other) const { // pass in constant reference (since read-only; no change) && const member function => does not change the object it belongs to
        // can either call this->y or just y is fine
        return Vec3(x+other.x, y+other.y, z+other.z);
    }
    // notice that we are returning a new Vec3 & its because +/ - math ops are not suppose to change the original vector; only if u do += or -=, then its a change & assignment op
}
```

Usage in Cling:
Vec3 a{1, 1, 1}, b{2, 2, 2};
Vec3 c = a + b; // Calls a.operator+(b)

## prioritization of operator overload

- compiler always respects std math operator precendence
- this still holds after u overload the operators => i.e. u overload `+` and `*`. when using them together, `*` is still executed first over `+`

i.e. `orig + t * dir` => (t * dir) executed first, then the + operator

# -------------------------------------------------------------------------------------------------
# Cpp REPL (Cling)

if you type expression without `;`, REPL tries to be helpful & prints type + MEM address of wtv that expression returns
i.e.
#include<iostream>
std::cout << "hello" # actually returns a reference to the cout

# -------------------------------------------------------------------------------------------------
# Low level thinking
1 byte = 8 bits
4 bytes = 32 bits
8 bytes = 64 bits

* x86 refers to 32 bits system, x64 (x86-64) refers to 64 bit architecture/systems

base-n (aka radix system)
- specific type of positional numeral representation
    - `numeral representaion` - broad term for any way of writing number systems
    - `positional` - the positions of its digit determines its value based on powers of a fixed number `n`
    i.e. 1000 in base-2 means 2^3 = 8
=> hexadeciaml is base-16
=> decimal is base-10

little endian
- system of byte ordering used in computer MEM
- stores least significant byte, of a multi-byte number, at the lowest memory
    i.e. number in dexadecimal is: 0x12345678
    in MEM: 78 56 34 12
    human like: 12 34 56 78
    * note that the arrangement of the bytes are reversed but the actual byte itself is not

* each hexadecimal is 4 bits
2 hexdecimal digits = 1 byte
4 bytes = 8 hexdecimal digits = 32 bits

* 4 bytes/ 8 bytes are most common word sizes
* an int is (typically) 4 bytes
    2^32 = ~4.2 bil different numbers
* MEM address is just a number, also typically 4 bytes(on x86, else 8 bytes)
    means roughly 4GB of addresses that can be pointed to

__char encoding__
- string encoding formats: ASCII, UTF-8, UTF-16 etc.
- encoding just maps specific numbers to character && dictates how many bytes store those numbers
    - i.e. ASCII has values 0-127 & uses 1 byte (8bits)
    - UTF-16 has more values to represent more characters & uses 2 bytes
how does this relate to cpp char types?
- normal `char` type does auto align with every encoding => traditionally char is 1 byte (8 bits)
    => maps perfectly to ASCI
    => too small to hold UTF-16

* `char` => ASCII or UTF-8 (1 byte)
* `char16_t` => designed specifically for utf-16 (2 bytes)
* `char32_t` => utf-32 (every character guaranteed to fit exactly into 4 bytes)
* `wchar_t` => "wide character" size depends on operating system (2 bytes on windows, 4 bytes on linux for utf-32)

* `_t` suffix - generally is used when the actual size of the type varies on different systems (`size_t` or `time_t`)

# -------------------------------------------------------------------------------------------------
# building & running project
1. go to the root of the project [here]() & run this
cmake -B build

# -------------------------------------------------------------------------------------------------
# chapter list
1. overview [chapter 1](../chapters/1_overview.md)
2. output image [chapter 2](../chapters/2_output_image.md)
    => PPM format (to see the image)
    => create this file
    => progress => to see progress of program & if it stalled
3. vec3 class => to hold coordinates; in many systesms is 4D (3D + homogenous coordinate OR RGB + transparency component)
    * homogenous coordinates: n-dimension geometry using n+1 numbers (i.e. (x, y, z, w))
    * last 
    * projective geometry - branch of 
4. rays, camera, BG
5. add sphere

6. surface normals & multiple objects      => seems like hard part of 3D projection programming

7. abstracting camera class
8. antialiasing?

9. Diffuse materials?
10. metals?
11. Dielectrics?
12. positionable camera
13. defocus blur

14. Final render

# -------------------------------------------------------------------------------------------------
# ray tracing basics

## definitions
cartesian coordinates - ((x,y) or (x,y,z)) points in 2D or 3D space
cartesian equations - algebraic expression relating these variables (i.e. y = mx + c)
homogeneous coordinates (projective coordinates) - n-dimension coordinates represented by n + 1 values; (n+1)th value representing weight
    * i.e. in 2D: point (1,2,1) == (2,4,2)
    * to convert homogeneous to cartesian => (x,y,z,w) = (x/w, y/w, z/w)
projective geometry - branch of math studying properties inveraint under projections focusing on incidence (points lying on lines)
    * isnt there angle & length when projecting? Yes, but they arent projective since they change depending on perspective
        => hence, we are interested in the invariant parts that survive this transformations!
ray tracer - rendering system that calculates an image by athematically simulating the path of light as it interacts with virtual objects

## cartesian vs homogeneous coords
cartesian:
- dimensions: n val for n-D space
- representation: each point has unique representation (i.e. (x,y) or (x,y,z))
- translation: via additiion (P + T)
- infinity: NIL
- perspective: NIL (hard to calc depth)

Homogeneous:
- dimensions: n+1 val for n-D space
- representation: 1 point has inf representations (i.e. (1,1,1) == (5,5,5))
- translation: via matrix multiplication (M . P)
- infinity: set w = 0
- perspective: naturally handles perspective projection & shadows

* homogeneous advantage: allows "unified" transformations (combine multiple steps into 1)
=> in cartesian math, translation requires a different formula than rotation (multi steps)
=> in homogenous space, can combine translation, rotation & scaling into single matrix allowing GPU to calc all in 1 step
* other advantages include HW alignment (SIMD), MEM alignment(16 bytes chunks)