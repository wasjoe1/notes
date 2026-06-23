# Trees

Trees are interesting data structures that silently optimizes operations in everyday machines/ operations.

Some important trees:
- BST
- AVL tree                  => in MEM (less popular than red-black tree)
- Red black tree            => in MEM (OS virtual MEM)
- B tree / B+ tree          => database (disk storage)
- trie tree                 => fast text search ; router IP forwarding tables

* All trees above (except trie tree) are variants of BST

generally:
in MEM: AVL vs Red-black tree
disk: B-tree vs B+ tree
string search: trie tree

# BST

properties:
- each node has at most 2 children
- for any node, all values in left subtree are smaller than all values in the right subtree
- not balanced: no strict rule for height difference between left & right child nodes

* because of its unbalanced property, operations are bounded by O(N) time complexity

# AVL tree

=> Strict BST

properties:
- 1st 2 properties are the same as BST
- strictly balanced: height difference between left & right is always 1
    - guarantees fast lookups
    - slow updates: inserts/ deletes/ updates require complex rotations to rebalance tree

condition to use:
- more searches > less writes/ updates

use cases:
- MEM mgmt: some OS kernels & language runtimes use AVL trees to track allocated MEM blocks & find specific MEM address
- network routing: used in routing tables to look up IP addresses or filter network traffic
- geometric DBs: in-MEM spatial indexing (find nearby points on a map)
- high-read in-MEM cachees: custom in-MEM lookups where data is loaded once & read multiple times

not good to use:
- in-MEM data structures that require high rates of updates / inserts / deletes (i.e. c++'s `std::map` or java's `TreeMap`)
- DBs perform better with cache locality (sequential reads of contiguous blocks of data); AVL tree's nodes are allocated independently in disk & sequential data is scattered across different locations, slowing down the read/ write operations
    - unlike B+ trees, AVL trees cant link leaf nodes together, making DB range queries slows

resource(Abdul bari): https://www.youtube.com/watch?v=jDM6_TnYIqE&t=29s

# Red Black tree

=> Loose AVL tree

properties:
- 1st 2 properties are the same as BST
- balanced: longest path to root is at most 2x shortest path

condition to use:
- write heavy workloads
- predictable worst-case latency (rotation count per op is constant, tighter bounds on tail latency for rebalancing => hence used in kernel code)

use cases:
- in-MEM data structures that require high rates of updates / inserts / deletes (i.e. c++'s `std::map` or java's `TreeMap`)
- OS virtual MEM mgmt: `vm_area_struct`; kernel uses red-black tree to track virtual MEM regions allocated to a process; allows fast allocation & deallocation
- epoll: linux's network I/O multiplexing facility uses RB trees to monitor & track registered file descriptors
    - 
- network routing: Hierarchical token bucket (HTB); network traffic control system in OS uses red-black trees to manage bandwidth queues; tells the OS which network q to process base on current rate (priority involved)
    - i.e. a queue sends a packet, it tokens out, kernel re-calculates its next new allowed time slot to send, then deletes that queue node from the front & re-inserts it deeper into the tree

not good to use:

* i learnt about this tree while on exchange and below is lecture notes from UC Berkley which explains it well
resource: https://www.learncs.site/resource/cs61b/lecture/[61B%20SP24]%20Lecture%2018%20-%20Data%20Structures%204_%20Tree%20Rotation%20and%20Red-Black%20Trees.pdf

## AVL vs Red Black trees

Red black trees, because of its loose balance, require fewer rotations during updates
- insertion: AVL require _multiple rotations_ up the tree, RB tree only require max of _2 rotations_
- deletion: AVL tree triggers cascade of rotations all the way up to the root (O(logn)), RB tree only requires a max of _3 rotations_

# B tree & B+ tree

resource(Abdul bari): https://www.youtube.com/watch?v=aZjYr87r1b8&t=2063s

