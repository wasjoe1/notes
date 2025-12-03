# Redundant connection
[union find]
- init(), always has ranks & parents dictionary ⇒ add both in find()
    - `{}` creates an empty dictinoary, not a set!!
    - `{val1, val2 …}`  creates a set, not a dict!!
    - can use either `dict()` or `set()`
- for union() make sure to use parent node instead of x, y (child nodes) ⇒ coz we are comparing parents to see if they are in the same set
