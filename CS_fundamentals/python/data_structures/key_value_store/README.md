# Key value store implementation

This key value store supports 3 basic functions: **Begin**, **Commit** & **Rollback** (definitions are described below)

## Functions
### Begin()
Starts a new transaction allowing user to perform multiple operations as a batch. Changes made in this transaction are temporary until user either commits or roll them back
### Commit()
Finalizes the transaction, applying all the changes made since the begin() call permanently to the key-value store
### Rollback()
Cancels the current transaction, undoing all the changes made since the begin() call & reverting the key-value store to the state it was in before the transaction began


## Certain clarifications:
- if rollback() was called before begin() was called, exception raised 
- if commit() was called before begin() was called, exception raised
- if its already in transaction & begin() is called, nested transaction occurs
- if alteration actions occur with no transaction in place, perm storage is used

## Exception considerations:
- IllegalStateError -> indicates an invalid state, methods pre-condition are not met (is a runtime exception; caused by programming logic errors) => meant to alert devs to fix logic
- RuntimeException -> because being in the wrong state is a runtime error, we could raise the runtime exception for these cases as well (since python has no builtin IllegalStateError)

## Description of my implementation:
- transaction system will support nested transactions (i.e. T1 calls put (x, 1), T2 calls put (y, 2), rollback() is called, T2 is discarded but not T1) supports, getting, putting and deleting values from the key value store
- if no temp transaction was initiated, alteration actions done will be to the permanent key value store


## Design decisions:
1. **IllegalStateError vs RuntimeError**
IllegalStateError is more inconvenient to implement as extra code is required to be written; RuntimeError is convenient
IllegalStateError is more explicit and better informs the developer

2. **get() - return None or KeyError, if key does not exist**
- None is straightforward & easy to implement. aligns with expected behaviour of DS like dictionary
- None handles missing keys without wrapping calls in try-except blocks => code is cleaner
- None follows convention, as mentioned python dictionary get() returns None as well
- None is more performant, compared to raising an exception which is costly in terms of execution time
- KeyError requires explicit handling => more cumbersome, less clean code
- KeyError encourages proper handling, devs are ensured to not overlook cases/ logical errors in their code
- Overall, decide on None due to consistency across expected bhaviours of DS in python
- Since delete was handled gracefully as well without raising an exception, this shall be the approach