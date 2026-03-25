# Strip white spaces (leading, trailing, both)
# Remove consecutive spaces
# Join empty array + Join empty string
# CHECK/ TRANSFORM UPPER & LOWER
# CONVERT STRING TO DATETIME
# CONVERT DATETIME TO STRING
# Format flat with 2 dp + commas

# ------------------------------------------------------------------------------
# Strip white spaces (leading, trailing, both)
string: str = "   hello   "
print(string.strip()) # returns "hello"
print(string.lstrip()) # returns "hello   "; strips leading spaces, on the left
print(string.rstrip()) # returns "   hello"; strips trailing spaces, on the right

# ------------------------------------------------------------------------------
# Remove consecutive spaces
s = "    hello     somethign   "
arr = s.split()
print(arr)
s = " ".join(s.split())
print("remove consecutive spaces & leading/ trailing:", s) # print(a,b,c) auto adds spaces => "a b c"
print(1,2)

# ------------------------------------------------------------------------------
# Join empty array + Join empty string
"".join([]) # returns empty string ''
"".join(['', '']) # returns empty string ''

# ------------------------------------------------------------------------------
# CHECK/ TRANSFORM UPPER & LOWER
# check
'A'.isupper() # return True
'a'.islower() # return True
'1'.isupper() # return False => if not characters then its false
'!'.isupper() # return False

# transform
'string'.upper() # returns STRING
'STRING'.lower() # returns string

# ------------------------------------------------------------------------------
# CONVERT STRING TO DATETIME
# CONVERT DATETIME TO STRING
import datetime
# CONVERT STRING TO DATETIME
dt_str = "2025-07-01 14:09:00.123456+0000"
DT_FORMAT = "%Y-%m-%d %H:%M:%S.%f%z" # the + is counted as part of the tz parsing; %f expects microseconds
dt = datetime.datetime.strptime(dt_str, DT_FORMAT) # DONT BE FOOLED by the kwargs => it doesnt take any!!
# CONVERT DATETIME TO STRING
date_string = datetime.datetime.strftime(dt, DT_FORMAT[:8])

# when parsing datetime string
dt_str = "2025-07-01 14:59:01.123456+0000"
DT_FORMAT = "%Y-%m-%d %H%M%S.%f%z"
dt = datetime.datetime.strptime(dt_str, DT_FORMAT)
dt_str = datetime.datetime.strftime(dt, DT_FORMAT) # put in expected str format you want to see when converting the dt

value = 1234567.8912
formatted = f"{value:,.2f}" # the , is to format it with commas between thousand values, and .2f means 2 dp
print(formatted)

# syntax for fstring => f"{value:format_spec}"
# i.e. offset : 010d
value = 1234567.8912
formatted = f"{value:010,d}" # comma must come after the width specification
print(formatted)
# 010d
# │ │ └─ format as decimal integer
# │ └── minimum width = 10 characters
# └──── pad with zeros