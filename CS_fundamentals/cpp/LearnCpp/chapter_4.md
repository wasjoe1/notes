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

## chp 4.6: fixed-width ints & `size_t`

## chp 4.7: intro to scientific notation
## chp 4.8: floating point numbers
## chp 4.9: boolean values
## chp 4.10: if statements
## chp 4.11: chars
## chp 4.12: type conversion & static_cast