#!/usr/bin.env python3

# Key value store implementation
# This key value store supports 3 basic functions: Begin, Commit & Rollback (definitions are described below)

# Begin() - Starts a new transaction allowing user to perform multiple operations as a batch.
# Changes made in this transaction are temporary until user either commits or roll them back

# Commit() - Finalizes the transaction, applying all the changes made since the begin() call permanently to the key-value store

# Rollback() - Cancels the current transaction, undoing all the changes made since the begin() call & reverting the key-value store
# to the state it was in before the transaction began

class IllegalStateError(RuntimeError):
    def __init__(self, msg="Illegal state for this operation"):
        self.message = msg
        super().__init__(self.message) # Exception __init__(self, *args)
# can also just raise RuntimeError

# storage for key-val store is using a dict
# am thinking that begin has nested transactions
# when begin is called w or wo a current session, it will create a temp storage to be edited, this is added into a stack (so the latest one can be edited)
# commit instruction will be commited to the 2nd last temp storage, or if theres only 1 temp storage, i want to commit it to perm storage
    # commit without begin will be an illegal state exception => use a runtime exception in python
# rollback is called during a "begin()", (once its commmited, it cant be rolled back) => it will just pop from the stack and revert to the previous storage
    # if begin() was not called, rollback will also raise an exception => to know if its not called check the length of the temp

# for get(key), put(key, val), delete(key) => all these methods are acted on the latest kv store be it temp or perm

class key_value_store:
    
    def __init__(self):
        self.perm = {} # k-v store
        self.temp = [] # [{...}, {...}, {...}, ...]
    
    # ------------------------------------------------
    # extra functions
    def has_temp(self,):
        return len(self.temp) > 0

    def commit_to_store(self, old, new):
        for k,v in old.items():
            new[k] = v
        for k in new:
            if k not in old:
                del old[k]
        
    # ------------------------------------------------

    def get(self, key):
        if self.has_temp():
            return self.temp[-1].get(key)
        else:
            return self.perm.get(key)

    def put(self, key, value):
        if self.has_temp():
            self.temp[-1][key] = value
        else:
            self.perm[key] = value

    def delete(self, key):
        if self.has_temp():
            if self.temp[-1].get(key) != None:
                del self.temp[-1][key]
        else:
            if self.perm.get(key) != None:
                del self.perm[key]

    def begin(self):
        temp = None
        if self.has_temp():
            temp = self.temp[-1].copy()
        else:
            temp = self.perm.copy()
        self.temp.append(temp)

    def commit(self):
        if self.has_temp():
            latest = self.temp.pop()
            if self.has_temp():
                self.commit_to_store(latest, self.temp[-1]) # doesnt return anythin
            else:
                self.commit_to_store(latest, self.perm) # doesnt return anythin
        else:
            raise RuntimeError("Execute begin() before executing commit()")

    
    def rollback(self):
        if self.has_temp():
            self.temp.pop()
        else:
            raise RuntimeError("Execute begin() before executing rollback()")



def test_key_value_store():
    count = 0
    kv_store = key_value_store()

    # TEST 1: Test put() and get() for permanent storage
    kv_store.put("key1", "value1")
    assert kv_store.get("key1") == "value1", "Failed to retrieve value from permanent storage"
    print("test 1 passed")
    count += 1

    # TEST 2: Test delete() for permanent storage
    kv_store.delete("key1")
    assert kv_store.get("key1") is None, "Failed to delete value from permanent storage"
    print("test 2 passed")
    count += 1

    # TEST 3: Test begin(), put(), and get() for temporary transactions
    kv_store.begin()
    kv_store.put("key2", "value2")
    assert kv_store.get("key2") == "value2", "Failed to retrieve value from temporary transaction"
    print("test 3 passed")
    count += 1
    
    # TEST 4: Test rollback()
    kv_store.rollback()
    assert kv_store.get("key2") is None, "Rollback did not remove the temporary value"
    print("test 4 passed")
    count += 1

    # TEST 5: Test begin() and commit() for permanent storage updates
    kv_store.put("key3", "value3")
    kv_store.begin()
    kv_store.put("key3", "temp_value3")
    kv_store.commit()
    assert kv_store.get("key3") == "temp_value3", "Commit did not update the permanent value"
    print("test 5 passed")
    count += 1

    # TEST 6: Test multiple begin() and rollback()
    kv_store.begin()
    kv_store.put("key4", "temp_value4")
    kv_store.begin()
    kv_store.put("key4", "temp_value4_updated")
    kv_store.rollback()  # Should rollback the last temp transaction
    assert kv_store.get("key4") == "temp_value4", "Rollback did not work as expected"
    print("test 6 passed")
    count += 1

    # TEST 7: Test commit() after nested transactions
    kv_store.commit()
    assert kv_store.get("key4") == "temp_value4", "Commit did not finalize the value correctly"
    print("test 7 passed")
    count += 1

    # TEST 8: Test IllegalStateError on commit() without begin()
    try:
        kv_store.commit()
    except RuntimeError as e:
        assert str(e) == "Execute begin() before executing commit()", "Failed to raise IllegalStateError on commit without begin()"
        print("test 8 passed")
        count += 1

    # TEST 9: Test IllegalStateError on rollback() without begin()
    try:
        kv_store.rollback()
    except RuntimeError as e:
        assert str(e) == "Execute begin() before executing rollback()", "Failed to raise IllegalStateError on rollback without begin()"
        print("test 9 passed")
        count += 1

    print(f"{count}/9 tests passed")
    if count == 9:
        print("All tests passed!")
    else:
        print("Some tests failed :(")

def main():
    # code to test key value store
    test_key_value_store()

if __name__ == "__main__":
    main()