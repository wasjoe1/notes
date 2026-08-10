# array<n>
- array<n> requires n to be compile-time known constant => cant be a runtime const int value
- cin >> n; array<n>; => this will never work as n is known only at runtime
- no choice have to use vector

# constexpr
- ensure var is a constant expression; compile-time evaluatable

# initialization & assignment
- initialization:
    - mandatory copy elision: URVO
    - optional copy elision: NRVO
    - move semantics: no NRVO
- assignment:
    - no copy elision, always move (temp created then moved into existing slot)

# rounding error
- always
    (1st) `std::llround(floating_type)`,
    then (2nd) static_cast<to_cast_type>(val)
- 0.5 & above will round up, else round down

# arithmetic operation (implicit conversion)
- c++ decides result type base on operand's type => need to explicitly cast first
- i.e. int * int => returns int (will overflow)
- i.e. int * long long => returns long long
- i.e. int * (long long)int => returns long long (explicit cast)

# L1, L2, L3 cache
MESI protocol - cache coherence protocol; ensures all cores see the same data
M(modify) E(exclusive) S(shared) I(invalid)
- write op
    1. core 1 broadcasts invalidation req over shared MEM bus
    2. snooping: all other cores constantly monitor this bus for addresses they have in their cache
    3. when other core sees msg, they intercept it
    4. transition:
        - snooping cores: S -> I
        - write core: S -> M
- exclusive: optimization purpose => eliminate unnecessary bus traffic by giving a single core exclusive acces to a MEM region