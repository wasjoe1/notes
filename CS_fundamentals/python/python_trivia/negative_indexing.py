# negative indexing
# access elements in a sequence type (list, tuple, str, bytes, etc.) using -ve indexes

arr = ['a', 'b']
# Implementation: arr[-k] == arr[len(arr) - k] == arr[n - k]
# , where n = len(arr)
arr[-1] # returns last element; == arr[n-1]

# EDGE CASES:
# (1) -ve DOes not wrap
arr[-3] # Raise: IndexError; == arr[n-3] == arr[-1] which is not possible
# (2) empty arr raises err
arr = []
arr[-1] # Raise: IndexError

# negative slicing
# slicing a DS using -ve index values
# same implementation # Implementation: arr[-k] == arr[len(arr) - k] == arr[n - k]
# BUT once u are past the 0th index i.e. -3, u just keep getting 'smaller'
# -4  -3  -2  -1
#        ['a' 'b']
arr[:-1] # returns ['a']
arr[-3:] # returns ['a', 'b']
arr[-3: -2] # returns []    => excludesthe last index
arr[-3: -1] # returns ['a']    => excludesthe last index