#include<vector>
#include<iostream>

// ------------------—------------------—------------------—------------------—------------------—-
// FOR loops
int for_loops () {
    std::vector<int> v = {1, 2, 3};
    // 1. INDEX-BASED FOR LOOP
    for (int i = 0; i < 10; ++i) { // use pre-increment(++i) instead of post increment (i++) => slightly more efficient
        // loop body
        // pre-increment(++i) => increment first, returns the newly incremented val
        // post increment (i++) => return old val, then increment
        int first_ele = v[0];
    }
    // 2. RANGE-BASED FOR LOOP
    for (int x : v) {
        std::cout << x << ",";
    }
}
