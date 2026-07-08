# vectors

in this video, cherno talks about how to use std::vectors optimally in these aspects:

- allocations of contiguous block of MEM: 1
- copies: 0
- moves: 0

## when to use

2 reasons NOT to use `std::vectors`:
1. amount of contiguous MEM allocated is static
2. std::vectors is allocated dynamically (MEM on heap), while std::array allocates MEM in persistent storage

## best practices (that prioritizes performance)

### 1st version: 6 allocations

```cpp
static int s_AllocationCount = 0;

void* operator new(size_t size) {
    std::cout << "Allocated " << size << " bytes\n";
    s_AllocationCount++; // this increments the allocation count every time u needed to allocate a new contiguous block of MEM
    return malloc(size);
}

struct Data {
    int value = 0;
    
    Data() = default;
    Data(int value)
        : Value(value) {}
}

static void PrintVecor(std::vector<Data> vector) {
    ... // implementation of printing vectors
}

int main() {
    std::vector<Data> vector;
    
    for (int i = 0; i < 5; i++)
        vector.push_back(Data(i)) // if reserve() is used, it will push_back at the empty index (i.e. index 0), but if resize used, it will push_back on the nth index => same with emplace_back(...)

    PrintVecor(vector);

    std::cout << s_AllocationCount << " allocations\n" // returns 8 here

    std::cin.get();
}
```

- 1 allocation from copying vector into the `PrintVector` function 
    - pass by value causes a copy & allocation of new contiguous MEM
    - we should apss by reference instead
    - change from `static void PrintVecor(std::vector<Data> vector)` to `static void PrintVecor(const std::vector<Data>& vector)`
- `push_back` causes re-allcoation; 5 allocations
    - add the line `vector.reserve(n);` which allocates a block of contiguous MEM for n elements
    - if u set the size in the constructor itself, it allocates MEM & initializes default values inside these MEM (`std::vector vector(5);` == `vector.resize(n);`)
    - `resize()` - allocates + initializes & you have to do `vector[i] = Data(i);`
    * reduces this to 1 allocation

### 2nd version: 1 allocation + 5 copy

```cpp
static int s_AllocationCount = 0;
static int s_CopyCount = 0;

void* operator new(size_t size) {
    std::cout << "Allocated " << size << " bytes\n";
    s_AllocationCount++; // this increments the allocation count every time u needed to allocate a new contiguous block of MEM
    return malloc(size);
}

struct Data {
    int value = 0;
    
    Data() = default;
    Data(int value)
        : Value(value) {}
    
    // copy constructor
    Data(const Data& other)
        : Value(other.value)
    {
        s_CopyCount++;
        std::cout << "Copied data\n"
    }
}

static void PrintVecor(const std::vector<Data>& vector) {
    ... // implementation of printing vectors
}

int main() {
    std::vector<Data> vector;
    vector.reserve(5);
    
    for (int i = 0; i < 5; i++)
        // vector.push_back(Data(i)) // copy was done here! creates the 5 copies
        vector.emplace_back(i) // jsut pass in the arguments for construction here (reduces the copies to 0)

    PrintVecor(vector);

    std::cout << s_AllocationCount << " allocations\n" // returns 8 here
    std::cout << s_CopyCount << " copies\n" // returns 8 here

    std::cin.get();
}
```

- `vector.push_back(Class(arg))` actually causes a copy operation to occur
    - this is because a temp object is created first
    - it is then copied into the MEM space of the vector
- better practice: `vector.emplace_back(arg)`
    - this constructs the object directly in the vector's MEM block
    - no copy operation

Q. what if there was a move constructor?

### 3rd version: 1 allocation + 0 copy + 5 moves

```cpp
static int s_AllocationCount = 0;
static int s_CopyCount = 0;
static int s_MoveCount = 0;

void* operator new(size_t size) {
    std::cout << "Allocated " << size << " bytes\n";
    s_AllocationCount++; // this increments the allocation count every time u needed to allocate a new contiguous block of MEM
    return malloc(size);
}

struct Data {
    int value = 0;
    
    Data() = default;
    Data(int value)
        : Value(value) {}
    
    // copy constructor
    Data(const Data& other)
        : Value(other.value)
    {
        s_CopyCount++;
        std::cout << "Copied data\n"
    }
    
    // move constructor
    Data(const Data&& other) // uses an rvalue reference
        : Value(other.value)
    {
        s_MoveCount++;
        std::cout << "Moved data\n"
    }
}

static void PrintVecor(const std::vector<Data>& vector) {
    ... // implementation of printing vectors
}

int main() {
    std::vector<Data> vector;
    vector.reserve(5);
    
    for (int i = 0; i < 5; i++)
        // vector.push_back(Data(i)) // move was done here! (creates the 5 moves)
        vector.emplace_back(i) // jsut pass in the arguments for construction here => removes the moves entirely 1 allocation + 0 copy + 0 moves

    PrintVecor(vector);

    std::cout << s_AllocationCount << " allocations\n" // returns 8 here
    std::cout << s_CopyCount << " copies\n" // returns 8 here
    std::cout << s_MoveCount << " moved\n" // returns 8 here

    std::cin.get();
}
```

- `vector.push_back(Data(i))` sees that `Data(i)` is an rvalue & decides to do _move semantics_
    - this causes 5 move operations
- to avoid this, we can jsut do `vector.emplace_back(i);`

* end best case would be 1 allocation + 0 copy + 0 moves

### 4th version

- if you noticed, vector is actually not necessary here since we have a static contiguous block of MEM
- jsut use array!