# Simple questions
This is a collection of questions which are simple enough that they dont need a dedicated file for note taking.

---------------------------------------------------------------------------------------------------
## Arrays & Hashing

### contains dulicate
1. use a for loop & 1 by 1 check if element in the set, if yes return True, else add the element into the set. return False at the end
2. compare len of nums set & arr return len(set(nums)) != len(nums)

### valid anagram
- anagram is a word that can be reconstructed with all the characters from another word

### 2 sum/ two sum
- use dict => O(n) time & space (check as u add into the dict)
- use sort + 2 pointers => O(nlogn)

---------------------------------------------------------------------------------------------------
## GREEDY

### hands of straight
1. min heap => do it in O(n)
2. counter

* heapq.heapify & counter.keys()
    ```python
    import heapq
    pq = list(counter.keys()) # counter.keys() do not return a list & hence cant be used in heapify
    heapq.heapify(pq)
    ```
    * DONT DO: `pq = heapq.heapify(list(counter.keys()))` as `heapq.heapify(...)` does not return the heapified list, it heapifies the list in place
