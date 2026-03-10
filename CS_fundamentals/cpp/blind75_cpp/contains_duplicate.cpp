#include <vector>
#include <unordered_set>

using std::vector;
using std::unordered_set;

class Solution { // class => treated like a declaration => need ;
public:
    bool containsDuplicate(vector<int>& nums) { // fn => treated as definitions => no need;
        // create set
        unordered_set<int> s; // empty anws so no need for curly brace initialization
        // iterate through set
        // for (const auto& x : nums) { // avoids copying && making x a read only reference
        //     if (s.count(x)) {
        //         return true;
        //     }
        //     // else add into the set
        //     s.insert(x);
        // }
        for (const auto& x : nums) { // avoids copying && making x a read only reference
            if (!s.insert(x).second) { // returns pair<iterator, bool> => where bool is whether x was inserted & iterator points to the ele in the set
                return true;
            }
        }
        return false;
    }
};
// definition => creates entity & usually allocates storage or provides the full implementation
// declaration => tells the compiler smt exists
// * every defn is a declaration, but not every declaration is a definition
// * declaration :> defn