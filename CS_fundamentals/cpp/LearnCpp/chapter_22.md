# chapter 22: move semantics & smart pointers &

## chp 22.1: intro: MEM leak & smart pointer class

### issue 0: MEM Leak

```cpp
class Resource {}; // or struct

int main () {
    Resource* ptr = new Resource();
    
    int x;
    if  (x==0) return; // function might return early here

    delete ptr; // might not be executed
}
```

- `new Resource()` asks the c++ runtime's heap allocator for a chunk of MEM on the heap
- the allocator has either free space already mapped into process's virtual address space OR it requests more from the OS via `mmap`
- when ptr is not deleted / deallocated, "MEM is leaked"
    - MEM leak - means that the allocator's metadata still marks that chunk of MEM as "in use"
        pointer's value is lost when ptr goes out of scope so there is no way to free it now
        as long as process stays alive, MEM stays unavailable to the rest of the program => less available MEM to use
- when process exits, OS just tears down the entire address space, so other processes can now use the MEM

### smart pointer class (example)

- classes contain destructors that get executed when an object goes out of scope
- can allocate MEM in constructor, then dellocate MEM in destructor
- MEM is guaranteed to be deallocated when class object is destroyed

_Auto_ptr1_ - delete op
```cpp
template <typename T>
class Auto_ptr1 {
    T* m_ptr {}; // value-initialization (instead of default initialization) so that m_ptr contains null_ptr instead of garbage value
public:
    // constructor: takes in a pointer (default is nullptr) & sets m_ptr
    Auto_ptr1(T* ptr=nullptr)
        : m_ptr(ptr) {}
    
    // destructor: deletes the ptr
    ~Auto_ptr1() { delete m_ptr; }

    // overload dereference(*) & arrow(->) operators so we can use Auto_ptr1 like a normal pointer
    T& operator*() const { return *m_ptr; } // i.e. *x = 6; changes what y really holds, if int* x = &y;
    // this * operator returns the same result as *ptr BUT, their mechanisms are different
        // raw pointer dereference (*ptr) - built-in language opereation, not a function call
            // compiler emits a direct MEM access => a direct load or store instruction
        // smart pointer operator*, returning reference type
            // syntactic sugar for a function call: `*x` literally becomes `x.operator*();`
            // function body does a raw dereference internall (*m_ptr)
            // function just returns a reference & the outer expression opereates on that returned reference (*x = 6)
    T* operator->() const { return m_ptr; } // i.e. *x->m_var returns the value of m_var of the actual T object
    // -> operator behaves differently from every other overloadable operator
        // its special-cased by the compiler & applied repeatedly until it terminates at a raw pointer
        // i.e. ptr->member; becomes (ptr.operator->())->member;
        // eventually it becomes (m_ptr)->member; => -> is not a built-int arrow operator on a raw pointer
        // compiler's rule to stop is when `operator->` returns a raw pointer
        // hence we return a pointer type
};

class Resource {
public:
    Resource() { std::cout << "Resource acquired\n"; }
    ~Resource() { std::cout << "Resource destroyed\n"; } // when pointer is deleted, the object its pointing to is destroyed (deconstructed + MEM unallocated)
};

int main() {
    // create an Auto_ptr object that stores a pointer of Resource* type
    // T is Resource type
    // new Resource() => returns a pointer, not an object of Resource type
    Auto_ptr1<Resource> res(new Resource()); // same as Auto_ptr1<Resource> res = Auto_ptr1<Resource>(new Resource())
    return 0; // upon exit, destructor for Auto_ptr1 is called
}
```

`delete ptr;` does 2 things
1. calls the destructor of the object `ptr` points to
    - runs any cleanup logic the object's class defines
2. deallocates the MEM that object was occupying, returning it to the heap allocator

* HOWEVER the pointer variable itself isnt destroyed or nulled
    - it still holds the same address
    - it now becomes a _dangling pointer_ - pointer pointing at MEM that was once valid but no longer valid
    - good practice `delete ptr; ptr = nullptr;`
* _dangling pointer_
    - if (nullptr) { ... } => nullptr conceptually address 0, returns false, defined behavior: dereferenceing it immediately crashes (segfault)
    - if (dangling_ptr) { ... } => dangling_ptr returns true as it holds the same address as before, undefined behavior: dereferenceing it migh crash OR might silently succeed

### smart pointer class

smart pointer - composition class designed to manage dynamically allocated MEM & ensure that MEM gets deleted when the smart pointer object goes out of scope
    built-in pointers are sometimes called "dumb pointers" because they cant clean up after themselves
    `Auto_ptr1` is an example of a smart pointer

### issue 1: critical flaw (with Auto_ptr1)

(due to auto generated code in class declarations => implicit copy constructor)

```cpp
// same classes as before
int main() {
    Auto_ptr1<Resource> res1(new Resource());
    Auto_ptr1<Resource> res2(res1); // copy-initialization
}
```

- both res1 & res2 now have pointers pointing to the same address
- when 1 of the 2 goes out of scope, the other is left with a dangling pointer
- undefined behavior for 2nd delete

```cpp
// another example with the same proble
void passByValue(Auto_ptr1<Resource> res) {}
int main() {
    Auto_ptr1<Resource> res1(new Resource());
    passByValue(res1);
}
```

- res1 will be copied by value into the parameter res
- both res1.m_ptr & res.m_ptr will hold the same address
- when the function ends, res is destroyed, & res1.m_ptr is left dangling
- when res1 goes out of scope later, undefined behavior occurs (same MEM region is unallocated => most likely crash)

### resolve 1: delete copy constructor & assignment operator

delete both to prevent copy operations / disallow pass by value

### issue 2: how to pass the pointer's address out of a function

```cpp
??? generateResource()
{
    Resource* r{ new Resource() };
    return Auto_ptr1(r);
}
```

misconception: i thought this is okay because of URVO & NRVO?
1. returning prvalue directly (temporary object)
    - `return Auto_ptr1<Resource>(new Resource());` this works, unconditionally, in C++17 & later => but what about earlier versions?
2. returning a named local object
    - NRVO is actually optional, even in c++17/20/23
    - compilers are permitted to elide move/ copy operations & almost all compilers fo it in simple cases like this
    - but C++ standard does not require it
    - even when compiler does apply NRVO, the language still requires that a valid, non-deleted, copy or move constructor be selectable at the return statement
    - so if Auto_ptr1 has a deleted copy constructor & no move constructor (like the e.g.) compiler fails to compile (HENCE our issue here!!)

### resolve 2: move semantics (move ownership) [Auto_ptr2]

core idea: what if we transfer/ move ownership of th epointer from the soruce to the destination object? => move semantics

move semantics - class will transfer ownership of the object rather than making a copy

### Auto_ptr2 - move semantics via copy constructor

_Auto_ptr2_ - delete op + shift pointer
```cpp
template <typename T>
class Auto_ptr2
{
	T* m_ptr {};
public:
	Auto_ptr2(T* ptr=nullptr)
		:m_ptr(ptr)
	{
	}

	~Auto_ptr2()
	{
		delete m_ptr;
	}

	// A copy constructor that implements move semantics
	Auto_ptr2(Auto_ptr2& a) // note: not const
	{
		// We don't need to delete m_ptr here.  This constructor is only called when we're creating a new object, and m_ptr can't be set prior to this.
		m_ptr = a.m_ptr; // transfer our dumb pointer from the source to our local object
		a.m_ptr = nullptr; // make sure the source no longer owns the pointer
	}

	// An assignment operator that implements move semantics
	Auto_ptr2& operator=(Auto_ptr2& a) // note: not const
	{
		if (&a == this)
			return *this;

		delete m_ptr; // make sure we deallocate any pointer the destination is already holding first
		m_ptr = a.m_ptr; // then transfer our dumb pointer from the source to the local object
		a.m_ptr = nullptr; // make sure the source no longer owns the pointer
		return *this;
	}

	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
	bool isNull() const { return m_ptr == nullptr; }
};
```

* `std::auto_ptr`
    - was introduced in c++98, deprecated in c++11 & removed in c++17
    - `std::auto_ptr` implemented move semantics just like Auto_ptr2 class does

### issue 3: dangerous to implement move semantics using copy constructor

1. passing by value (i.e. when using a function) will cause the resource to get moved to the function parameter
    function parameters then gets destroyed at the end of the function when they get out of scope
    afterwards, when accessing the ptr outside of the function, you will reference a deleted ptr (dereferencing null pointer etc.)
2. `std::auto_ptr` always deletes its contents using non-array delete; `delete` instead of `delete[]`
    this means auto_ptr wont work with dynamically allocated arrays becoz of the wrong type of deallocation
    furthermore, it doesnt prevent passing it a dynamic array, causing mismanagement & hence MEM leaks
3. it doesnt work well with other classes in the std lib; containers & algos
    its because std lib assumes that when an item is copied, it actually makes a copy & not move operation

* core problem: there was no mechanism to differentiate "copy semantics" from "move semantics" (pre c++11)

## chp 22.2: rvalue references (referring to the variable)

### lvalue reference (recap)
- prior to c++11, there was only 1 type of reference, hence it was just called "reference"
- in c++11 & after, its called lvalue reference

_lvalue reference_ - `(int& y = _)`
- can only be initialized with modifiable l-values

_lvalue reference to const objects_ - `(const int& y = _)`
- can be initialized with modifiable & non-modifiable l-values & r-values
- these values cant be modified though
* are useful because they allow us to pass any type of argument(l-value or r-value) into a function without making a copy of the argument

### rvalue reference

- in c++11, r-value reference was added
- rvalue reference - designed to be initialized with rvalue only
- created using double ampersand
    ```cpp
    int x{5};
    int& rref{5}; // lvalue reference initialized with l-value x
    int&& rref{5}; // rvalue reference initialized with r-value 5
    ```

_2 properties_
rvalue references have 2 properties:
1. rvalue references extend the lifespan of the object they are initalized with to the lifespan of the rvalue reference
    - lvalue refereces to const objects can do this too
2. non-const rvalue references allow you to modify the rvalue [impt!!]
    i.e.
    ```cpp
    class Fraction {
    private:
        int m_numerator { 0 };
        int m_denominator { 1 };
    public:
        Fraction(int numerator = 0, int denominator = 1) :
            m_numerator{ numerator }, m_denominator{ denominator } {}

        friend std::ostream& operator<<(std::ostream& out, const Fraction& f1) {
        // friend std::ostream& operator<<(std::ostream& out, Fraction& f1) => *this actually still works!
            out << f1.m_numerator << '/' << f1.m_denominator;
            return out;
        }
    };

    int main() {
        auto&& rref{ Fraction{ 3, 5 } }; // r-value reference to temporary Fraction
        // f1 of operator<< binds to the temporary, no copies are created.
        std::cout << rref << '\n'; // prints 3/5
    } // rref (and the temporary Fraction) goes out of scope here
    ```

- as an anonymous object, `Fraction(3,5)` normally goes out of scope at the end of the expression in which it is defined
- because we initialized an rvalue reference with it, its duration is extended until the end of the block
    * note the 2nd signature in comments & think why it works, we will discuss it later

another e.g. (less intuitive)
```cpp
int&& rref{ 5 }; // initialize r-value reference with a literal, a temporary with value 5 is created
rref = 10;
std::cout << rref << '\n';
```

- it may seem weird to init an rvalue reference with a literal value, & be able to change that value
- BUT during initialization of an rvalue reference with a literal, a temporary object is constructed from the literal
    such that the reference, is referencing a temporary object, not a literal value

* both examples above are not common usage of rvalue references, below is the common usage.

### rvalue references as function parameters

- rvalue references are typically used as function parameters
- used in function overloads, to have different behaviors for lvalue & rvalue args (by taking in lvalue & rvalue)
```cpp
// l-value arguments will select this function
void fun(const int& lref) { std::cout << "l-value reference to const: " << lref << '\n'; }

// r-value arguments will select this function
void fun(int&& rref) { std::cout << "r-value reference: " << rref << '\n'; }

int main() {
	int x{ 5 };
	fun(x); // l-value argument calls l-value version of function
	fun(5); // r-value argument calls r-value version of function
}
```

### rvalue reference variables are lvalues

consider this:
```cpp
int&& ref{5};
fun(ref); // which version of fun would be called: fun(const int&) OR fun(int&&)
```

- fun(const int&) is called
- although ref has type int&&, when used in an expression, it is an lvalue => named variables
    - type of an object & its value category are independent
    i.e.
    5 is rvalue, type int
    int x is lvalue, type int
    int&& ref is lvalue, type int&&
    - hence, fun(int&&) was not called as: _rvalue references cant bind to lvalues_
* remember the function signature: `friend std::ostream& operator<<(std::ostream& out, Fraction& f1)`
    - `rref` was an lvalue categoy (rvalue reference variable), of type Fraction&&
    - you might wonder then how come `Fraction&` can take in type `Fraction&&`?
        => variable rref has type `Fraction&&`
        => but the result of the expression `rref` has type `Fraction` & is an lvalue
        * the result of an expression has the same type as the underlying object's type, & is always an lvalue;
            `&` & `&&` just indicates whether variable is binding to a lvalue or rvalue
* once you create a variable that binds to an rvalue object, that variable is an lvalue

### returning rvalue reference

- (almost) never return an rvalue reference, for the same reason you (almost) never return an lvalue reference
    - might end up returning a handing reference when the referenced object goes out of scope

## chp 22.3: move constructors & assignment

previous: discussed downside when copy constructor, designed for copy semantics, was used to implement move semantics
this chapter: move constructors & move assignment to resolve downside

### copy constructor, deep copy

_Auto_ptr3_ - delete op + deep copy
```cpp
template<typename T>
class Auto_ptr3 {
	T* m_ptr {};
public:
	Auto_ptr3(T* ptr = nullptr)
		: m_ptr { ptr } {}
	~Auto_ptr3() { delete m_ptr; }

    // Deep copy-ing
	// Copy constructor
	Auto_ptr3(const Auto_ptr3& a) {
		m_ptr = new T;
		*m_ptr = *a.m_ptr;
	}
	// Copy assignment
	Auto_ptr3& operator=(const Auto_ptr3& a) {
		// check first
		if (&a == this)
			return *this;
		delete m_ptr;

        // copy
		m_ptr = new T;
		*m_ptr = *a.m_ptr;
		return *this;
	}

	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
	bool isNull() const { return m_ptr == nullptr; }
};
class Resource {...}; // same as above

Auto_ptr3<Resource> generateResource() {
	Auto_ptr3<Resource> res{new Resource}; // initial creation of Resource, (1) constructor invoked
	return res; // this return value will (2) invoke the copy constructor
}

int main() {
	Auto_ptr3<Resource> mainres; // mainres already constructed
	mainres = generateResource(); // this assignment will invoke the (3) copy assignment (NO Copy elision - mandatory copy elision only takes effect for initialization)
        // => hence temp object created
}
```

- display:
    Resource acquired
    Resource acquired
    Resource destroyed
    Resource acquired
    Resource destroyed
    Resource destroyed
- steps for display:
    1. `generateResource()` has local `res` variable & initializaed with Resource object => "1st Resource acquired"
    2. `res` is returned back to main() by value
        - need to _return by value_ & not address or reference because res is a local variable & will be destroyed
        - res is copy constructed into a _temp object_ (function's return slot)
        - copy constructor does deep copy, so another `new Resource()` was allocated, 2nd "Resource acquired"
        - when `res` goes out of scope, 1st "resource destroyed" was called
    3. temp obj is assigned to mainres by copy assignment
        - copy assignment does deep copy => `new Resource` is allocated here, 3rd "Resource acquired"
        - assignment expression ends, & _temp obj_ goes out of expression scope & is destroyed, 2nd "resource destroyed" called
    4. at the end, mainres goes out of scope & 3rd "resource destroyed" calls
    * NOTE: the lifetime of a temp object of a return value from the function, lasts until the end of the expression instead of the function block

### move constructor, steal resource

_move constructors & assignment_

- C++ defines 2 new functions in service of move semantics: move constructor & move assignment operator
- goal of move ops is to move ownership of resources from 1 object to another
- both functions use _non-const rvalue reference parameters_ => only bind to rvalue

_Auto_ptr4_
```cpp
#include <iostream>

template<typename T>
class Auto_ptr4 {
	T* m_ptr {};
public:
	Auto_ptr4(T* ptr = nullptr)
		: m_ptr { ptr } {}

	~Auto_ptr4() { delete m_ptr; } // deleting a null_ptr is no-op (does nothing)

	// Copy constructor
	Auto_ptr4(const Auto_ptr4& a)
	{
		m_ptr = new T;
		*m_ptr = *a.m_ptr;
	}

	// Move constructor
	Auto_ptr4(Auto_ptr4&& a) noexcept
		: m_ptr { a.m_ptr } {
		a.m_ptr = nullptr;
	}

	// Copy assignment
	Auto_ptr4& operator=(const Auto_ptr4& a)
	{
		// Self-assignment detection
		if (&a == this)
			return *this;
		delete m_ptr; // Release any resource we're holding

		// Copy
		m_ptr = new T;
		*m_ptr = *a.m_ptr; // member access has higher precedence than unary * (dereference) => same as *(a.m_ptr)
		return *this;
	}

	// Move assignment
	Auto_ptr4& operator=(Auto_ptr4&& a) noexcept {
		// Self-assignment detection
		if (&a == this)
			return *this;
		delete m_ptr; // Release any resource we're holding

		// Transfer ownership => a.m_ptr to m_ptr
		m_ptr = a.m_ptr;
		a.m_ptr = nullptr; // we'll talk more about this line below
		return *this;
	}

	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
	bool isNull() const { return m_ptr == nullptr; }
};

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

Auto_ptr4<Resource> generateResource()
{
	Auto_ptr4<Resource> res{new Resource};
	return res; // this return value will invoke the move constructor
}

int main()
{
	Auto_ptr4<Resource> mainres;
	mainres = generateResource(); // this assignment will invoke the move assignment

	return 0;
}
```

- instead of deep copy `*m_ptr = *a.m_ptr;` we just move teh src object's resources `m_ptr = a.m_ptr` involving shallow copy of src pointer & set src pointer to null
- when executed, `Resource acquired` & `Resource destroyed` runs once only
- move constructors & assignment should be marked as `noexcept`

### implicit creation of move constructor & assignment

compiler will create an implicit move constructor & assignment operator if all of the following are true:
- no user-declared copy constructors or copy assignment operators
- no user-declared move constructors or move assignment operators
- no user-declared destructor

=> copy constructors are generated if user-defined move constructors arent declared
=> so having a normal constructor `Class(int a, int b)` will implicitly generate _both copy & move_ constructors!

implicitly generated functions do a memberwise move, following:
- if member has move constructor / assignment, it will be invoked
- else member is copied

=> implicit move constructors/ assingment will copy pointers, not move them. hence you need
    to define the move constructor & assignment yourself

### move constructor + disable copy

_Auto_ptr5_ - disable copy; only have move semantics
```cpp
#include <iostream>

template<typename T>
class Auto_ptr5
{
	T* m_ptr {};
public:
	Auto_ptr5(T* ptr = nullptr)
		: m_ptr { ptr }
	{
	}

	~Auto_ptr5()
	{
		delete m_ptr;
	}

	// Copy constructor -- no copying allowed!
	Auto_ptr5(const Auto_ptr5& a) = delete;

	// Move constructor
	// Transfer ownership of a.m_ptr to m_ptr
	Auto_ptr5(Auto_ptr5&& a) noexcept
		: m_ptr { a.m_ptr }
	{
		a.m_ptr = nullptr;
	}

	// Copy assignment -- no copying allowed!
	Auto_ptr5& operator=(const Auto_ptr5& a) = delete;

	// Move assignment
	// Transfer ownership of a.m_ptr to m_ptr
	Auto_ptr5& operator=(Auto_ptr5&& a) noexcept
	{
		// Self-assignment detection
		if (&a == this)
			return *this;

		// Release any resource we're holding
		delete m_ptr;

		// Transfer ownership of a.m_ptr to m_ptr
		m_ptr = a.m_ptr;
		a.m_ptr = nullptr;

		return *this;
	}

	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
	bool isNull() const { return m_ptr == nullptr; }
};
```

- move constructors & assignment should be marked as `noexcept`
	- tells compiler that functions will not throw exceptions
- when & which constructors are called
	- move: move functions are defined args for construction is an rvalue (typicall a literal or temp value)
	- copy: copy functions are used otherwise; when arg is an lvaule OR when arg is rvalue + move fns arent defined
- if you delete copy constructor, compiler will not generate an implicit move constructor
    => makes objects neither copyable nor moveable
    => after deleting copy constructor, need to declare move constructors!

### other notes
- **move functions should always leave both objs** in a valid state => dont leave rvalue with dangling pointer; undefined behavior
- **automatic l-values returned by value (of a function) may be moved instead of copied** => generateResource return res by value, its moved instead of copied
    - c++ specification has special rule that allows l-value that return by value to be moved since they will be destroyed at the end of the function
    * in some cases, copy & move are both elided
- **disabling copy**: Auto_ptr4 left in copy constructor for comparison purpose; in move-enabled classes, it is sometimes desireable
    to delete the copy constructor to ensure copies arent made


### timer (comparing performance)
```cpp
#include <cstddef> // for std::size_t

template <typename T>
class DynamicArray
{
private:
	T* m_array {};
	int m_length {};

	void alloc(int length)
	{
		m_array = new T[static_cast<std::size_t>(length)];
		m_length = length;
	}
public:
	DynamicArray(int length)
	{
		alloc(length);
	}

	~DynamicArray()
	{
		delete[] m_array;
	}

	// Copy constructor
	DynamicArray(const DynamicArray &arr) = delete;

	// Copy assignment
	DynamicArray& operator=(const DynamicArray &arr) = delete;

	// Move constructor
	DynamicArray(DynamicArray &&arr) noexcept
		:  m_array { arr.m_array }, m_length { arr.m_length }
	{
		arr.m_length = 0;
		arr.m_array = nullptr;
	}

	// Move assignment
	DynamicArray& operator=(DynamicArray &&arr) noexcept
	{
		if (&arr == this)
			return *this;

		delete[] m_array;

		m_length = arr.m_length;
		m_array = arr.m_array;
		arr.m_length = 0;
		arr.m_array = nullptr;

		return *this;
	}

	int getLength() const { return m_length; }
	T& operator[](int index) { return m_array[index]; }
	const T& operator[](int index) const { return m_array[index]; }
};

#include <iostream>
#include <chrono> // for std::chrono functions

class Timer
{
private:
	// Type aliases to make accessing nested type easier
	using Clock = std::chrono::high_resolution_clock;
	using Second = std::chrono::duration<double, std::ratio<1> >;

	std::chrono::time_point<Clock> m_beg { Clock::now() };

public:
	void reset()
	{
		m_beg = Clock::now();
	}

	double elapsed() const
	{
		return std::chrono::duration_cast<Second>(Clock::now() - m_beg).count();
	}
};

// Return a copy of arr with all of the values doubled
DynamicArray<int> cloneArrayAndDouble(const DynamicArray<int> &arr)
{
	DynamicArray<int> dbl(arr.getLength());
	for (int i = 0; i < arr.getLength(); ++i)
		dbl[i] = arr[i] * 2;

	return dbl;
}

int main()
{
	Timer t;

	DynamicArray<int> arr(1000000);

	for (int i = 0; i < arr.getLength(); i++)
		arr[i] = i;

	arr = cloneArrayAndDouble(arr);

	std::cout << t.elapsed();
}
```

* move constructor is faster

### issues with move semantics & `std::swap`

- copy & swap also works for move semantics - we implement move ops by swapping resources with the obj that will be destroyed
	2 benefits
	1. persistent obj now controls the resources that were previously under ownership of the dying object (primary goal)
	2. dying obj now controls the resources that were previously under ownership of the persistent object	
		=> when the dying obj actually dies, it can do required cleanup on the old resources
- `std::swap` comes to mind when implementing swap for move ops
	- BUT its problematic as `std::swap()` calls both move constructor & assignment on move-capable objs
		=> infinite recursion

```cpp
#include <iostream>
#include <string>
#include <string_view>

class Name
{
private:
    std::string m_name {}; // std::string is move capable

public:
    Name(std::string_view name) : m_name{ name }
    {
    }

    Name(const Name& name) = delete;
    Name& operator=(const Name& name) = delete;

    Name(Name&& name) noexcept
    {
        std::cout << "Move ctor\n";

        std::swap(*this, name); // bad!
    }

    Name& operator=(Name&& name) noexcept
    {
        std::cout << "Move assign\n";

        std::swap(*this, name); // bad!

        return *this;
    }

    const std::string& get() const { return m_name; }
};

int main() {
    Name n1{ "Alex" };
    n1 = Name{"Joe"}; // invokes move assignment
}
```

- example's result:
	Move assign
	Move ctor
	Move ctor
	... (infinite callign of move ctor)
- `std::swap(*this, name)` keeps calling `move(...)` constructors of `*this` & name
	swap()'s rough implementation:
	```cpp
	T temp{ std::move(a) } // calls T's move constructor
	a = std::move(b) // calls T's move assignment
	b = std::move(temp) // calls T's move assignment
	```

### Resolve for `std::swap`: swap member function should not call move ops

- implement the move constructor & assignment using your own swap function
- our own swap function can call `std::swap` on member variables => as long as their move ops dont recursively call themselves 
	=> avoid recursive calls by invoking `std::swap` on the `std::string` member
- but swap function should not be called on the current class
	=> else it will keep recursively calling the current's class move

```cpp
#include <iostream>
#include <string>
#include <string_view>

class Name
{
private:
    std::string m_name {};

public:
    Name(std::string_view name) : m_name{ name }
    {
    }

    Name(const Name& name) = delete;
    Name& operator=(const Name& name) = delete;

    // Create our own swap friend function to swap the members of Name
    friend void swap(Name& a, Name& b) noexcept
    {
        // We avoid recursive calls by invoking std::swap on the std::string member,
        // not on Name
        std::swap(a.m_name, b.m_name);
    }

    Name(Name&& name) noexcept
    {
        std::cout << "Move ctor\n";

        swap(*this, name); // Now calling our swap, not std::swap
    }

    Name& operator=(Name&& name) noexcept
    {
        std::cout << "Move assign\n";

        swap(*this, name); // Now calling our swap, not std::swap

        return *this;
    }

    const std::string& get() const { return m_name; }
};

int main()
{
    Name n1{ "Alex" };
    n1 = Name{"Joe"}; // invokes move assignment
}
```

* this prints:
	Move assign
	Joe

## chp 22.4: std::move

case: you want to invoke move semantics, but the objs you have are lvalues not rvlaues

### scenario 1: lvalue reference parameters cant invoke move ops

```cpp
// BAD: copy scenario
template <typename T>
void swapCopy(T& a, T& b) {
	T tmp { a }; // invokes copy constructor
	a = b; // invokes copy assignment
	b = tmp; // invokes copy assignment
}

// GOOD: move scenario
template <typename T>
void swapCopy(T& a, T& b) {
	T tmp { std::move(a) }; // invokes move constructor
	a = std::move(b); // invokes move assignment
	b = std::move(tmp); // invokes move assignment
}
```

- in c++ 11, std::move is a std lib fn that casts (using static_cast) its arguments into an rvalue reference
	basically, converts luvaes into rvalues

### scenario 2: filling elements of a container

```cpp
std::vector<std::string> v;
std::string str { "knock" };
v.push_back(str); // calls lvalue version of push_back, copies str into array
v.push_back(std::move(str)); // calls rvalue version of push_back, moves str into array
```

### moved-from objects? valid but indeterminate state

- when using std::move on lvalue objects, we can continue to access these objects after their values have been moved
- there are 2 schools of thought
	1. objects that have been moved from sohuld be reset back to default / zero state
	2. do whats convenient; moved from objects shall be placed in valid but unspecified state (can contain any value)
	* avoid using value of a moved-from object as results is implementation-specific
- moved-from object
	- safe to call any function that doesnt depend on the current value (i.e. `operator=`, `clear()`, `reset()` etc.)
	- avoid accesing elements from its container `operator[]` or `front`

### scenario 3: sorting

- `std::move` is useful when sorting, as they work by swapping pairs of elements

## chp 22.5: std::unique_ptr

smart pointers - main aim is to manage dynamically allocated resources provided by the user of the smart pointer
					it ensures the dynamically allocated objects are cleaned up (typically when the smart ptr goes out of scope)

- smart ptrs should never be dynamically allocated themselves => risk of not being deallocated
- should be allocated on the stack; this ensures smart pointer will properly go out of scope; proper deallocation
- 4 smart pointer classes: `std::auto_ptr` (removed in c++17), `std::unique_ptr`, `std::shared_ptr` & `std::weak_ptr`
	`std::unique_ptr` is most used

### `std::unique_ptr<T>(new T(args...))` & `std::make_unique<T>(args...)`

- intro:
	- is c++11's replacement for std::auto_ptr
	- used to managed dynamically allocated obj not shared by multiple objs
		- `std::unique_ptr` should completely own the obj it managed
	- lives in the <memory> header

- how to use:
	```cpp
	#include <memory>

	int main() {
		// takes in the MEM address on the heap (ptr) & is owned by the ptr
		std::unique_ptr<Resource> res{ new Resource() };

		// move semantics properly implemented
		std::unique_ptr<Resource> res2 {} // start as nullptr
		res2 = std::move(res1); // res2 assumes ownership, res1 is set to nullptr
		// res2 destroyed here when res2 goes out of scope
	}
	```
- move & copy implementation specs:
	- properly implements move semantics
	- copy initialization & assignment are disabled
	* if you want to transfer contents, MUST use move semantics
- accessing managed obj: overloaded operator* & operator->
	- operator* returns a reference to obj
	- operator-> returns a pointer (recursively calls -> operator until pointer returns, then calls built-in pointer member access)
- std::unique_ptr may not always be managing an obj (was created created empty or resource was moved)
	- std::unique_ptr has a cast to bool that returns true (if resrc exists)
	- `if (res) {...}` => implicit cast to bool
- arrays: `std::unique_ptr` is smart enough to know whether to use scalar delete or array delete
	- scalar delete `delete p1` => destroys 1 obj
	- array delete `delete[] p2` => array delete; destroys all objects in the array & frees it
	* but best practice: favor `std::array`, `std::vector` or `std::string`
- `std::make_unique()` (intro-ed in c++14)
	- is recommended over creating `std::unique_ptr` yourself
	- resolves an exception safety issue that can result from c++ leacing the order of evaluation for function args unspecified?
	```cpp
	class Fraction {
		Fraction(int numerator = 0, int denominator = 1) :
		...
	}
	// example
	auto f1{ std::make_unique<Fraction>(3,5) }; // create Fraction with numerator 3 & denominator 5 (custom class that i didnt write down)
	auto f1{ std::make_unique<Fraction[]>(4) }; // dynamically allocated array of Fractions of length 4

	// safety exception resolved
	i.e.
	process(std::unqiue+ptr<Widget>(new Widget()), risky())
	// new Widget() creates the raw pointer
	// risky() called next
	// std::unique_ptr is supposed to be called; but in the event that risky() fails, this never happens
	// * THUS, raw pointer is now MEM leaked
	```
	- no repetition of the type/ less error-prone
	```cpp
	std::unique_ptr<Widget> w(new Widget(a,b,c)) // "Widget" typed twice
	auto w = std::make_unique<Widget>(a,b,c); // typed once only; `std::unique_ptr` is returned
	```

	- under the hood implementation (my own notes)
		```cpp
		// std::make_unique UTH implementation (simplified)
		template<typename T, typename... Args>
		std::unique_ptr<T> make_unique(Args&&... args) {
			return std::unique_ptr<T>(new T(std::forward<Args>(args)...))
		}
		```
		- variadic templates - allow functions & classes to accept an arbitrary number of args of various types
			i.e.
			template<typename... Args> // declares Args as a pack of 0 or more types; if not compiler will complain that Args isnt a param pack
			void(Args... args) {} // ... allows u to take in multiple args & pack into `args`; expands pack into function parameter pack: variable number of individually-typed params, all sharing the base name args
			=> foo(1, "hello", 3.14) is called
			=> compiler deduces that Args = {int, const char*, double}
			=> ... is the syntax marking that this is a pack, not a single type
		- `Args` is just a label, can use other things like `Ts`
		- `std::forward<Args>(args)...` instead of just `args...`
			- inside the function body, `args` is treated as an lvalue expression
			- `std::forward<Args>(args)` solves this; it looks at what T was deduced to
		- `...` after `std::forward<Args>(args)`
			- expands this per-element across the whole pack
			- equivalent to `std::forward<Args0>(args0), std::forward<Args1>(args1), std::forward<Args2>(args2)`
		- forwarding references (`T&&`) - special type of reference in c++ that binds to anything (lvalues or rvalues)
			its used to take in both rvalue & lvalue types into a function for mutability (without the const)
			allows template function to take in both rvalues & lvalues that can be modified; 2 condtions needed:
			1. T is a template parameter
			2. T is being deduced at that exact spot
			- is seen in 
				1. function templates => template<typename T>; void process(T&& arg) {}; process(x) or process(5) // arg is a forwarding reference
				2. auto&& => `auto&& x = some_function();` // x is a forwarding reference
			* but the thing is these args are still lvalue references when taken into the function
			* this is to allow the function generation to be flexible (can take in both rvalue & lvalue types; not that it can take in any values)
		- reference collapsing
			lvalue arg: T deduces to T&. then parameter T&& collapses (& + && -> &) to T& (get lvalue reference)
			rvalue arg: T deduces to plain T(no reference). parameter stays as T&& (no collapsing) (get rvalue reference)
			* this is just a rule to collapse reference types when too many `&`s are produced

### Using std::unique_ptr in functions

- returning it from a function
	```cpp
	std::unique_ptr<Resource> createResource() {
		return std::make_unique<Resource>(); // create unique pointer, taking in no args
	}
	auto ptr { createResource() }; // assign the unique_ptr to ptr
	```
	- if the value is not assigned to anything, the temp return val goes out of scope & Resource is cleaned up
	- if its assigned(in c++14 & earlier; as shown above), move semantics will transfer the Resource from the return value to the object assigned to
	- in c++17 & newer, return will be elided
		* better than returning a raw pointer as there is clear ownership of who owns the pointer & destructor runs automatically

- passing it into a function
	_pass by value_ - function take ownership
	```cpp
	void takeOwnership(std::unique_ptr<Resource> res) {}
	auto ptr{ std::make_unique<Resource>() };
	// takeOwnership(ptr); // this fails, need move semantics
	takeOwnership(std::move(ptr)); // turns ptr into an rvalue, then is move-constructed in res
	```
	- pass by value: if you want to take ownership of the contents of the pointer
	- need to use `std::move` to pass in the variable as copy semantics have been disabled
	- ownership of the resource was transferred to `takeOwnership()`, so the Resource was destroyed at the end of `takeOwnership()` rather than `main()`
		* this is different from passing in by reference
	
	_pass by raw pointer_ - function want to use resource without ownership
	- most of the time, u dont want function to take ownership of the resource
	- can pass `std::unique_ptr` using `const T&` or `T&`, but its better to just pass the resource itsefl
		* allows the function to remain agnostic of how the caller is managing its resources
	- use the `.get()` member function to get raw ptr
	```cpp
	void useResource(const Resource* res) {...} // takes in a raw pointer

	auto ptr{ std::make_unique<Resource>*() };
	useResource(ptr.get());
	```

	_pass in by reference_ - function want to modify the caller's unique_ptr itself
	```cpp
	void borrowOwnership(std::unique_ptr<Resource>& res) {}
	auto ptr{ std::make_unique<Resource>() };
	borrowOwnership(ptr); // ptr still contains container
	```
	- no move, no copy nothing, just binds a reference to the pointer in the outer scope
	- idea: function is borrowing p temporarily, not taking ownership
	- can modify the unique_ptr inside the function

### other notes

- std::unique_ptr & classes
	- can use this as a composition member of classes
	- this prevents you worrying about ensuring class destructor will delete the dynamic MEM or no
	- BUT must ensure that class object is properly destroyed, else the std::unique_ptr will not be destroyed too

- misusing std::unique_ptr (2 ez ways)
	- multiple objs manage the same resource
		```cpp
		Resource* res{ new Resource() };
		std::unique_ptr<Resource> res1{ res };
		std::unique_ptr<Resource> res2{ res };
		```
		- this is legal syntactically, but both res1 & 2 will try to delete resource => UB

	- dont manually delete the resource
		```cpp
		Resource* res{ new Resource() };
		std::unique_ptr<Resource> res1{ res };
		delete res;
		```
		- if u do this, std::unique_ptr will try to delete an already deleted resource => UB

## chp 22.6: std::shared_ptr

(recap)
__std::unique_ptr__
- std::unique_ptr was designed to singly own & manage a resource

__std::shared_ptr__
- std::shared_ptr is meant to solve the case where multiple pointers need to co-own a resource
- this means: multiple shared_ptrs can point to the same resource without deallocating the resource when 1 or more goes out of scope
- std::shared_ptr lives in <memory> header

### 2 ways of creating shared_pointers (1 correct, 1 wrong)

(example Resource class)
```cpp
class Resource {
	public:
	Resource() {std::cout << "Resource acquired\n";}
	~Resource() {std::cout << "Resource destroyed\n";}
};
```

_correct_
```cpp
Resource* res{new Resource};
std::shared_ptr<Resource> ptr1 {res}; // create ptr from res (raw ptr)
{
	std::shared_ptr<Resource> ptr2{ptr1}; // create ptr2 from ptr1 (shared_ptr)
	std::cout << "Killing 1 shared pointer\n"
} // ptr2 goes out of scope
std::cout << "Killing another shared pointer\n"
// ptr1 goes out of scope & allocated resource is destroyed only once
```
	result:
	Resource acquired
	Killing 1 shared pointer
	Killing another shared pointer
	Resource destroyed
- inside the nested block, copy constructor called, to create 2nd shared_ptr
- they point to same resource
- ptr2 goes out of scope but doesnt destroy resource (since ptr1 still points to it)

_wrong_
```cpp
Resource* res{new Resource};
std::shared_ptr<Resource> ptr1 {res}; // create ptr from res (raw ptr)
{
	std::shared_ptr<Resource> ptr2{res}; // create ptr2 from res (raw ptr; instead of ptr1)
	std::cout << "Killing 1 shared pointer\n"
} // ptr2 goes out of scope
std::cout << "Killing another shared pointer\n"
// ptr1 goes out of scope & allocated resource is destroyed only once
```
	result:
	Resource acquired
	Killing 1 shared pointer
	Resource destroyed
	Killing another shared pointer
	Resource destroyed
- here, we create shared_ptr independently from each other
- ptrs arent aware of each other
- ptr2 goes out of scope, thinking its the only owner of the resource, deallocates the resource


* best practice: always copy an existing shared_ptr if u need more than 1 of it pointing to the same resource
	- also, shared_ptr can be null ptr, so always check to make sure its valid

### std::make_shared

- akin to `std::make_unique`, we should use `make_shared` to create `shared_ptr`s
- reason: simple, safe (cant create indpt ptrs), more _performant_

```cpp
// same Resource class
auto ptr1{std::make_shared<Resource>()};
{
	auto ptr2 {ptr1} // can only create ptr2 from ptr1; cant accidentally access the raw obj
}
```

### std::make_shared vs std::shared_ptr

- claim: std::make_shared is more performant
- share ptr mechanism:
	- uses 2 pointers internally
	- ptr1 points to resource
	- ptr2 points to control block (tracks stuff like count etc.)
- comparison:
	- std::shared_ptr constructor: MEM for the managed obj (usually passed in) is first created, & then control block(constructor creates) is then allocated separately
	- std::make_shared: optimized into a single MEM allocation
		* only accesses the heap once(instead of 2) + places these 2 blocks of MEM close tgt (cache locality per access)

### creating shared ptrs from unique ptrs

- unqiue_ptr converted to shared_ptr via special shared_ptr constructor
- speical constructor accepts unique_ptr rvalue
- contents of the unique_ptr will be moved to the shared_ptr
	BUT
* cant convert shared_ptr to unique_ptr safely
	=> when creating a function that is returning a smart ptr, better to return unique first then assign to shared later

### some perils & arrays

_perils_
- same issue as `std::unique_ptr` where, if the unique_ptr was not properly disposed, resource wont be deleted
- shared_ptr is worse where ALL ptrs has to be disposed of

_arrays_
in c++17 & earlier: shared_ptr doesnt properly support arrays, should not manage C-style arrays
in c++20: shared_ptr has support for arrays

## chp 22.7: circular dependency issues with std::shared_ptr & std::weak_ptr
