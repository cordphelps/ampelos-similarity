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

for transect in unique_transects:

   for week in unique_weeks: 

        for time in unique_times:

            filtered_df = pd.DataFrame()

            #  !!!!!!!  'f' is curly brace support !!!!!!!
            filtered_df = df.query( f" transect == '{transect}' and week == '{week}' and time == '{time}' ")

#print(">>>>>>>>>>>>>>>> filtered df >>>>>>>>>>>>>.")
#print(filtered_df)
#print(">>>>>>>>>>>>>>>> end filtered df >>>>>>>>>>>>>.")

#      transect    time week julian delimeter p0 p1 p2 p3 p4 p5 p6 p7 p8 p9
# 115  oakMargin   pm   23    158           :  1  3  1  2  0  0  1  2  2  3
# 119  oakMargin   pm   23    157           :  0  0  1  1  3  0  1  0  1  0
# 121  oakMargin   pm   23    156           :  0  0  0  0  2  0  1  1  1  0

# create a list of text strings from the available dataframe records
corpus_df = spider_lib.corpus_text_df(compressed_df=filtered_df)




#print("::::::::::::::::::::::corpus_list::::::::::::::::::::::::::")
#print(corpus_text_list)
#print("::::::::::::::::::::::corpus_list::::::::::::::::::::::::::")

# ['oakMargin pm 23 156 : 0 0 0 0 2 0 1 1 1 0', 
#  'control pm 23 156 : 0 0 1 0 1 0 1 1 0 2', 
#  'oakMargin pm 23 157 : 0 0 1 1 3 0 1 0 1 0', 
#  'oakMargin am 23 157 : 0 1 0 0 0 0 2 0 0 0', 
#  'control pm 23 157 : 0 0 1 4 0 2 2 1 0 1', 
#  'control am 23 157 : 0 0 1 0 0 0 0 2 0 0', 


for k in range(len(corpus_text_list)):
    #print("sending k=", k)
    #print(corpus_text_list[k])

    # convert the corpus into a context string and a sentence composed of 4 encoded words
    # representing TRUE/FALSE spider counts in each of the 3 kmeans() position groups
    # sending k sentences : '163 am 24 oakMargin : 2 1 1 0 1 0 2 1 0 0' 
    corpus_text_list[k] = spider_lib.row_text_to_three_words(corpus_text_list[k])
    # receiving : # k list elements, the context string and a sentance containing the 4 encoded words 


#print("::::::::::::::::::::::corpus_list k ::::::::::::::::::::::::::")
#print(corpus_text_list[k])
#print("::::::::::::::::::::::corpus_list k ::::::::::::::::::::::::::")

# ['control am 34 236 ', 'falsefalsefalse falsefalsefalse falsefalsefalse false']

####################################################
# compare oakMargin to control for each day and time
####################################################

# convert the text into a dataFrame
from io import StringIO  # allows treating text as a file-like object
df = pd.read_csv(StringIO(data), sep='\s+', header=None)
# Assign column names (optional)
df.columns = ['Name', 'Profession', 'Salary']






# trigger the compare "oakMargin to control" logic (raw == FALSE)
# stacked_similarity() is designed to compare oakMargin records to matching control transect
# records based on an assumption of how the corpus is assembled
# 
df = thad_o_mizer.stacked_similarity(corpus=corpus_text_list, raw=False)

# print(df)

#    BOW cosine similarity  levenshtein distance  ...            sentence1           sentence2
# 0               0.970918                     3  ...  162 am 24 oakMargin   162 am 24 control 
# 1               0.944152                     3  ...  163 am 24 oakMargin   163 am 24 control 
# 2               0.946856                     2  ...  164 am 24 oakMargin   164 am 24 control 

# [3 rows x 8 columns]


filename = './metrics/transect-compare-' + 'week-24-' + 'am.csv'

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












