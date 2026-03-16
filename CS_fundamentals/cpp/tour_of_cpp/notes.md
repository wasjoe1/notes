# Tour of CPP
just some thoughts i found important while reading the book.
does not include additional notes i have scribbled on the book itself LOL

## chapter 1
## chapter 2 User defined types
### intro
- user defined types preferred over built in types
    - ez to use
    - less error prone
    - more efficient
### classes
- `new` oeprator allocates mem on the heap / free store => indpt of the scope from which they are created in
- `void vector_init(Vector& v, ints)` -> pass v by non-const reference (__pass by non-const reference__)
- 
    ```cpp
    class Vector {
        public:
        Vector(ints) :
            elem{new double[s]},
            sz{s} {}
        double& operator[](int i) { return elem[i]; } // created method for element access: subscripting
        // returns a refernce to the ith ele, allows both read & write since its not const
        private:
        double* elem;
        int sz;
    }
    ```
- referring to the code above, user defined types are always the same size
    - Vector obj can have different # of elements but the object size itsefl remains constant (1 ptr, 1 int)
- mentioend **destructor**? but wait till 5.2.2 to learn LOL
### enums
- enums underlying type is int
- 
    ```cpp
    // enumerator class
    enum class Color {red, green, blue}''
    // bad
    int i = Color::red // compiler err => Color::red is not an int
    Color c = 2; // initialization err
    // good
    Color col = Color::red // enumerators are in the scope of their `enumerator class`
    Color x = Color{5}; // OK, using copy initialization is fine
    Color y{6}; // OK, list initialization
    int x = int(Color::red);// explicitly convert enum val to underlying type => allowed
    
    // plain enums
    enum Color {red, green, blue};
    int col = green; // allowed => enumerators of plain enum are entered into the same scope as the name of their enum!!
    ```
- `enum Color { RED, GREEN, BLUE };` does not allocate MEM at all! => compile-time constants


- 
    ```cpp
    // write code
    ```