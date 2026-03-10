#include <string>

using std::string;

struct Node {
    Node* children[26]; // 26 characters
    bool is_word;
    
    // Node() {
    //     is_word = false;
    //     for (int i = 0; i < 26 ; ++i) {
    //         children[i] = nullptr; // set to null first since there is no addresses available yet
    //     }
    // }
    
    // initializer list
    Node() : is_word(false) {
        for (int i = 0; i < 26; ++i) {
            children[i] = nullptr;
        }
    }
};
// default initialization Node n; =>> constructor runs
class Trie {
private:
    Node* dummy_root;
    // default initialization of dumm_root = garbage => coz its a pointer!
public:
    Trie() {
        // constructor
        dummy_root = new Node(); // dont place on stack, else it will become dangling pointer (pointer points to invalid MEM)
    }
    
    void insert(string word) {
        // when inserting the word, keep iterating down the root node
        // while (curr_idx < word.size()) { // is not nullptr
        
        Node* curr = dummy_root;
        for (char c : word) {
            char curr_c = c - 'a';
            // printf(curr->children[curr_c]);
            // printf("%d\n", curr_c);
            if (!curr->children[curr_c]) {
                // it is a nullptr, we need to insert the character via a new node
                // Node* new_node = new Node(); // address of object is returned
                curr->children[curr_c] = new Node();
            }
            curr = curr->children[curr_c];
        }
        curr->is_word = true;
    }
    
    bool search(string word) {
        // 2 ways this would fail
        // 1. while getting to the end of the word, the curr pointer becomes nullptr
        // 2. at the end, the node is not a word
        
        Node* curr = dummy_root;
        for (char c : word) {
            // if the curr pointer's children does have the character c
            c = c - 'a';
            if (!curr->children[c]) { // implicitly converts to bool
                return false; // doesnt have the character
            }
            curr = curr->children[c]; // update pointer
        }
        if (!curr->is_word) {
            return false;
        }
        return true;
    }
    
    bool startsWith(string prefix) {
        Node* curr = dummy_root;
        for (char c : prefix) {
            // if the curr pointer's children does have the character c
            c = c - 'a';
            if (!curr->children[c]) { // implicitly converts to bool
                return false; // doesnt have the character
            }
            curr = curr->children[c]; // update pointer
        }
        return true;
    }
};

/**
 * Your Trie object will be instantiated and called as such:
 * Trie* obj = new Trie();
 * obj->insert(word);
 * bool param_2 = obj->search(word);
 * bool param_3 = obj->startsWith(prefix);
 */