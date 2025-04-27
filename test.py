

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

# erase any existing variance csv
import os 
filename = './metrics/count-variance.csv'
if os.path.exists(filename):
    os.remove(filename)
# Create an empty DataFrame and csv
df = pd.DataFrame(columns=['transect', 'time', 'data_label', 'count', 'mean', 'variance'])
df.to_csv(filename, index=False)

# partition data by position 1-4 ; 5-7 ; 8-10

group1_df = spider_lib.chopPosition(df=week_records_df, position_list=['1', '2', '3', '4'])
hoser = spider_lib.central_limit(both_transects_dataframe=group1_df, daytime=time, file_label='_1to4_')

group2_df = spider_lib.chopPosition(df=week_records_df, position_list=['5', '6', '7'])
hoser = spider_lib.central_limit(both_transects_dataframe=group2_df, daytime=time, file_label='_5to7_')

group3_df = spider_lib.chopPosition(df=week_records_df, position_list=['8', '9', '10'])
hoser = spider_lib.central_limit(both_transects_dataframe=group3_df, daytime=time, file_label='_8to10_')

# partition data by position 1-4 ; 5-7 ; 8-10

group1_df = spider_lib.chopPosition(df=week_records_df, position_list=['1', '2', '3', '4'])
group1_df_week1 = spider_lib.chopWeek(df=group1_df, week_list=['23', '24', '25'])
hoser = spider_lib.central_limit(both_transects_dataframe=group1_df_week1, daytime=time, file_label='_1to4_23to25')

group2_df = spider_lib.chopPosition(df=week_records_df, position_list=['5', '6', '7'])
group2_df_week2 = spider_lib.chopWeek(df=group2_df, week_list=['26', '27', '28', '29', '30', '31'])
hoser = spider_lib.central_limit(both_transects_dataframe=group2_df_week2, daytime=time, file_label='_5to7_26to31')

group3_df = spider_lib.chopPosition(df=week_records_df, position_list=['8', '9', '10'])
group3_df_week3 = spider_lib.chopWeek(df=group3_df, week_list=['32', '33', '34'])
hoser = spider_lib.central_limit(both_transects_dataframe=group3_df_week3, daytime=time, file_label='_8to10_32to34')

print("csv written")
sys.exit(1)



posterior_result = spider_lib.negative_binomial(number_independent_trials=10, number_of_successes=3, csv_ID='hoser')

print('results:   Posterior median: %.3f, Posterior quantile interval: %.3f-%.3f' % 
          (posterior_result[0], posterior_result[1], posterior_result[2]))


print("week total written")
sys.exit(1)



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
