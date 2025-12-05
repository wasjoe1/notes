#!/usr/bin/env python3

# can be found in leetcode qns 208

# A tries (aka prefix tree) is a tree data structure used to efficiently store & retrieve keys in a dataset of strings
# (or the way i interpret is retrieve substrings/ strings from dataset of strings).
# This can be used in programs such as autocomplete, spellchecker, or even contains() methods.

# Trie implementation
class Node:
    def __init__(self, char):
        self.is_end = False # no need character, since u already know the char
        self.children = {} # use a dict => {c: node, ...}; better naming would be children

    def f_is_end(self): # cant be the same name as a variable
        return self.is_end

    def set_end(self):
        self.is_end = True

class Trie:
    def __init__(self):
        self.head = Node(None)

    def insert(self, word: str) -> None:
        curr = self.head
        for c in word:
            if not curr.children.get(c):
                curr.children[c] = Node(c)
            curr = curr.children[c]
        curr.set_end()

    def search(self, word: str) -> bool:
        curr = self.head
        for c in word:
            if not curr.children.get(c):
                return False
            curr = curr.children[c]
        return curr.f_is_end()

    def startsWith(self, prefix: str) -> bool:
        curr = self.head
        for c in prefix:
            if not curr.children.get(c):
                return False
            curr = curr.children[c]
        return True

def main():
    # Code to test Trie
    # refer to leetcode test cases

    # Your Trie object will be instantiated and called as such:
    # obj = Trie()
    # obj.insert(word)
    # param_2 = obj.search(word)
    # param_3 = obj.startsWith(prefix)
    pass

if __name__ == "__main__":
    main()
