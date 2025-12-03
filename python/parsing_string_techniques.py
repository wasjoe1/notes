# Strip white spaces (leading, trailing, both)


# ------------------------------------------------------------------------------
# Strip white spaces (leading, trailing, both)
string: str = "   hello   "
print(string.strip()) # returns "hello"
print(string.lstrip()) # returns "hello   "; strips leading spaces, on the left
print(string.rstrip()) # returns "   hello"; strips trailing spaces, on the right

# ------------------------------------------------------------------------------