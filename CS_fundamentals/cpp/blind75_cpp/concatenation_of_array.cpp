#include <vector>

using std::vector;

class Solution {
public:
    // 2nd attemp more canonical
    vector<int> getConcatenation(vector<int>& nums) {
        // insert numbers into end of iterator
        nums.insert(nums.end(), nums.begin(), nums.end());
        return nums;
    }
};

class Solution_1 {
public:
    // 1st attempt
    vector<int> getConcatenation(vector<int>& nums) {
        // create temp arr
        int n = nums.size();
        int temp[n]; // non-canonical
        for (int i = 0; i < n; ++i) {
            temp[i] = nums[i]; // copy over the value
        }
        for (const int x : temp) {
            nums.push_back(x);
        }
        return nums;
    }
};