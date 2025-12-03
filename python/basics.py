# basics

# SORTING (sorted & .sort())
# BINARY SERCH (bisect)
# COUNTER, DEFAULTDICT, NAMEDTUPLE, ENUM, DATACLASS, CLASS

# ------------------------------------------------------------------------------
# SORTING (sorted & .sort())
test_arr = [6,5,4,3]
# in-place sorting
test_arr.sort(key=lambda x: x[1], reverse=True) # sort by 2nd element, sort in decreasing rather than increasing order
test_arr.sort(key=None, reverse=False, lo=0, hi=len(test_arr)) # only the stated portion is sorted
# out-of-place sorting
sorted(test_arr, key=lambda x: x[1]) # sort by 2nd element
sorted(test_arr, key=lambda x: x[1], reverse=True) # sort by 2nd element in reverse order
new_arr = sorted(test_arr, key=lambda x: int(x[1:])) # sort by number that is formed by the characters after the first 1 index
# * sorted does not support hi & lo parameters

# sorting comparator
from functools import cmp_to_key
def my_cmp(prev_val, curr_val):
    # return negative if prev_val < curr_val
    # return positive if prev_val > curr_val
    # return 0 if equal
    
    # example: compare based on string length
    return len(prev_val) - len(curr_val)
test_arr.sort(key=cmp_to_key(my_cmp))

# ------------------------------------------------------------------------------
# BINARY SERCH (bisect)
import bisect
test_arr = [1,3,5,7]
bisect.bisect_left(test_arr, 5) # returns 2; returns the exact index of the value that exists inside the arr
bisect.bisect_left(test_arr, 2) # returns 1; returns the index to the left of the val in the arr
bisect.bisect_left(test_arr, 8) # returns 4; returns the next index once the target is bigger than value inside the arr

bisect.bisect_right(test_arr, 2) # returns 1; when the value is smaller, it still returns the index its supposed to be inserted at
bisect.bisect_right(test_arr, 3) # returns 2; when the value is exactly the same, it returns the index to the right of the value it == to

# to find index for values >= a target val:
target_value = 2
lo, hi = 0, len(test_arr) # lo is inclusive, BUT hi is exclusive
bisect.bisect_left(a=test_arr, x=target_value, lo=lo, hi=hi, key=lambda x: x) # this will return index 1 which is from 3 onwards
# params: a, x, lo, hi, key
# ------------------------------------------------------------------------------
# COUNTER, DEFAULTDICT, NAMEDTUPLE, ENUM, DATACLASS, CLASS
from collections import Counter, defaultdict
from typing import NamedTuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# COUNTER
arr = [1,1,1,1,2]
counter = Counter(arr) # this wil return me a dictionary where the keys are the values in the array and the value is the freq it appeared in the arr

# DEFAUL DICT
defaultdict(list) # {new_1: [], new_2: [] ...}
defaultdict(int) # {new_1: 0, new_2: 0 ...}

# NAMED TUPLE
class someTuple(NamedTuple):
    int_attrib: int
    float_attrib: float
    string_attrib: str
    # ...
st = someTuple(6,8.0,"string")
st.int_attrib # returns 6

# ENUM
class OrderType(Enum):
    CANCEL = "CANCEL"

# DATA CLASS
@dataclass(order=True)
class CancelOrder():
    datetime: datetime
    order_id: str
    order_type: OrderType.CANCEL
    id_to_cancel: str
    share_name: str
    client_name: str
dt = order_id = order_type = id_to_cancel = share_name = client_name = 1 # tbh the type checking for class, dataclass, NamedTuple, Enum types arent enforced strictly; will only be checked by mypy
cacnel_order = CancelOrder(dt,order_id,order_type,id_to_cancel,share_name,client_name)
cacnel_order.datetime # access only via dot notation, cant by bracket notation!!

# CLASS
class Node():
    def __init__(self, nxt = None, val: int = 0, key: int = 0):
        self.next = nxt
        self.val = val
        self.key = key
key = value = 10
Node(key=key, val=value) # we can dont include default kwargs & it will instantiate fine; next = None here

# ------------------------------------------------------------------------------
