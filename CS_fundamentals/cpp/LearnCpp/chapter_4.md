# chapter 4: fundamental data types

## chp 4.1: intro

(recap)
- objects & `variables` - variables are names for a piece of MEM that can store info
- RAM is MEM available for programs to use; when a variable is defined, a piece of that MEM is set aside for that variable
- `bit` / binary digit - smallest uni of MEM, holds value of 0 or 1
- MEM is organized into sequential units called `MEM addresses`
- `each MEM address` holds `1 byte` of data
    * each bit does not get its own unique MEM address becoz, addresses is limited & the need to access data bit-by-bit is rare
    - each MEM address holds 1 bytes of data instead
- `byte` - group of bits that are operated on as a unit; modern standard byte is comprised of 8 sequential bits

### data types

since all data on a computer is just a sequence of bits,
- we use _data types_ to tell the compiler how to interpret the contents of the MEM in a meaningful way
- compiler & CPU encodes the value (value given to an object) into the appropriate sequence of bits for that type & stored in MEM
    - i.e. value `65` is converted to the sequence of btis `0100 0001` & sotred in the MEM assigned to the obj

### fundamental data types

| TYPEs                   CATEGORY                MEANING
|-----------------------------------------------------------------------------------
| float                   floating point          number with fractional part
| double
| long double
| 
| bool                    integral (boolean)      true / false
| 
| char                    integral (character)    single character of text
| wchar_t
| char8_t (c++20)
| char16_t (c++11)
| char32_t (c++11)
| 
| short int               integral (integer)      +ve & -ve whole numbers, include 0
| int
| long int
| long long int (c++11)
| 
| std::nullptr_t(c++11)   Null pointer            null pointer
| 
| void                    void                    no type

* this chapter explore these fundamental types in detail except std::nullptr_t which is discussed with pointers

### integer vs integral

- in math, "integer" is a number with no decimal / fractional part, including -ve, +ve & 0
- in c++, "integral" means "like an integer" => has other meanings in other context but we'll use this definition

c++ standards define:
- _standard integer types_ are: `short`, `int`, `long`, `long long` (including signed & unsigned variants)
- _integral types_ are: `bool`, various char types, & _stand integer types_
    * all std int types are integral types, but not vice versa

- all integral types are stored in MEM as integer values
- but only standard integer types will display as integer values when output
- C++ std explicitly notes that "integer types" is synonym for "integral types" BUT conventionaly
    used as "standard integer types" as shorthand
- note that "integral types" only include fundamental types
    - non-fundamental types like `enum` & `enum class` are not integral types (even when they are stored as an integer)

### other sets of types (3 sets)

c++ contains 3 sets of types:
1. "fundamental data types" - provide most basic & essential data types
2. "compound data types" provide complex data types, allowing for the creation of custome (user-defined) types
    * 1st 2 sets are built-in to the language itself (dont required inclusion of headers)
3. 3rd type
    - provided by the c++ std lib, which is included in all c++ distributions, & are hence broadly available & standardized for compatibility
    - use of types in std lib requires inclusion of appropriate header & linking in the std lib
    - largest set of types 

* note: the term "built-in" type is often a synonum for fundamental data types
    but, stroustrup (& others) use the term to mean both fundamental & compound data types (both built-in to the core language)
    since this term isnt well-defined, its reccomended to avoid
* type to handle string? (sequence of characters that is typically used to represent text)
    => will be introduced in next chapters

### _t suffix

- suffix means "type"
- its common nomenclature applied to modern types
- if something has _t suffix, its probably a type; but many types dont have _t suffix


## chp 4.2: void

- means no type
- an example of _incomplete type_
    _incomplete type_
    - compiler knows the existence of such types, but doesnt have enough info to know how much MEM to allocate for objects of that type
    - represents lack of type, & thus cant be defined
    - cant be instantiated
- used to indicate a function doesnt return a value

## chp 4.3: obj `sizes` & `sizeof` operator

### object sizes

- most objs take up more than 1 byte of MEM
    => single obj may use 1, 2, 4... consecutive MEM addresses
- compiler hides the details of how many bytes a given obj uses
- when accessing a variab,e, the compiler knows how many bytes need to be retrieved (based on the type) & will output the appropriate machine language to handle that detail for us
- note: new programmers focus too much on optimizing code to use as little MEM as possible
    BUT this makes a negligible difference
    => should focus on writing maintainable code & optimize when benefit is substantive

### fundamental data type sizes

C++ standard doesnt define the exact size (in bits) of fundamental types
it just says:
- an obj must occupy at least 1 bytes (so that each obj has a distinct MEM address)
- a byte must be at least 8 bits
- the integral types `char`, `short`, `int`, `long` & `long long` must have a min. size of 8, 16, 32, 64-bits respectively
- `char` & `char8_t` are exactly 1 byte (at least 8 bits)

in this tut series, the book makes these assumptions that generally hold true for modern architectures:
- A byte is 8 bits.
- Memory is byte addressable (we can access every byte of memory independently).
- Floating point support is IEEE-754 compliant.
- We are on a 32-bit or 64-bit architecture.

CATEGORY	    TYPE	        MINIMUM SIZE	    TYPICAL SIZE
Boolean	        bool	        1 byte	            1 byte
Character	    char	        1 byte (exactly)	1 byte
                wchar_t	        1 byte	            2 or 4 bytes
                char8_t	        1 byte	            1 byte
                char16_t	    2 bytes	            2 bytes
                char32_t	    4 bytes	            4 bytes
Integral    	short	        2 bytes	            2 bytes
                int	            2 bytes	            4 bytes
                long	        4 bytes	            4 or 8 bytes
                long long	    8 bytes	            8 bytes
Floating point	float	        4 bytes	            4 bytes
                double	        8 bytes	            8 bytes
                long double	    8 bytes	            8, 12, or 16 bytes
Pointer	        std::nullptr_t	4 bytes	            4 or 8 bytes

* for max portability, you shouldnt assume that objects are larger than the min. size
    can use `static_assert` to have the compiler fail a build if it is compiled on an architecture where assumptions arent true
    (how to do this is covered in chp 9.6 -- assert & static_assert)

- my common uses:
    - bool      1 byte      => if its standalone will cost at least 1 byte; but can pack many using std::bitset for fixed-size flag sets
    - char      1 byte
    - int       4 bytes
    - float     4 bytes
    - double    8 bytes
    - pointer   8 bytes     => (x86-64, ARM64 etc.), typically 32 bits on (x86, ARM32)

### sizeof operator

- help to determine size of data types on a particular machine
- unary operator taking in a type or variable & returns the size of an object in bytes
- using `sizeof` on incomplete types will result in compilation error
    - if u havent disabled compiler extensions, gcc allows `sizeof(void)` to return 1 (turn it off according to chp 0.1)
- does not include dynamically allocated MEM used by an object

### fundamental data type performance

- objects of fundamental data types are considered fast & performance of copy ops etc. are generally not a concern
- furthermore,
    assumption: types that use less MEM is faster than those that use more
    actual: not always true, CPUs often optimize to process data of a certain size (i.e. 32 bits), & types have that size may be processed quicker
        thus, on such a machine, a 32-bit int could be faster than a 16-bit short or 8-bit char

## chp 4.4: signed ints

- C++ only guarantees that integers will have minimum size, not a specific size
- integers in c++ are signed by default (number's sign is stored as part of the value)
- singed integer ranges assumes the 2's complement binary representation
- range is from -2^n to 2^n-1
- overflow: evaluation of an expression is not mathematically defined or not in the range of representable values for its type, behavior is undefined
- integer overflow / arithmetic overflow - value is created outside the range that can be represented
    * overflow results in info being lost
- integer division - division with 2 integers, always produces integer results

## chp 4.5: unsigned ints, & why avoid them

- unsinged integers are integers that can only hold non -ve whole numbers
    `unsigned short`, `unsigned int`, `unsigned long`, `unsigned long long`
- range is from 0 to 2^n-1
- oddly, c++ standard says "a computation involving unsigned operands can never overflow"
    this is contrary to general programming consensus that integer overflow encompasses both signed & unsigned cases
    we'll call this overflow despite c++ standard's statements
- during overflow, result is divided by (1 + largest number of type) & remainder is returned (basically modulo of largest number + 1)
    i.e. 280 % 256 (1 byte range) = 24

### why do ppl discourage using them?

- ez to overflow bottom of the range (0) because majority values are near that
- unexpected behaviors can result when mixing signed & unsigned integers
    `signed int s {-1}` when compared with `unsigned int u {1}`, s is implicitly converted to 429... & is thus false `(s < u)` 
    * conversion rules will be covered in chpater 10: both operands of certain binary operations need to be the same type
- accidentally passing the wrong value when using unsigned as paramter type
    `void doSomething(unsigned int x)` then we call `doSomething(-1)` -1 is implicitly converted to 429...

### when should we use them then?

- bit manipulation
- encryption, random number algos etc. => where well-defined wrap-around behavior is required
- array indexing (will touch on this more later)
- embedded systems (arduino etc.) where MEM/processor has limited context & are used for performance reasons

## chp 4.6: fixed-width ints & `size_t` (& `sizeof(...)`)

context:
- int can be min. 16 bytes but most architectures use 32 bits => not safe to assume
- goes back to early C days, performance was utmost concern, compiler implementors can pick size of int that was most efficient
- by modern standards, lack of consistent ranges for various integral types ~~sucks~~ is bad (esply since c++ is designed for portability)

fixed-width ints: ints with fixed size
- defined in <cstdint> header
- introduced in c++11

fixed-width examples:
std::int8_t
std::uint8_t
std::int16_t
std::uint16_t
std::int32_t
std::uint32_t
std::int64_t
std::uint64_t

- u unsigned
- divide by 8 to see how many bytes (8 is 1 byte, 16 is 2 etc.)
- best practice: use fixed-width int type when integral type has fixed range

### `std::int8_t` & `std::unit8_t` (downside 1)

- due to oversight in c++ specification, modern compiler treat these 2 types + corresponding fast & least fixed-width types
    as signed & unsigned char type
- weird exammple: 
    ```cpp
    std::int8_t x{65};
    std::cout << x << '\n'; // doesnt print 65 => discuess what this prints in 4.12 (type conversion & static cast)
    ```
- further explanation:
    - fixed width ints actually dont define new types; they are aliases (for existing types w desired size)
    - the implementation (compiler + std lib) decides which existing type is aliased
    - i.e. on platform where int is 32 bits, int32_t is alias for int
    - i.e. on platform where int is 16 bits & long is 32 bits, int32_t is alias for long instead
- weird example explanation:
    - 8-bit fixed-width types? most cases are aliases for signed char
    - signed char is the only 8-bit signed integral type (bool & char are not considered)
    - hence, in this case, int8_t behaves just like char on that platform
    - if platform has an implementation-specific 8-bit signed integral type, the integral may decide to make int8_t an alias for that type instead
    - may behave more like an int than char
    * uint8_t behves similarly

### other fixed-width downsides (other 2 downsides)

1. fixed-width integers not guaranteed to be defined on all architectures
    - only exist on systems where there exists fundamental inegral types that match their widths + binary representation
    - program fails to compile when architecture dont support that fixed-width integer
    - BUT most modern architectures do support 8/16/32/64-bit variables
2. fixed-width integer may be slower than wider type
    - some architectures are faster at processing 64 bit ints; even tho u might have thought to save space + knowing the range
    - BUT CPU processing a given type faster doesnt mean overall program faster => alot of programs run slow because of the larger MEM usage
    * trade off between _raw processing faster_ vs _MEM footprint_ causing slow down

### resolve downsides: Fast & least integral types

- optional chapter & not typically used anws
- fast types provide the fastest signed/ unsigned integer type with a width of at least # bits (i.e. std::int_fast32_t)
- least types provide the smallest signed/ unsigned integer type with a width of at least # bits
    - i.e.
    std::int_least16_t is 16 bits, but std::int_fast16_t is 32 bits
    => beco 32 bits on author's machine is faster to process than 16 bit ints
    on platform with only 16 bit & 64 bit integral types,
    std::int32_t would not exist, std::least_int32_t would be 64 bits

downsides to these resolution:
- not many devs use => lack of familiarity
- fast types can lead to MEM wastage => might be severe wastage
- worst, becoz size of fast/ least ints is implementation defined, programs may exhibit different behaviors (almost as if its UB)
    on different architectures
    * rather deterministic than non-determinisitc

best practice: avoid these types as they exhibit different behaviors on different architectures

### Best practices for integral types

- avoid fast/ least types => until u need to support an esoteric platform which fixed-width type isnt supported
    , then decide how to migrate & retest at that point
    * better correct than fast
    * better fail at compile time, than runtime

- prefer `int` when size dont matter + range fits within 2 bytes
- prefer int#_t when int has guaranteed range
- prefer uint#_t when doing bit manipulation OR well-defined wrap around behavior

AVOID
- short & long integers type => prefer fixed-width int type
- fast & least integral types
- unsigned types for holding quantities => use signed int type
- 8-bit fixed-width integer types (prefer 16 bit fixed width integer type)
- any compiler specific fixed-width integers

### std::size_t

```cpp
cout << sizeof(int) // prints 4 (author machine)
```

- sizeof returns integer value, but whats the type? `std::size_t`!
    sizeof(...) returns amt of MEM used by the result of the expression
- size_t is a typedef -> covered in 10.7 typedefs & type aliases
- size_t is defined in different headers; <cstddef> is the best as it contains the least number of other defined identifiers
- using size_t explicitly requires including necessary headers
- but using sizeof doesnt require any headers
    - `sizeof` is built-in keyword, return type s a fundamental type (size_t is just defined in the header if u wanna use it)

* while unsigned ints are generally discouraged, MEM can never be -ve, hence we use this for size

### std::size_t imposes upper limit on size of an object (optional)

- sizeof must return byte-size of an obj as a value of type std::size_t
- byte size of obj has to be within size_t largest value
- if not, sizeof will not be able to return that value

## chp 4.7: intro to scientific notation
(math lesson on presenting large numbers in scientific notation)

## chp 4.8: floating point numbers

floating point type variable - variable that can hold a number with a fractional component

- floating point data types are always signed
- types + typical size: float (4 bytes), double (8 bytes), long double (8, 12, 16 bytes)
    `float` is almost always implemented using 4-byte IEEE 754 single-precision format
    `double` is almost always implemented using 8-byte IEEE 754 double-precision format
    * single-precision is precise to 7 digits, double-precision is precise to 15-17 digits
    BUT `long double` varies by platform:
    - 8-byte IEEE 754 double-precision format (same as double)
    - 80 bit (often padded to 12 / 16 bytes) x 87 extended precision format (compatible w IEEE 754)
    - 16 byte IEEE 754 quadruple precision format
    - 16 byte IEEE 754 double-double precision format (not compatible w IEEE 754)
        * double-double means u store 1 number as 2 double numbers, addition result being the number actl stored

### floating point variables & literals

- must include at least 1 decimal place, signals to compiler that number is a floating point number, not int
- floating point literals default to double
- f suffix denotes literal of type float
- best practice: ensure type of literals match the type of variables they're assigned to/ initialized with
    else => unnecessary conversion occurs, potential _loss of precision_
```cpp
int a{5}; // integer
double b{5.0}; // default double
float c{5.0f}; // float
```

### printing floating point numbers

```cpp
cout << 5.0 << '\n';
cout << 6.7f << '\n';
cout << 9876543.21 << '\n';
```

results:
5
6.7
9.87654+06

- cout default to NOT print decimal part if its 0
- 3rd case, it prints in scientific notation

### floating point precision

precision - precision of a floating point type defines # of significant digits it can represent without info loss
    depends on type (float less precise than double)
    & value (some values represented more precise than others)
* floating type can only represent a certain # of significant digits
    using a value with more significant digits than the min. may result in the value being stored inexactly
    * i.e. precise up till 15 digits, but use float variable to store => lost precision
    * or i.e. literal is way bigger, but variable has less precision => wrong precision

### outputting floating point values

- cout has default precision of 6 => assumes all floating point variables are only significant to 6 digits (min. precision of a float)
    * note that cout defaults to outputting #s in scientific notation in some cases
```cpp
cout << 9.87654321 << '\n';
cout << 987.654321f << '\n';
cout << 987654.321f << '\n';
cout << 9876543.21f << '\n';
cout << 0.0000987654321f << '\n';
```
returns:
9.87654
987.654
987654
9.87654e+006
9.87654e-005

- override default precision of std::cout using `output manipulator` w fn named `std::setprecision()`
    * output manipulators alter how data is output, & defined in iomanip header
```cpp
cout << std::setprecision(17); // shows 17 digit of precision
cout << 3.333333333333333333333333333333333333333333333333f << '\n'; // f suffix: float
cout << 3.333333333333333333333333333333333333333333333333 << '\n';
```
returns:
3.3333332538604736  <= can see that precision doesnt hold
3.3333333333333335  <= precision doesnt hold

* precision set to 17 digits, each num is printed with 17 digits, but nums arent precise to 17 digits
    floats less precise than doubles, hence float has more errors

### rouding error

- precision error - when precision is lost becoz number cant be stored precisely
- doesnt only impact fractional numbers
    `cout << std::setprecision(9);` to show 9 digits + cout << 123456789.0f
    results: 123456792  <= only precise up till the 6th digit, some precision was lost!
- best practice: use double over float, unless space is at a premium => float often leads to inaccuracies

### rounding errors make floating point comparisons tricky

- floating point numbers are tricky to work with
- non-obvious differences between binary & decimal nums
    in decimal, 1/10 is represented as 0.1, in decimal is infinite sequence 0.0001100110011...
    i.e.
    double d{0.1};
    cout << d << '\n';
    cout << std::setprecision(17);
    cout << d << '\n;
    
    returns:
    0.1
    0.10000000000000001     <= see that d is not exactly 0.1
    
    double d2{0.1 + 0.1 ... + 0.1}; // should equal 1.0
    cout << d2;
    
    returns:
    0.99999999999...

    * rounding errors may make number slightly larger or smaller
    * be wary when using floating point numbers for financial or currency data

### NaN & Inf

Inf - infinity, is signed, can be -ve(-inf) or +ve(+inf)
NaN - not a number
signed 0 - there are separate representations for +0.0 & -0.0

```cpp
double zero{0.0};
double posinf{5.0 / zero} // +ve inf
double neginf{-5.0 / zero} // -ve inf
double z1 {0.0 / posinf} // +ve 0
double z2 {-0.0 / posinf} // -ve 0
double nan {zero / zero}; // nan
```

prints:
inf
-inf
0
-0
nan

## chp 4.9: boolean values

- bool variables only have 2 values: true & false
- logical NOT(!) operator can be used to flip boolean val
- printing Boolean values:
    0 cout prints `0` for false & `1` for true
    using `std::boolalpha` to output bool values:
    `cout << std::boolalpha;`
    `cout << true << '\n';` // returns true instead of 1
    `cout << false << '\n';` // returns false instead of 0
- int to boolean conversion
    - using uniform initialization: only 0 & 1 allowed
        `bool False{0};` // okay
        `bool True{1};` // okay
        `bool No{2};` // error: narrowing conversions
    - other contexts (typically copy initialization):
        0 is false, other values i true
        bool b1 = 4; // copy init, implicit conversion from int to bool
        bool b2 = 0; // copy init, implicit conversion from int to bool
- inputting bool vals
    - normal cin: cant accept "true" or "false"
    - `std::boolalpha`: `cin >> std::boolalpha` + `cin >> b`
        * only accepts lower-cased false OR true
        doesnt accept capital letters or other int values


## chp 4.10: if statements
- if, if-else, if-else if-else
- early return - cause the fn to return when return statement is executed (b4 the fn would otherwise return)

## chp 4.11: chars


## chp 4.12: type conversion & static_cast

- type conversion - converting data from 1 type to another
- _implicit_ type conversion - compiler does type conversion on our behalf without explicitly asking
    => doesNT modify current value/ obj; produces _temporary object_
    => conversion process uses data as input & produces converted result
    => copy elision occurs for initialization, but temp obj is created for any other case
- _brace initialization_ ensures implicit type conversions dont happen & throws error when we initialize a variable with an initializer that will lose value when implicitly type converted
- _explicit type conversion_ - allows programmer to explicitly tell compiler to convert a value from 1 type to another; if conversion results in loss of val, compiler will NOT warn us
    (chp 10.6 will go further into explicit type conversion & static_cast)
- static_cast to convert char to int
    char ch{97}
    cout << ch; // prints 'a'
    cout << static_cast<int>(ch) // prints 97
- static cast to convert signed to unsigned integral values & vice versa
    - if val being converted can be represented in dest type, converted val remains unchanged
    - if val being converted canNOT be represented in dest type,
        - if dest type is unsigned, val will be modulo wrapped
            i.e. `static_cast<unsigned int>(-1)` is wrapped to largest num `4294967295`
        - if dest type is signed, val is implementation-defined prior to c++20, & will be modulo wrapped as of c++20
            i.e. `static_cast<int>(4294967295)` is wrapped to `-1` because all 1s in 2s complement is -1
- `std::int8_t` & `std::uint8_t` behaving like chars
    1. `std::int8_t myInt{65}` might think it prints 65, but actl prints `A`
        BUT, can convert val to int via static_cast `static_cast<int>(myInt)` returns 65 (the returned val now takes 4 bytes instead of 1 byte)
    2. `cin >> myInt` where myInt is of type `std::int8_t` is bad
        i.e. input 35, but int8_t is treated as char, so '3' & '5' is treated as separate chars
        char obj can only hold 1 character, so '3' is extracted while '5' is left in the input stream
        '3' has ASCII code point 51,  so `static_cast<int>(myInt)` will return `51` instead
        COZ its casting a char to int basically
