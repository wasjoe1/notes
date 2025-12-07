// At the time of writing, i am a total newbie to CPP and am just trying to get use to the syntax
#include <iostream>
#include <vector> // part of the c++ std lib

int main() {
    // print hello world
    std::cout << "hello world" << std::endl;
    // << stream insertion operator => sends data to an output stream i.e. std::cout
    // can chain this i.e. std::cout << "hello" << "World!" << 123 << "\n";
    // std::endl
        // => adds a new line
        // => flushes the output buffer immediately so data can be seen on the screen; ensures output is seen right away

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

    return 0; // optional but good practice
}
