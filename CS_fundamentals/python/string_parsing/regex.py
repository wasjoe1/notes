import re

# COLLAPSE LONG SPACES INTO 1 SPACE
# REMOVE LEADING / TRAILING SPACES
# REMOVE MULTIPLE MATCHES

# -------------------------------------------------------------------------------------------------
# COLLAPSE LONG SPACES INTO 1 SPACE
regex_pattern = "\\s+"
regex_pattern = r"\s+" # essentially the same thing but coz regex has alot of `\` hence we can use r-string to not rewrite so many \

replacement = " "
string = "hello    test   check"
result_str = re.sub(regex_pattern, replacement, string)
verify_string = "hello test check"

assert verify_string == result_str
print(verify_string == result_str)

string = " hello    test   check "
verify_string = " hello test check "
result_str = re.sub(regex_pattern, replacement, string) # this only replaces spaces, but dont remove them
assert verify_string == result_str
print(verify_string == result_str)

# -------------------------------------------------------------------------------------------------
# REMOVE LEADING / TRAILING SPACES

s = "    leading removed"
s = re.sub(r"^\s+", "", s) # ^ - start of string
assert s == "leading removed"
print(s)

s = "trailing removed    "
s = re.sub(r"\s+$", "", s) # $ - end of string
assert s == "trailing removed"
print(s)

s = "    leading & trailing removed    "
s = re.sub(r"^\s+|\s+$", "", s) # equivalent to strip()
assert s == "leading & trailing removed"
print(s)

# -------------------------------------------------------------------------------------------------
# REMOVE MULTIPLE MATCHES
s = "cat and dog"
s = re.sub(r"cat|dog|\s+", "", s) # | - OR operation
assert s == "and"
print(s)
