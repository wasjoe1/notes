#include<vector> // for std::vector
#include<iostream> // for printing things to output stream
#include<list> // for std::list

// QUICK USE
int quick() {
    int arr[5] = {1,2}; // remaining elements are 0-initialized
    std::vector<int> v_convert(arr, arr+3);

    std::vector<int> v = {1,2,3};
    std::vector<int> v_another(v.begin(), v.end());
    
    v.push_back(4);
    for (int x : v) std::cout << x << ',';
    std::cout << '\n';
    v.pop_back(); // pops the last element from the vector
    for (int x : v) std::cout << x << ',';
    std::cout << '\n';
    v.size(); // current number of elements in the vector
    for (int x : v) std::cout << v.size() << '\n';
    v.capacity(); // allocated_space for thsi vector (maybe larger than size)
    for (int x : v) std::cout << v.capacity() << '\n';

    v[0];        // fast, no bounds checking
    v.at(0);     // bounds-checked (throws exception)
    v.front();
    v.back();
    v.push_back(5); // append
    v.pop_back(); // pop
    v.insert(v.begin() + 1, 10); // insert a new element at index 1; shifts elements O(n)
    v.erase(v.begin() + 2); // deletes elements at index 2; shifts elements O(n)
    v.clear(); // deletes all elements; destructor called for every element O(n)
    v.shrink_to_fit(); // may free memory
}

// DETAILED
int detailed() {
    // std::vector is a dynamic arr that can grow & shrink automatically
    // 1. INITIALIZATION
    std::vector<int> v; // empty vector of ints
    std::vector<int> nums = {1,2,3}; // initialize with vals; this is an initializer list; this syntax is only supported from c++11 onwards
    std::vector<int> v = {1,2,3}; // this is an initializer list; this syntax is only supported from c++11 onwards
    // before c++11,
    // (1) devs had to manually populate the vector as they couldnt use initializer lists `{}`
    // ... many push_back()s
    // or (2) using a constructor that takes a range of iterators
    int arr[] = {1,2,3}; // array/ aggregate initialization => array arr decays to a pointer to its first element i.e. int* ptr = &arr[0] == arr
    std::vector<int> v(arr, arr+3); // from arr[0] to arr[2]; vector constructor expects [first, last)
        // - range constructor syntax; vector constructor takes 2 pointers/ iterators
        // - the 3 does not mean that 3 addresses are traversed (so its not exact of 4bytes * 3!!) => this is pointer arithmetic instead
        // - arr decays to a pointer to the 1st element (int*)
        // - during arr + 3, compiler does pointer arithmetic, not raw byte arithmetic => + n moves n elements forward, not n bytes
        // - compiler knows the size of the element type, int in this case
    
    // 2. POINTERS AS ITERATORS
        // an iterator is an object that lets you traverse a container ele by ele
        // pointer is the simplest form of iterator
    int* p = arr; // pointer to 1st element
    p + 1; // this moves by sizeof(int) bytes
    int* past_last = p + 3; // pointer past last element

    
    // 3. MODIFICATION (append, pop, insert, erase, clear)
    v.push_back(1); // appends ints
    v.push_back(2);
    v.push_back(3);
    v.push_back(4);
    v.pop_back(); // pops the last element from the vector
    v.insert(v.begin() + 1, 10); // insert a new element at index 1; shifts elements O(n)
    v.erase(v.begin() + 2); // deletes elements at index 2; shifts elements O(n)
    v.clear(); // deletes all elements; destructor called for every element O(n)
    v.shrink_to_fit(); // may free memory

    // 4.SIZE & CAPACITY(space allocated)
    v.size(); // current number of elements in the vector
    v.capacity(); // allocated_space for thsi vector (maybe larger than size)
    
    // 5. ACCESS
    int x = v[0]; // will NOT throw err (even if doesnt exist) => undefined behavior; might crash, return garbage, might "work" no guarantees; but no C++ errors
    int y = v.at(1); // throws err (if doesnt exist); throws std::out_of_range exception
    
    // 6. ITERATION
    // use direct elements
    for (int x : v) {
        std::cout << x << "\n";
    }
    // using indices, size_t
        // - unsigned nature: size_t is an unsigned int type used to represent sizes of objects in mem
        // - compiler warning: v.size() returns type size_t (unsigned) whereas int is (signed); comparison between int & size_t triggers compiler warning
        // - able to hold max size: on 64 bit systems, size_t is usually unsigned long (64 bits); vs int is usually (32 bits) which could overflow for huge vectors
    for (size_t i = 0; i < v.size(); i++) {
        std::cout << v[i] << "\n";
    }

    // 7. CHECKING VECTOR EQUALITY
    // content
    if (v == nums) { // this checks content element wise
        std::cout << "Vectors have the same contents!";
    }
    // reference
    if (&v == &nums) {
        std::cout << "Same object in MEM";
    } else {
        std::cout << "diff object in MEM";
    }
}
// ------------------—------------------—------------------—------------------—------------------—-
// RANGE CONSTRUCTOR
void range_constructor() {
    // 1. CONVERT A CONTAINER TO ANOTHER (list -> vector)
    std::vector<int> v = {1, 2, 3, 4};
    std::list<int> l(v.begin(), v.end());

    // 2. COPY PART OF A CONTAINER
    std::vector<int> sub(v.begin() + 1, v.begin() + 3); // {2, 3}

    // 3. TURN RAW ARRAY INTO CONTAINER
    int arr[] = {10, 20, 30};
    std::vector<int> v(arr, arr + 3);
    //OR
    std::vector<int> v(arr, arr + sizeof(arr)/sizeof(arr[0])); // => no builtin len(arr) so this is the standard
    // OR
    std::vector<int> v(std::begin(arr), std::end(arr)); // auto compute start & end pointers
    v.begin() + 2;  // (vector) ✅ valid, vector is random-access iterator
    l.begin() + 2; // (lsit) ❌ invalid, list iterators are not random-access

    // 4. COPYING NON PRIMITIVE OBJECTS
    // class RandomClass {}; // empty class; () is used for constructors
    class RandomClass {
    public:
        RandomClass(int) {} // empty constructor & parameter unused
    };

    std::vector<RandomClass> v = {
        RandomClass(1),
        RandomClass(2),
        RandomClass(3)
    };
    // std::vector<RandomClass> v2(v, v + 3); // ❌ this is invalid => v is not a pointer unlike when copying from an arr
                                            // its not because of RandomClass but because this is copying from a vector (STL container)
    std::vector<RandomClass> v2(v.begin(), v.begin() + 3); // valid range constructor

    // * range constructors dups the objects themselves, not just addresses!!
}