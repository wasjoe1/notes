# chapter 12: 

## chp 12.1: 
## chp 12.2: value categories (lvalues & rvalues)

- lvalue references -> 1st compound type
- expression (from chp 1.1) - combination of literals, variables, operators & function calls executed to produce a singular value (i.e. 2 + 3;)
    - can have side effects (i.e. ++x lhas side-effect of incrementing x)
    - can also, *evaluate to objects or functions*

### properties of an expression
- to determine how expressions should evaluate & where they can be used,
    all expressions in c++ have 2 properties:
    1. type
    2. value category

_type_
- compiler uses the type of an expression to determine whether an expression is valid in a given context
- i.e.
    compiler determines (at compile time) that a division with a double operand & an int operand, produces a double result
    * arithmetic operators must have operands of matching types
    so, the int operand getes converted to a double
    &, a floating point division is performed
    hence, double is the type of this expression
- note: the type of expression must be determinable at compile time (else type checking & type deduction wouldnt work)
    BUT, the value of an expression may be determined at compile time (constexpr) or runtime (not constexpr)

_value category_
- value category of an expression (or subexpression) indicates whether an expression resolves to a _value_, _function_, or _object_ of some kind
- prior to c++11, there was only 2 value categories: _lvalue_ & _rvalue_                        <= cover these 2 first
- in c++11 & after, 3 additional value categories were added: _glvalue_, _prvalue_, _xvalue_


### lvalue & rvalue
_lvalue_
- lvalue - an expression that evaluates to an _identifiable object or function_ (or bit-field)
- the term "identity" used by the C++ standard is not well-defined (below tries to elaborate on what identity is)
    - an entity (such as an object or function) that has an identity can be differentiated from other similar entieis (typically by comparing the addresses of the entity)
    - entities with identities can be accessed via an identifier, reference, or pointer & typically have a lifetime lonfer than a _single expression or statement_
    * so, lvalue is an entity with identity; identifiable entity;
    i.e.
    ```cpp
    int x {5};
    int y {x}; // x is an lvalue expression; evaluates to variable x (has an identifier)
    ```
- modifiable lvalue - lvalue whose value can be modified
- non-modifiable lvalue - lvalue whose value cant be modified (because its const or constexpr)

_rvalue_
- is an expression that is not an lvalue
- r value expressions evaluate to a _value_
    - include literals (except C-style string literals, which are lvalues), return value of functions & operators that return by value
- rvalues _arent identifiable_ & only exist within the scope of the expression
    i.e.
    ```cpp
    int return5() { return 5; }

    int x{ 5 }; // 5 is an rvalue expression
    const double d{ 1.2 }; // 1.2 is an rvalue expression

    int y { x }; // x is a modifiable lvalue expression
    const double e { d }; // d is a non-modifiable lvalue expression
    int z { return5() }; // return5() is an rvalue expression (since the result is returned by value)

    int w { x + 1 }; // x + 1 is an rvalue expression
    int q { static_cast<int>(d) }; // the result of static casting d to an int is an rvalue expression
    ```
* return5(), x+1 & static_cast are rvalues because these expressions produce temporary values that are not identifiable objects

_OVERALL_
lvalue expressions - evaluate to an identifiable object
rvalue expressions - evaluate to a value / temporary object

### value categories & operators

now we can answer why
5 = x; // is not valid
x = 5; // is valid

- binary `operator=` expects its left operand to be a modifiable lvalue expression
- `5 = x` fails because the left operand expression 5 is an rvalue, not a modifiable lvalue

### lvalue-to-rvalue conversion

`x = y;` // y is not an rvalue, but this is legal

- in cases where an rvalue is expected but an lvalue is provided, the lvalue undergoes _lvalue-to-rvalue conversion_
- under the hood, lvalue is evaluated to produce its value, which is an rvalue

`x = x + 1`

- on the left, x is an lvalue expression that evaluates to variable x
- on the right, x undergoes lvalue-to-rvalue conversion, & is evaluated so that it can be used as the left operand of `operator+`, returning a total rvalue expression 3

### lvalue vs rvalue

- Lvalue expressions - evaluate to functions or identifiable objects (including variables) that persist beyond the end of the expression.
- Rvalue expressions - evaluate to values, including literals and temporary objects that do not persist beyond the end of the expression.

## chp 12.3: 
## chp 12.4: 
## chp 12.5: 
## chp 12.6: 
## chp 12.7: 
## chp 12.8: 
## chp 12.9: 
## chp 12.10: 