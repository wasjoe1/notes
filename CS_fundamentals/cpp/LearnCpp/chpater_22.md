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
    - even when compiler does apply NRCO, the language still requires that a valid, non-deleted, copy or move constructor be selectable at the return statement
    - so if Auto_ptr1 has a deleted copy constructor & no move constructor (like the e.g.) compiler fails to compile (HENCE our issue here!!)

### resolve 2: move semantics (move ownership) [Auto_ptr2]

core idea: what if we transfer/ move ownership of th epointer from the soruce to the destination object? => move semantics

move semantics - class will transfer ownership of the object rather than making a copy

### Auto_ptr2 - move semantics via copy constructor

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

## chp 22.2: rvalue references
## chp 22.3: 
## chp 22.4: 
## chp 22.5: 
## chp 22.6: 
## chp 22.7: 
## chp 22.8: 
## chp 22.9: 
## chp 22.10: 