# this includes common methods & custom functions to parse pandas dataframes
import pandas as pd

# CREATING DATAFRAMES IN PANDS
# FILTERING BY ROWS
# CHANGING TIMEZONE IN PANDAS
# CREATING DATETIME FROM STRINGS
# PARSING DATETIME

df = pd.DataFrame()
# ------------------------------------------------------------------------------
# CREATING DATAFRAMES IN PANDS
# method 1
data = {
    "name": ["Alice", "Bob", "Charlie", "David"],
    "age": [25, 30, 35, 40],
    "city": ["NY", "LA", "SF", "Chicago"]
}
# method 2
data = {
    "name": pd.Series(["john", "james"], dtype="string"),
    "reference_period": pd.Series(
	    {
		    0: pd.Timestamp("2025-05-26 09:48:18.192000+0000", tz="UTC"),
		    1: pd.Timestamp("2025-05-26 09:48:18.192000+0000", tz="UTC")
	    }
	    , dtype="datetime64[ms, UTC]"
	   ),
    "observation_time": pd.Series(
	    {
		    0: pd.to_datetime("2025-05-26 09:48:18.192000+0000", tz=True),
		    1: pd.to_datetime("2025-05-26 09:48:18.192000+0000", tz=True)
	    }
	    , dtype="datetime64[ms, UTC]"
	   ),
}

df = pd.DataFrame(data)

# ------------------------------------------------------------------------------
# FILTERING BY ROWS
df[df["age"] > 30]
df[df["fruit"].isin(["apple", "orange"])] # returns rows where the fruit column == apple or orange; exact matches

# ------------------------------------------------------------------------------
# CHANGING TIMEZONE IN PANDAS
df["time"] = pd.to_datetime(df["time"]) # convert to datetime64[ns]
df["time"] = df["time"].dt.tz_localize("UTC") # localizes the datetime
df["time"] = df["time"].dt.tz_convert("Asia/Singapore") # changes the timezone
# or
df["time"] = df["time"].astype("datetime[ms, Asia/Singapore]") # changes the timezone

# ------------------------------------------------------------------------------
# CREATING DATETIME FROM STRINGS
date_str = "2025-06-01"
date_obj = pd.to_datetime(date_str, format="%Y-%m-%d")
date_str = "2025-jun-01"
date_obj = pd.to_datetime(date_str, format="%Y-%b-%d")

# grabbing values from datetime & inserting to strings
date_obj = pd.to_datetime("2025-07-01", format="%Y-%m-%d")
formatted_date_str = date_obj.strftime("%Y-%m-%d")
# %Y year
# %m month
# %d day
# %H hour
# %M minute
# %S second
# %z timezone
date_obj = pd.to_datetime("2025-06-01 14:30:00+0000", format="%Y-%m-%d %H:%M:%S%z")

# ------------------------------------------------------------------------------
# PARSING DATETIME
DATE_FORMAT = "%Y%B%d"
print(df["reference_period"].dtype) # check type like this
# Timestamp & datetime
pd.to_datetime("2025November15", format="%Y%B%d") # returns Timestamp('2025-11-15 00:00:00')
df["reference_period"] = pd.to_datetime(df["reference_period"], format=DATE_FORMAT) # by default returns datetime64[ns]
# changing precision
df["reference_period"] = pd.to_datetime(df["reference_period"], format=DATE_FORMAT).astype("datetime64[us]") # can immediately convert to us from ns
# changing both precision & timezone
df["reference_period"] = pd.to_datetime(df["reference_period"], format=DATE_FORMAT).astype("datetime64[us, America/New_York]") # WRONG (cant parse naive dt to timezone aware dt)
df["reference_period"] = pd.to_datetime(df["reference_period"], format=DATE_FORMAT).tz_localize("America/New_York").astype("datetime64[us, Amnerica/New_York]") # CORRECT 
# * note that datetime64[ns] is a type for Series (like entire col)
# * note that Timestamp is a type for Scalar (like entire col)

# ------------------------------------------------------------------------------
# FINDING HEADERS (finding rows that contain list of strings in its cells)
# iterating through rows to find the row which contains all columns you want
want_cols = ["col_name_1", "col_name_2", "col_name_3"]
# vectorized
def _find_headers_vectorized(df: pd.DataFrame) -> int:
    """
    finds the row with call the wanted cols
    """
    norm_df = df.applymap(lambda x: str(x).strip().lower())
    want = [s.strip().lower() for s in want_cols]

    # For each row, check if it contains all want_cols values
    mask = norm_df.apply(lambda row: all(col in row.values for col in want), axis=1) # ax

    if mask.any():
        idx = mask.idxmax()  # get first True index
        return idx, df.loc[idx]
    return -1

# ------------------------------------------------------------------------------
# RENAMING HEADERS/ COLUMNS
typos={
    "typo_1": "renamed_1",
    "typo_2": "renamed_2",
    "typo_3": "renamed_3",
}
df = df.rename(columns=typos)

# ------------------------------------------------------------------------------
# Series accessors
df["some_col"].astype(str).str.lower() # is a series accessor! => so it doesnt work with the entire DF

# ------------------------------------------------------------------------------
# PARSING DATETIME
DATE_FORMAT = "%Y%B%d"
print(df["reference_period"].dtype) # check type like this
# Timestamp & datetime
pd.to_datetime("2025November15", format="%Y%B%d") # returns Timestamp('2025-11-15 00:00:00')
df["reference_period"] = pd.to_datetime(df["reference_period"], format=DATE_FORMAT) # by default returns datetime64[ns]
# changing precision
df["reference_period"] = pd.to_datetime(df["reference_period"], format=DATE_FORMAT).astype("datetime64[us]") # can immediately convert to us from ns
# changing both precision & timezone
df["reference_period"] = pd.to_datetime(df["reference_period"], format=DATE_FORMAT).astype("datetime64[us, America/New_York]") # WRONG (cant parse naive dt to timezone aware dt)
df["reference_period"] = pd.to_datetime(df["reference_period"], format=DATE_FORMAT).tz_localize("America/New_York").astype("datetime64[us, Amnerica/New_York]") # CORRECT 
# * note that datetime64[ns] is a type for Series (like entire col)
# * note that Timestamp is a type for Scalar (like entire col)

# ------------------------------------------------------------------------------
# PYARROW CONVERSION FROM PANDAS
# float64 -> double
# datetime64[ns] -> timestamp[ns]
# datetime64[ns,tz] -> timestamp[ns, tz]
# object containing datetime.date -> date32 => in panddas there is no nastivce date type (just let the pandas do the natural date conversion LOL)