

import requests
import csv 
import io
import sys
import pandas as pd 

import spider_lib 
import thad_o_mizer
from km_lib import km 

bug_count_df_list = []

# get the bugs data
url = 'https://raw.githubusercontent.com/cordphelps/ampelos/refs/heads/master/data/bugs.csv'
bugs_list = spider_lib.read_raw_bugs_data(url)

if bugs_list[0] == "error":
    # choke
    print("csv data not found, error code: ", bugs_list[2])
    sys.exit(1)  # graceful exit on error condition with cleanup

# get a dataframe of spider counts with specific columns
#
##### transect row time week julian Thomisidae (crab spider) position #####
# transect is either 'oakMargin' or 'control'
# row corresponds to row IDs from the ampelos vineyard where the samples were taken
# time is either 'am' or 'pm' indicating when the data was collected
# week represents the 'integer' week when the data was collected, range: 23-34 excluding 33
# julian represents the 'integer' day when the data was collected, range: 156-236
# Thomisidae (crab spider) is the count of spiders observed
# position represents sequential vine positions (at various spacings) sampled for spider counts, range: 1-10
#####
# 

# pandas list to df
df = pd.DataFrame(bugs_list)

import pandas as pd

# convert the list to dataframe
#df = pd.DataFrame(records_list)

# Set the first row as column headers
df.columns = df.iloc[0]  # Assign first row to columns
df = df.rename(columns=df.iloc[0]).iloc[1:]  # Remove the first row

omit_columns = ['transect', 'row', 'time', 'week', 'julian', 'position', 'date', 'positionX']

df_filtered = df.drop(columns=omit_columns)

# Step 1: Convert all columns to numeric where possible
df_numeric = df_filtered.apply(pd.to_numeric, errors='coerce')

# Step 1: Calculate column totals (ignoring NaN by default)
column_totals = df_numeric.sum()

# Step 2: Sort totals in descending order
ranked_totals = column_totals.sort_values(ascending=False)

for col, total in ranked_totals.items():
    print(f"{col}: {total}")


