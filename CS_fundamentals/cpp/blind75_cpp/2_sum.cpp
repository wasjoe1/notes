#include <unordered_map>
#include <vector>
#include <utility> // for pair
#include <algorithm> // for sort()

using std::vector; // include this as the solution below does not specify the std:: name space
using std::pair;
using std::sort;

// to maintain cpp namespace hygiene
// dont do using namespace std; => coz imports everything from std & cause namespace pollution; conflict with other libs

// google cpp style guide say DONT use `using namespace std;`
// competitive programming say to use `using namespace std;` => to save time

class Solution {
// 2 ways to do this:
    // 1. store map => then see if there exists a value in the set that can already fulfill the target
    // 2. sort the vector, then use 2 pointers to find the target value => guaranteed 1 soln

public:
    // store as map, & find the target val
    vector<int> twoSum(vector<int>& nums, int target) {
        // i guess i do need a unordered_map => to store {x: idx, ...}
        std::unordered_map<int, int> target_idx_map;

        // for (int i = 0; i < v.size(); ++i) {
        for (size_t i = 0; i < nums.size(); ++i) {
            // use size_t => because v.size() returns size_t type, else compiler will warn about comparison between signed & unsinged => sometimes might convert signed to unsigned => then -ve numbers becomes HUGE
            // v.size() returns # of elements
            // get mem size => v.size() * sizeof(int)
            
            int curr_val = nums[i];
            int curr_target = target - curr_val;
            auto it = target_idx_map.find(curr_target);

            if (it != target_idx_map.end()) {
                return {it->second, (int)i}; // i is always after
            }
            // else continue finding
            target_idx_map[curr_val] = i;
        }
        return {}; // note that we get compilation warning => non-void function does not return a value in all control path
        // if -Werror flag is enabled, it will be raised as a compilation error instead
    }

    vector<int> twoSum(vector<int>& nums, int target) {
        // create the array of pairs
        vector<pair<int, int>> arr;
        for (int i = 0; i < nums.size(); ++i) {
            arr.push_back({nums[i], i}); // push_back == append
        }

        // sort the pairs in arr => arr.begin() returns an iterator => generic type to iterate across the container
        //  iterators are produced by member functions of the container!
        sort(arr.begin(), arr.end()); 
        
        int l = 0, r = arr.size() - 1;

        while (l < r) {
            // check if the values are correctly getting the target value
            int sum_val = arr[l].first + arr[r].first;
            if (sum_val == target) {
                return {arr[l].second, arr[r].second}; // arr[i] is not a pointer, its the actual pair value => thus use . instead of ->
            } else if (sum_val < target)
            {
                l += 1;
            } else {
                r -= 1;
            }
        }
        // if they reached the end
        return {};
    }
};
