import requests
import csv 
import io
import sys
import pandas 

import spider_lib 
import thad_o_mizer

import test_sentences


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
week_records_df = spider_lib.rough_dataset_clean(records_list=bugs_list, transect='oakMargin', week='24', time='am')

# print(week_records_df)
# 0     transect row time week julian Thomisidae (crab spider) position
# 391  oakMargin  80   am   24    162                        0        1
# 392  oakMargin  80   am   24    162                        1        2
# 393  oakMargin  80   am   24    162                        1        3
# 394  oakMargin  80   am   24    162                        0        4
# 395  oakMargin  80   am   24    162                        0        5
# ..         ...  ..  ...  ...    ...                      ...      ...
# 596  oakMargin  84   am   24    164                        0        6
# 597  oakMargin  84   am   24    164                        1        7
# 598  oakMargin  84   am   24    164                        2        8
# 599  oakMargin  84   am   24    164                        0        9
# 600  oakMargin  84   am   24    164                        1       10
# 
# [90 rows x 7 columns]

# trim dataframe by julian day
#df = week_records_df.query(" julian == '162' ")
#print(df)

# compress the daily counts by row into daily total counts (add counts by position)
df = spider_lib.daily_spider_count(df=week_records_df)

# print(df)
#   julian time week   transect p0 p1 p2 p3 p4 p5 p6 p7 p8 p9
# 0    164   am   24  oakMargin  2  2  2  3  1  1  4  4  0  2
# 1    163   am   24  oakMargin  1  1  0  1  2  3  6  1  1  2
# 2    162   am   24  oakMargin  2  1  1  0  1  0  2  1  0  0


# pop the result onto bug_count_df_list[] 
bug_count_df_list.insert(0, df)

# repeat as necessary (add data for another transect, week, and time)
# ------------------------------------------------------------------------------
week_records_df = spider_lib.rough_dataset_clean(records_list=bugs_list, 
                                                transect='control', 
                                                week='24', 
                                                time='am')
df = spider_lib.daily_spider_count(df=week_records_df)
# merge the dataframes
bug_count_df_list.insert(0, df)
# ------------------------------------------------------------------------------

# create a list of text strings from the available dataframe records
corpus_text_list = spider_lib.df_to_corpus_text(df_list=bug_count_df_list)
# print(corpus_list)
# ['162 am 24 oakMargin : 2 1 1 0 1 0 2 1 0 0', 
# '163 am 24 oakMargin : 1 1 0 1 2 3 6 1 1 2', 
# '164 am 24 oakMargin : 2 2 2 3 1 1 4 4 0 2', 
# '162 am 24 control : 1 0 1 1 1 0 0 1 1 0', 
# '163 am 24 control : 0 2 2 2 1 0 1 0 3 4', 
# '164 am 24 control : 2 0 1 2 1 2 0 2 5 2']

#single_sentence_text_list = spider_lib.text_to_words('162 am 24 oakMargin : 2 1 1 0 1 0 2 1 0 0')
#print(single_sentence_text_list)

#result = spider_lib.create_embedding_model(corpus=corpus_list)
#print(result)
# -------------- prior to using torch --------------

# workbench to play with s1 and s2
# result = test_sentences.s1_s2()
# s1 = result[0]
# s2 = result[1]
# print(s1, s2)


for k in range(len(corpus_text_list)):
    #print("sending k=", k)
    #print(corpus_text_list[k])

    # convert the corpus into a context string and a sentence composed of 3 encoded words
    # representing TRUE/FALSE spider counts in each of the 3 kmeans() position groups
    # sending k sentences : '163 am 24 oakMargin : 2 1 1 0 1 0 2 1 0 0' 
    corpus_text_list[k] = spider_lib.row_text_to_three_words(corpus_text_list[k])
    # receiving : # k list elements, the context string and a sentance containing the 3 encoded words 


# get s1/s2 string array, s1/s2 similarity, s1/s2 distance array
# 
metrics_array = thad_o_mizer.make_similarity_arrays(corpus=corpus_text_list, raw=False)

print(metrics_array)



######################################################################################################

# now compare the row similarity in a specific transect for a specific week and time

######################################################################################################

metrics_array = spider_lib.row_similarity(records_list=bugs_list, transect='control', week='24', time='am')

# print("################ metrics_array from main ################")
# print(metrics_array)

# [[[0.9999999 0 1.0 0.9999999 0 1.0 '162 am 24 control '
#    '162 am 24 control ']
#   [0.98172927 2 0.7222222222222222 0.98172927 2 0.7222222222222222
#    '162 am 24 control ' '163 am 24 control ']
#   [0.96084946 2 0.6140350877192983 0.96084946 2 0.6140350877192983
#    '162 am 24 control ' '164 am 24 control ']]
# 
#  [[0.98172927 2 0.7222222222222222 0.98172927 2 0.7222222222222222
#    '163 am 24 control ' '162 am 24 control ']
#   [1.0 0 1.0 1.0 0 1.0 '163 am 24 control ' '163 am 24 control ']
#   [0.9757236 3 0.7169811320754716 0.9757236 3 0.7169811320754716
#    '163 am 24 control ' '164 am 24 control ']]


print("################ metrics_array from main ################")
######################################################################################################

# collect and store similarity metrics from individual weeks
# the intention is to assess the distribution of specific metrics to undersstand the 
# tolerances around "similarity""

######################################################################################################


# get similarity data across rows and kmeans() segments for one transect, one week, one time. 
# update datastore

# Flatten the first two dimensions into one
metrics2d_array = metrics_array.reshape(-1, metrics_array.shape[-1])
print(metrics2d_array)

filename = "metrics.csv"



import numpy as np

# Write the array to a CSV file
np.savetxt(filename, metrics2d_array, delimiter=",", fmt="%s", 
    header="cosine similarity (BOW),levenshtein distance,cosine similarity (NGRAM),BOW flip,LD flip,NGRAM flip,sentence 1,sentence 2")


# Read a CSV file into a NumPy array
array = np.genfromtxt(filename, delimiter=',', dtype=object)
# By default, `np.genfromtxt()` returns byte strings (`b'string'`). decode them using:
decoded_data = np.array([[cell.decode("utf-8") if isinstance(cell, bytes) else cell for cell in row] for row in array])
print("decoded_data type: ", type(decoded_data))
#print(local_disk_array)

# get some more metrics
metrics_array = spider_lib.row_similarity(records_list=bugs_list, transect='oakMargin', week='34', time='pm')
# Flatten the first two dimensions into one
metrics2d_array = metrics_array.reshape(-1, metrics_array.shape[-1])

# jam them together
metrics2d_array = np.concatenate((array, metrics2d_array), axis=0)
np.savetxt(filename, metrics2d_array, delimiter=",", fmt="%s", 
    header="cosine similarity (BOW),levenshtein distance,cosine similarity (NGRAM),BOW flip,LD flip,NGRAM flip,sentence 1,sentence 2")

















