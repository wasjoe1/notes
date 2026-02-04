# Strip white spaces (leading, trailing, both)
# CHECK/ TRANSFORM UPPER & LOWER
# CONVERT STRING TO DATETIME
# CONVERT DATETIME TO STRING

# ------------------------------------------------------------------------------
# Strip white spaces (leading, trailing, both)
string: str = "   hello   "
print(string.strip()) # returns "hello"
print(string.lstrip()) # returns "hello   "; strips leading spaces, on the left
print(string.rstrip()) # returns "   hello"; strips trailing spaces, on the right

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
