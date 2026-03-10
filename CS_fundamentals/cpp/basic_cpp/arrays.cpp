int arrays() {
    int arr[3];

    int* ptr = arr; // 1. POINTER TO FIRST ELEMENT
    // vs
    int (*arr_ptr)[3] = &arr; // 2. POINTER TO ENTIRE ARR

    // --------------------------------------------------------------------------------------------
    // 1. POINTER TO FIRST ELEMENT
    // - arr decays from int[3] -> int*
        // void foo(int *p) { => cant declare a nested function
            // no knowledge of size
        // }
    // - ptr points to arr[0]
    // - sizeof(ptr) returns sizeof(int)
    // - size NOT preserved
    // - ptr arithmetic
    ptr + 1; // moves by sizeof(int)
    // - usage:
    ptr[0]; // arr[0]
    ptr[1]; // arr[1]
    ptr[2]; // arr[2]
    // * most commonly used

    // --------------------------------------------------------------------------------------------
    // 2. POINTER TO ENTIRE ARR
    // - ptr type => int (*)[3]; points to 1 object: array arr
        // void foo(int (*p)[3]) {
            // knows array has exactly 3 elements
        // }
    // - ptr points to entire arr
    // - sizeof(ptr) returns sizeof(int[3])
    // - size preserved
    // - usage:
    (*arr_ptr)[0]; // arr[0]
    (*arr_ptr)[1]; // arr[1]
    // * NOT commonly used
}