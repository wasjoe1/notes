# stl vectors

tips: stop using std::vector wrongly!
why?: performance => in the sense of comparing within STL & not self optimization
resource: https://www.youtube.com/watch?v=Xx-NcqmveDc&t=386s

1. Dont use at all! => COZ heap allocation is expensive

# ------------------------------------------------------------------------------------------------
1. Dont use at all! => COZ heap allocation is expensive
when not needed (dont need dynamic insertions, just need contiguous memory &
O(1) access), just use std::array

`std::vector` => allocated on the heap
`std::array` => allocated on the stack

* heap is slower than stack, in terms of MEM allocation

```cpp

std::vector<Color> getCellColors() {
  return
}
```

# ------------------------------------------------------------------------------------------------
2. 