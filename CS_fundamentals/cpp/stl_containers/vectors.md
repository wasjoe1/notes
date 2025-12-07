# Vectors
A vector is a dynamic sized array in the standard template lib (STL) that auto grows in size

# std::vectors vs arrays
std::vector
- size: dynamic => can grow & shrink
- MEM mgmt: auto => how??
- bounds checking: v.at(i) checks; v[i] doesnt
- copy/ assign: deep copies
- resize: v.resize(n)
- performance: slight overhead, but contiguous in mem like an array

C-style array
- size: fixed at compile time
- MEM mgmt: manual
- bounds checking: no built-in checking
- copy/ assign: manual; implementation is tricky or error-prine
- resize: impossible => need new arr
- performance: fastest possible
