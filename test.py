

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




# get the binomial probabilities and their variace by position and time clusters
null = spider_lib.analyze_position_time_clusters(df=week_records_df)
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
