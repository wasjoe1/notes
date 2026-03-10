// import std; // cpp modules => only supported in cpp 20
#include <string>
#include <map>
#include <vector>

using namespace std;

// ------------------------------------------------------------------------------------------------
// struct(public) vs classes(private)

// The only real difference is the default access level
//                          struct  class
// default member access    public  private
// default inheritance      public  private

// but in practice, struct is used mainly for plain data holders
// & classes is used when type has behaviour, invariants & encapsulation

// struct:
    // - expose fields directly
    // - little or no logic
    // i.e. node struct, small tuples, Orders(in OrderBook) etc.

// class:
    // - hides data
    // - exposes functions (methods/ member fns)
    // - enforces invariants
    // * used when u want encapsulation; real entities i.e. BankAccounts, Orderbook

struct Point {
    int x;
    int y;
};

struct Node {
    int key;
    int value;
    // Node next; // while still defining Node, ur not allowed to use it as u dk its size yet => compiler doesnt know how much space to allocate this member
    Node* next; // always use a pointer (8 bytes)
};

// ------------------------------------------------------------------------------------------------
// initializer list (MEM allocation, default initialized, )
class Node {
    // is_word: bool
    // children => only lowercase english letters
    Node* children[26]; // 26 characters
    bool is_word;
    // constructor
    // normal method
    // not as good coz:
    // 1. is_word is first default initialized
    // 2. then assigned false
    Node() {
        is_word = false;
        for (int i = 0; i < 26 ; ++i) {
            children[i] = nullptr; // set to null first since there is no addresses available yet
        }
    }
    // initializer list method => initializes member variables b4 the constructor body runs
    // better coz: directly initialize is_word with false => more efficient
    // if u had multiple memebers
    // Node() : key(0), value(0), isWord(false) {}
    Node() : is_word(false) {
        for (int i = 0; i < 26; i++) {
            children[i] = nullptr;
        }
    }
    
    // why does this definition & initialization occur?
    // when creating an object, obj must already exist in MEM b4 the constructor body runs
    // 1. MEM for obj is allocated
    // 2. all member variables are initialized
    // 3. constructor body executes => so compile cant wait till assignment then the member exists (it already needs to exist by the time Node is being assigned stuff)

    // thus:
    // 1. MEM allocated for Node
    // 2. is_word default initialized 
    // 3. constructor body runs
    // 4. assignment occurs
};

// declaration usually already allocates MEM i.e. int x;
    // => declare x
    // => mem allocated for x
    // what declaration really means is to: give it type + name
// initialize => assign 1st val at the moment its created
    // declare x
    // allocate MEM
    // initialize x with 5
// BUT for struct/ classes
    // inside struct, members are declared
    // MEM is allocated when Node obj is created

// ------------------------------------------------------------------------------------------------
// declaring struct
struct Address {
    string streetName;
    int streetNumber;
};

struct Person {
    string name;
    int age;
    Address address;
};

// ------------------------------------------------------------------------------------------------
// initiailzing structs

// old way: c-style initialization
Person p = {"John", 25, {"something", 14}};
// "initialize the obj using values inside the braces"
// some ppl might confuse with Person("John", 25, {"something", 14})

// modern cpp: using brace initialization
Person p{"John", 25, {"something", 14}};
// or
Address addr{"something", 14};
Person p{"John", 25, addr};
// prevents you from making "most vexing parse problem" in cpp
// another example:
map<string, string> capitals {
    {"UK", "London"}
};

// ------------------------------------------------------------------------------------------------
// MOST VEXING PROB in cpp
// vector<int> v(); // programmers might think that this means to "create a vector v" immediately in variable v
    // but the compiler interprets this as executing a function named v; v();

// correct way (initialization from temp)
vector<int> v = vector<int>(); //but creates a temp vector first, b4 copying/ moving into v
// new correct way (brace initialization)
vector<int> v{}; // avoids creating a temp, & immediately constructs into v
// * after cpp 17, `std::vector<int> v = std::vector<int>();` no longer creates temp; guarantees copy ellision
// * copy ellision - cpp optimization where compiler skips creating a temp obj & copy/ move that follows, & instead, constructs obj directly in its final location