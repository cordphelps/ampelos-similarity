




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


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# get the binomial probabilities and their variance by position and time clusters
# uses central_limit() *raw and normalized counts* + csv_probability_variance() 
# plus files recording probability by vineyard position
#           './metrics/control_df-' + daytime + file_label + '-raw_count-.csv'
#           './metrics/control_df-' + daytime + file_label + '-prob-.csv'
#
null = spider_lib.analyze_position_time_clusters(df=week_records_df)
print("csv written")
sys.exit(1)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# get posterior distributions by cluster to eventually compare the credible intervals (in R)
#
# get binomial position counts by row calculate NGRAM similarity
# return two dataframes :  
#    (filename = './metrics/row_binomial_success.csv') transect time week julian row  nonZero
#    (filename = './metrics/row_NGRAM.csv') transect, week, julian, time, row1_to_row2, row1_to_row3, row2_to_row3
df_list = spider_lib.julian_row_compare_alternate(week_records_df)

# for each weekly cluster, calculate "success" and "trials"
df = spider_lib.binomial_success_week(df_list[0])

# for each transect / time / week_cluster
# calculate total trials and successes
# pipe to binomial() to save the posterior distribution to csv
#     - use R to create distribution graphics
#     - package coda: HPD/HDI interval: Narrowest interval containing the specified 
#       probability mass (better for skewed posteriors)
#     - calculate a credible interval for the success probability mean
# 
df = spider_lib.binomial_credible_interval(df, graphics="False", csv_ID='hoser')
# now compare credible intervals in R

#
print("compare_alternate")
sys.exit(1)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^






#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

week_df = spider_lib.weekly_spider_count(df=week_records_df)

print("week total written")
sys.exit(1)


#print(">>>>>>>>>>>>>>>> week_records_df df >>>>>>>>>>>>>.")
#print(week_records_df)
#print(">>>>>>>>>>>>>>>> end week_records_df df >>>>>>>>>>>>>.")

julian = '193'
week='34'
transect = 'oakMargin'
time = 'am'

filtered_df = week_records_df.query( f" transect == '{transect}' and week == '{week}' and time == '{time}' ")

print(filtered_df)
print("to_string done")
sys.exit(1)

#df = spider_lib.julian_row_compare_alternate(filtered_df)
df = spider_lib.julian_row_compare_alternate(week_records_df)
