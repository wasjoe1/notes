#include<vector>
#include<iostream>

int main() {
    std::vector<int> v = {1,2,3}; // this is an initializer list; this syntax is only supported from c++11 onwards
    // before c++11,
    // (1) devs had to manually populate the vector as they couldnt use initializer lists `{}`
    // ... many push_back()s
    // or (2) using a constructor that takes a range of iterators
    int arr[] = {1,2,3}; // array/ aggregate initialization
    std::vector<int> v(arr, arr+3); // from arr[0] to arr[2]; vector constructor expects [first, last)
        // - range constructor syntax; vector constructor takes 2 pointers/ iterators
        // - the 3 does not mean that 3 addresses are traversed (so its not exact of 4bytes * 3!!) => this is pointer arithmetic instead
        // - arr decays to a pointer to the 1st element (int*)
        // - during arr + 3, compiler does pointer arithmetic, not raw byte arithmetic => + n moves n elements forward, not n bytes
        // - compiler knows the size of the element type, int in this case
    // pointers as iterators
        // an iterator is an object that lets you traverse a container ele by ele
        // pointer is the simplest form of iterator
    int* p = arr; // pointer to 1st element
    p + 1; // this moves by sizeof(int) bytes
    int* past_last = p + 3; // pointer past last element

    // std::vector is a dynamic arr that can grow & shrink automatically
    // initialization
    std::vector<int> v; // empty vector of ints
    std::vector<int> nums = {1,2,3}; // initialize with vals
    // append & pop
    v.push_back(1); // appends ints
    v.push_back(2);
    v.push_back(3);
    v.push_back(4);
    v.pop_back(); // pops the last element from the vector
    // size & capacity(space allocated)
    v.size(); // current number of elements in the vector
    v.capacity(); // allocated_space for thsi vector (maybe larger than size)
    // access
    int x = v[0]; // will NOT throw err (even if doesnt exist) => undefined behavior; might crash, return garbage, might "work" no guarantees; but no C++ errors
    int y = v.at(1); // throws err (if doesnt exist); throws std::out_of_range exception
    // iteration
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
    // checking vector equality
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