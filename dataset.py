import requests
import csv 
import io
import sys
import pandas as pd 

import spider_lib 
import thad_o_mizer

import test_sentences

from datetime import datetime
timestamp = datetime.now()
formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
print("::::::::::::::::::::::::::::::::::::::::::::::::")
print("::::::::::::::::::::::::", formatted_timestamp, "::::::::::::::::::::::::")
print("::::::::::::::::::::::::::::::::::::::::::::::::")




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

#print(">>>>>>>>>>>>>>>> week_records_df df >>>>>>>>>>>>>.")
#print(week_records_df)
#print(">>>>>>>>>>>>>>>> end week_records_df df >>>>>>>>>>>>>.")

#>>>>>>>>>>>>>>>> week_records_df df >>>>>>>>>>>>>.
#0      transect row time week julian Thomisidae (crab spider) position
#1     oakMargin  79   pm   23    156                        0        1
#2     oakMargin  79   pm   23    156                        0        2
#3     oakMargin  79   pm   23    156                        0        3
#4     oakMargin  79   pm   23    156                        0        4
#5     oakMargin  79   pm   23    156                        0        5
#...         ...  ..  ...  ...    ...                      ...      ...
#3716    control  53   am   34    236                        0        6
#3717    control  53   am   34    236                        0        7
#3718    control  53   am   34    236                        0        8
#3719    control  53   am   34    236                        0        9
#3720    control  53   am   34    236                        0       10

#[3720 rows x 7 columns]
#>>>>>>>>>>>>>>>> end week_records_df df >>>>>>>>>>>>>.


# compress the daily counts by row into daily total counts (add counts by position)
df = spider_lib.daily_spider_count(df=week_records_df)

# print(">>>>>>>>>>>>>>>> daily_spider_count df >>>>>>>>>>>>>>>>>>>>>>>>>>>.")
# print(">>>>>>>>>>>>>>>> 32 days, 2 times, 2 transects = 128 >>>>>>>>>>>>>.")
# print(df)
# print(">>>>>>>>>>>>>>>> end daily_spider_count df >>>>>>>>>>>>>.")

#       transect time week julian delimeter p0 p1 p2 p3 p4 p5 p6 p7 p8 p9
# 0      control   am   34    236         :  0  0  0  0  0  0  0  0  0  0
# 1      control   pm   34    236         :  0  0  0  0  0  0  0  0  1  1
# 2    oakMargin   am   34    236         :  0  0  0  0  0  0  0  0  0  0
# 3    oakMargin   pm   34    236         :  0  0  0  0  0  0  0  0  0  0
# 4      control   am   34    235         :  0  0  0  0  0  0  0  0  0  0
# ..         ...  ...  ...    ...       ... .. .. .. .. .. .. .. .. .. ..
# 117    control   pm   23    157         :  0  0  1  4  0  2  2  1  0  1
# 118  oakMargin   am   23    157         :  0  1  0  0  0  0  2  0  0  0
# 119  oakMargin   pm   23    157         :  0  0  1  1  3  0  1  0  1  0
# 120    control   pm   23    156         :  0  0  1  0  1  0  1  1  0  2
# 121  oakMargin   pm   23    156         :  0  0  0  0  2  0  1  1  1  0
# 
# [122 rows x 15 columns]



# compare the samples from the same transect, time, and day 
# 

unique_transects = df['transect'].unique()
unique_weeks = df['week'].unique()

unique_times = df['time'].unique()

transect_df = pd.DataFrame(columns=df.columns)

for transect in unique_transects:

    week_df = pd.DataFrame(columns=df.columns)

    for week in unique_weeks: 

        time_df = pd.DataFrame(columns=df.columns)

        for time in unique_times:

            filtered_df = pd.DataFrame()

            #  !!!!!!!  'f' is curly brace support !!!!!!!
            filtered_df = df.query( f" transect == '{transect}' and week == '{week}' and time == '{time}' ")

            # merge the dataframes by stacking rows (default behavior of concat)
            time_df = pd.concat([time_df, filtered_df], ignore_index=True)

        #print("****************** time_df ****should be time by week********************")
        #print(time_df)

        week_df = pd.concat([week_df, time_df], ignore_index=True)
    #print("****************** week_df ************************")
    #print(week_df)

    transect_df = pd.concat([transect_df, week_df], ignore_index=True)
#print("****************** transect_df ************************")
#print(transect_df)

filtered_df = transect_df

#print(">>>>>>>>>>>>>>>> filtered df >>>>>>>>>>>>>.")
#print(filtered_df)
#print(">>>>>>>>>>>>>>>> end filtered df >>>>>>>>>>>>>.")

#       transect time week julian delimeter p0 p1 p2 p3 p4 p5 p6 p7 p8 p9
# 0      control   am   34    236         :  0  0  0  0  0  0  0  0  0  0
# 1      control   am   34    235         :  0  0  0  0  0  0  0  0  0  0
# 2      control   am   34    234         :  0  0  0  0  0  0  0  0  1  0
# 3      control   pm   34    236         :  0  0  0  0  0  0  0  0  1  1
# 4      control   pm   34    235         :  0  1  0  0  0  0  0  0  0  0
# ..         ...  ...  ...    ...       ... .. .. .. .. .. .. .. .. .. ..
# 117  oakMargin   am   23    158         :  1  2  0  0  0  0  2  0  0  1
# 118  oakMargin   am   23    157         :  0  1  0  0  0  0  2  0  0  0
# 119  oakMargin   pm   23    158         :  1  3  1  2  0  0  1  2  2  3
# 120  oakMargin   pm   23    157         :  0  0  1  1  3  0  1  0  1  0
# 121  oakMargin   pm   23    156         :  0  0  0  0  2  0  1  1  1  0
# 
# [122 rows x 15 columns]


# create a list of text strings from the available dataframe records
corpus_df = spider_lib.corpus_text_df(compressed_df=filtered_df)


#       transect time  ...    squashed                                        transformed
# 115  oakMargin   pm  ...  1312001223      TRUETRUETRUE TRUEfalsefalse TRUETRUETRUE TRUE
# 119  oakMargin   pm  ...  0011301010   falsefalseTRUE TRUETRUEfalse TRUEfalseTRUE false
# 121  oakMargin   pm  ...  0000201110  falsefalsefalse falseTRUEfalse TRUETRUETRUE false


####################################################
# compare oakMargin to control for each day and time
####################################################



# trigger the compare "oakMargin to control" logic (raw == FALSE)
# stacked_df_similarity() is designed to compare oakMargin records to matching control transect
# records 
# 

df = thad_o_mizer.stacked_df_similarity(df=corpus_df, raw=False)

#print(df)

#    julian time  NGRAM cosine similarity  flip NGRAM CS levenshtein_distance LD flip
# 0     236   am                 1.000000       1.000000                    0       0
# 1     236   pm                 0.656250       0.656250                    2       2
# 2     235   am                 1.000000       1.000000                    0       0
# 3     235   pm                 0.813559       0.813559                    1       1
# 4     234   am                 0.813559       0.813559                    1       1
# 5     234   pm                 0.813559       0.813559                    1       1
# 6     220   am                 0.813559       0.813559                    1       1
# ...
# 52    163   am                 0.614035       0.614035                    3       3
# 53    163   pm                 0.780000       0.780000                    1       1
# 54    162   am                 0.920000       0.920000                    3       3
# 55    162   pm                 0.716981       0.716981                    2       2
# 56    158   am                 0.580645       0.580645                    3       3
# 57    158   pm                 0.784314       0.784314                    1       1
# 58    157   am                 0.890909       0.890909                    2       2
# 59    157   pm                 0.796296       0.796296                    3       3



filename = './metrics/transect-compare-.csv'

# mode='w' indicates 'overwrite'
df.to_csv(filename, header=True, index=True, mode='w')




######################################################################################################

# now compare the row similarity in a dataset 
# optional: pre-filter for a specific transect / week / time

######################################################################################################



# Convert DataFrame to a list of lists
all_records_list = week_records_df.values.tolist()

#print(">>>>>>>>>>>>>>>>>>>>>>>.all records list>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#print(all_records_list)
#print(bugs_list)
#print(">>>>>>>>>>>>>>>>>>>>>>>.all records list>>>>>>>>>>>>>>>>>>>>>>>>>>>")


# filename = './metrics/control-' + 'week-24-' + 'am.csv'
filename = './metrics/row-compare.csv'

columns = ['BOW cosine similarity', 'levenshtein distance', 
    'NGRAM cosine similarity', 'BPW flip', 'LD flip', 'NGRAM flip', 'data ID 1', 'data ID 2']
# Create an empty DataFrame with the specified columns
empty_df = pd.DataFrame(columns=columns)
# create csv (overwite if it exists)
empty_df.to_csv(filename, index=True)

# mode='w' indicates 'overwrite'
#df.to_csv(filename, header=True, index=True, mode='w')

# get a list of weeks 
unique_weeks_list = week_records_df['week'].unique()

print(">>>>>>>>>>>>>>>>>>>>>>>.unique_weeks_list>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(unique_weeks_list)
#print(bugs_list)
print(">>>>>>>>>>>>>>>>>>>>>>>.unique_weeks_list>>>>>>>>>>>>>>>>>>>>>>>>>>>")


for k in range(len(unique_weeks_list)):

    df = spider_lib.TWT_row_similarity(records_list=all_records_list, transect='oakMargin', week=k, time='am')

    df.to_csv(filename, header=False, index=True, mode='a')












