# CONST
Understanding const in cpp can be confusing (it sure was for me)
and i think the better approach to learning it, is to understand when we use it
(semantics behind const)

# 1. Basic concept
# 2. protect DATA
# 3. protect POINTER
# 4. protect BOTH
# 5. const in pointer vs reference
# 6. class member function

# -------------------------------------------------------------------------------------------------
# Basic concept
`Const is applied to the thing immediately ot its left (or right if left is empty)`

i.e. `int const* ptr` & `const int* ptr` for both, const points to int
vs   `int* const ptr` const points to *

# -------------------------------------------------------------------------------------------------
# protect DATA

* `int const* ptr` & `const int* ptr` for both, const points to int

    - `const int* ptr` this is the more common way written (google style mentions this, most codebases use this as well)
    - `int const* ptr` i prefer this becoz it helps to align everything with "const points to thing on left" concept

-> const points to int (type)
-> __VALUE__ in the address (that the pointer points to) __CANNOT__ be modified via the ptr
-> __CAN__ change ptr __ADDRESS__

i.e.
```cpp
const int* ptr = &a;
ptr = &b    // yes
~~*ptr = 30;  // NO~~
```

# -------------------------------------------------------------------------------------------------
# protect POINTER

* int* const ptr;

-> const points to pointer(*)
-> __CAN__ change __VALUE__ via ptr
-> __CANNOT__ change ptr'a __ADDRESS__

i.e.
```cpp
int* const ptr;

*ptr = 30; // yes
ptr = &ptrb // NO
```

# -------------------------------------------------------------------------------------------------
# protect BOTH

* const int* const ptr;

-> const points to both val & pointer
-> __VALUE__ & __ADDRESS__ __CANNOT__ change

i.e.
```cpp
int* const ptr;

*ptr = 30; // NO
ptr = &ptrb // NO
```

# -------------------------------------------------------------------------------------------------
# const in pointer vs reference

genreal concept:
* data const-ness must be preserved
* pointer const-ness can disappear in copies

# -----------------------------------------------
## for pointers
SO,
```cpp
int* const ptra;
int* ptrb = ptra; // yes => address is just copied over to this ptrb
    // ptr's address is given to ptrb by copy
    // ptrb receives copy of the address
    // not actually const, since u can change the val inside the address, & the ptrb can point to any other address as well
```

BUT,
```cpp
const int* ptra;
int* ptrb = ptra; // NO => compilation error need `const int* ptrb` to handle a const value in the address
```

# -----------------------------------------------
## for references
* `const int& x`
    * `int& const x` is illegal since references are implicitly const already (once its bounded, it cant be reseated/ reassigned to another variable)
- const points to valu
-> __CANNOT__ change __VALUE__ via ref

# -----------------------------------------------
## pointer vs reference

* `const int&` vs `const int*`
    - `const int&`
        -> returns ref to const int
        -> CANNOT modify through ref
        -> __guaranteed__ to exist
    - `const int*`
        -> returns ptr to const int
        -> CANNOT modify through ptr
        -> __NOT guaranteed__ to exist

# -------------------------------------------------------------------------------------------------
# class member function

`const int& some_func(...) const {...}`

* 1st const => follows the rule of ref const
    (no further explanation, refer to above lol)

* 2nd const
    -> means fn is a const member fn
    -> internally, compiler sees it as `const ClassName* this` => so u cant change inherent values inside ClassName

- 1. cant change member variables
- 2. cant call non-const methods

i.e.
```cpp
class A {
public:
    int x;
    int getX() const {
        return x; // allowed
    }

    void bad() const {
        x = 5; // NOT allowed
    }
};

// 1. allow u to get val without changing internal state of obj
const int& x = o.getvalue()
x = 5; // NOT allowed

// 1.1 compilation of const val
const int& x = o.getvalue() // allowed
int& x = o.getvalue() // NOT allowed => strict typing

// 2. allow u to call const methods
const A obj;
obj.getX(); // allowed
obj.bad(); // NOT allowed
```

# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------
I think understanding const using practical exampels help us see why we need/ use it!
this is my understanding so far & hopefully nothing else confusing comes my way...
