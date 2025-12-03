# design_hashmap
[OOP]

- `put()`, `get()` & `remove()` methods
- hash(key) to get the hashed value then % by the length to ensure the index fits in to the len of the array of buckets => 


* collision schemes
    - Open addressing
    - chaining
* primary clustering => is when many keys collide into the same initial probe region, creates large consecutive filled slots
    * linear probing encounters primary clustering
* secondary clustering => keys with same initial hash value follow the exact same probe sequence, but keys with different initial hashes do not join this cluster
    * quadratic probing encounteres secondary clustering
* double hashing avoids both types of clusterings!!
