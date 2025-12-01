# this includes common methods & custom functions to parse pandas dataframes

import pandas as pd

# FINDING HEADERS
# RENAMING HEADERS/ COLUMNS
# Series accessors
# PARSING DATETIME

df = pd.DataFrame()
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