# notes
Random unorganised notes taken while learning cpp

# 1
what does vector<int> ans = nums; do?
```cpp
std::vector<int> ans = nums; // creates a new vector by COPYING nums!!
// 1. allocate MEM for ans
// 2. copy each element from nums to ans

```

is it because its copy by value, so when i change the element in ans, it doesnt change it in nums
[cling]$ nums
(std::vector<int, allocator<int> > &) { 2, 2, 3 }
[cling]$ v
(std::vector<int> &) { 1, 2, 3 }
[cling]$ 
as can be seen from here?
<!-- can see that OG array is not affected since it is just COPY-ing elements over!! -->

# 2
what does container.insert() do?
```cpp
ans.insert(ans.end(), nums.begin(), nums.end()); // insert adds elements into a container at a specified position
// insert into ans
// at position ans.end() => the end of the ans vector
// copy elements from range nums.begin() to nums.end() => if u think about it, its just elements from the nums vector
// key word is COPY

// return value of insert => iterator
// iterator insert(iterator pos, InputIt first, InputIt last);
```

# 3
This 2 version when compared, why is the 1st one faster?
## version 1
vector<int> ans;
ans.reserve(nums.size() * 2);
ans.insert(ans.end(), nums.begin(), nums.end());
ans.insert(ans.end(), nums.begin(), nums.end());

## version 2
vector<int> ans = nums;
ans.insert(ans.end(), nums.begin(), nums.end());
return ans;