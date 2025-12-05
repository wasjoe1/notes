# Str.contains => vectorized
# Str.replace => vectorized
# Df.astype => vectorized
# .sum => vecorized
# .any => vectorized

# .apply => row/ column wise depends on axis arg

# slower since its row by row
mask = df.apply(lambda row: row.astype(str).str.contains("something", na=False, regex=False), axis=1).any(axis=1)
df_filtered = df[~mask] # ~ inverts the boolean mask so that it removes the rows that arent needed

# faster since its column wise checking before row
mask = df.astype(str).apply(lambda col: col.str.contains("something", na=False, regex=False)).any(axis=1)

# even faster (its just sum operation is faster than any on some hardware)
mask = df.astype(str).apply(lambda col: col.str.contains("something", na=False, regex=False)).sum(axis=1) > 0

# what did i wanna do?
# i want to check if every row, at least 1 column contains the string im searching for
df.astype(str) # converts all the elements in the df to dtype string
df.astype(str).apply(lambda col: col.str.contains(r"\s+", na=False, regex=True), axis=0) # this applies the lambda function col wise (default)
df.astype(str).apply(lambda row: row.str.contains("random_string", na=False, regex=False), axis=1) # this applies the lambda function column wise
mask = ....any(axis=1) # checks if there is any true value for each row, and returns a mask of it
df[mask] # returns rows that contain that string
df[~mask] # returns rows that DONT contain that string


# ------------—------------—------------—------------—------------—------------—------------—------
# finding the first row that contains string, & set df to start from there
# slowest way; NOT recommended
for index in len(df):
	row = df.iloc[index]
	is_contain = row.astype(str).str.contains("something", regex=True, na=False)
	if is_contain:
		break
# - not vectorized => slow; looping over rows is much slower in python
# - less readable; verbose
# - not idiomatic => not using pandas syntax

# medium way; Recommended
# vectorizes the checking of each row's element for containing string(but column is not)
# vectorizes the checking of each row if its true
mask = df.astype(str).apply(lambda col: col.str.contains("something", regex=True, na=False)).any(axis=1)
start_index = df[mask].index[0]
df = df[start_index:].reset_index(drop=True)


# fastest way; but not idiomatic
values = df.astype(str).to_numpy() # converts this to 2d numpy of strings
# np.char.find(values, "something") applies a vectorized operation on ALL elements (.find("something") is an element-wise opertaion)
# happens in natice C loops => faster than python-level iteration
mask = (np.char.find(values, "something") >= 0).any(axis=1) # applies row wise 
start_idx = np.argmax(mask)
new_df = df.iloc[start_idx:].reset_index(drop=True)