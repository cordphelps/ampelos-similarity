

# looking at geombox plot, maybe the amont of wind, one transect to another , has a sppressive effect on the 
# appearance or migration of the spiders.



import requests
import csv 
import io
import sys
import pandas as pd 

import spider_lib 
import thad_o_mizer

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

week_records_df = spider_lib.rough_dataset_clean(df)

time = 'pm'

# get the relative frequencies by count

hoser = spider_lib.central_limit(both_transects_dataframe=week_records_df, daytime=time, file_label='_1to10_')

# ^^^^^^^^^^^^^ MCMC analysis in ngram.Rmd ^^^^^^^^^^^^^

# partition data by position 1-4 ; 5-7 ; 8-10

group1_df = spider_lib.chop(df=week_records_df, position_list=['1', '2', '3', '4'])
hoser = spider_lib.central_limit(both_transects_dataframe=group1_df, daytime=time, file_label='_1to4_')

group2_df = spider_lib.chop(df=week_records_df, position_list=['5', '6', '7'])
hoser = spider_lib.central_limit(both_transects_dataframe=group2_df, daytime=time, file_label='_5to7_')

group3_df = spider_lib.chop(df=week_records_df, position_list=['8', '9', '10'])
hoser = spider_lib.central_limit(both_transects_dataframe=group3_df, daytime=time, file_label='_8to10_')

# now segment by week.................


print("csv written")
sys.exit(1)

#print(">>>>>>>>>>>>>>>> week_records_df df >>>>>>>>>>>>>.")
#print(week_records_df)
#print(">>>>>>>>>>>>>>>> end week_records_df df >>>>>>>>>>>>>.")

julian = '193'
transect = 'oakMargin'
time = 'pm'

#filtered_df = week_records_df.query( f" transect == '{transect}' and julian == '{julian}' and time == '{time}' ")

#print(filtered_df.to_string())
#print("to_string done")
#sys.exit()

#df = spider_lib.julian_row_compare_alternate(filtered_df)
df = spider_lib.julian_row_compare_alternate(week_records_df)
