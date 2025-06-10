




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

week_records_df = spider_lib.rough_dataset_clean(df)

######################################################################
#   transect    row    time    week    julian    thomisidae crab spider   position
#
######################################################################

import os
filename = './data/bugs.by.position.csv'
if os.path.exists(filename):
    os.remove(filename)
week_records_df.to_csv(filename, header=True, index=False, mode='w')

# Great observation! If `.describe()` returns `'object'` as the dtype for your column, 
#that means pandas is treating `'Thomisidae (crab spider)'` as a string/object column, 
#not as numeric. This is common if the column was read from a CSV or Excel file and contains 
#any non-numeric entries, missing values, or even just because pandas couldn’t infer the type.

week_records_df['Thomisidae (crab spider)'] = pd.to_numeric(
    week_records_df['Thomisidae (crab spider)'], errors='coerce'
)
week_records_df['position'] = week_records_df['position'].astype("string")
week_records_df['week'] = week_records_df['week'].astype("string")


#print(week_records_df.to_string())

#   warnings.warn(
#   0      transect row time week julian  Thomisidae (crab spider) position
#   1     oakMargin  79   pm   23    156                         0        1
#   2     oakMargin  79   pm   23    156                         0        2
#   3     oakMargin  79   pm   23    156                         0        3
#   4     oakMargin  79   pm   23    156                         0        4
#   5     oakMargin  79   pm   23    156                         0        5
#   6     oakMargin  79   pm   23    156                         0        6
#   7     oakMargin  79   pm   23    156                         1        7
#   8     oakMargin  79   pm   23    156                         0        8
#   9     oakMargin  79   pm   23    156                         1        9
#   10    oakMargin  79   pm   23    156                         0       10



######################################################################
# compare SI and NGRAM indecies

success_probability = 0.5   
ngram_width = 4

spider_lib.buildIndexComparitor(sp = success_probability, ng = ngram_width)

# creates filename = './metrics/sorensen_combined.csv'
# see chunk sorensen_correlation in ngram.Rmd

exit(1)


######################################################################
########################################################################
#
# get position counts by week 
# 
#

wc_df = spider_lib.week_compare_counts(df=week_records_df)


    # ==============================================================
    # read by the chunk bug-wilcoxonSRT in wilcoxcon.anova.Rmd
    # ==============================================================

    # that is columns for each transect/time/week/row and rows of summed position
    # filename = './metrics/counts_week.csv'

    # print(wc_df.iloc[:, 0].to_string())

     #    oakMargin.pm.23.79 oakMargin.pm.23.81 oakMargin.pm.23.83
     #                 <int>              <int>              <int>
     #  1                  0                  1                  0
     #  2                  0                  0                  3
     #  3                  1                  0                  2
     #  4                  1                  0                  1
     #  5                  0                  3                  0
     #  6                  2                  2                  1
     #  7                  0                  0                  0
     #  8                  3                  0                  0
     #  9                  2                  1                  0
     # 10                  2                  1                  1



exit(1)




######################################################################
# find clusters
# build
#     # > head(total.df, 10)                          <-- 372 rows
#    #   week  transect time trap-position 1 : 10 
#    #1    23 oakMargin   am   each:totalSpiders
#    #2    23 oakMargin   am   each:totalSpiders
#
#   # return a list of the clusters occurring in the dataset
# 
#    #   week  transect time trap-position 1 : 10 
#    #1    23 oakMargin   am   each:clusterID
#    #2    23 oakMargin   am   each:clusterID


spider_lib.kmeans_clusters(df=week_records_df)

exit(1)




########################################################################
#
# assess the species composition of both transects
# and calculate the Sorensen Index of similarity
# (used by Daane/Hogg 2010)
# since it uses incidence of species to compare
# samples, and is insensitive to changes in species abundances.

spider_lib.sorensenIndex(df=df)



# get NGRAMS to compare row triplets in transect/daytime pairs
# write

df_list = list() 



########################################################################
#
# get binomial position pattern by row for each julian/time/transect
# calculate NGRAM similarity between transects
# save the NGRAM computation to disk
# (in R) compare spider count text similarity between transects by julian day and time
# compare across transects, save filename = './metrics/NGRAM_transect.csv'
#

#spider_lib.julian_row_compare_transect()
#exit(1)



# =======================================================================================
# save binomial success count to filename = './metrics/binomial_nonZero_counts_row.csv'
# save binomial success by postion to ilename = './metrics/binomial_position_success.csv'
# compare same-transect true/false position strings for 3 same julian rows 
#         save filename = './metrics/binomial_NGRAM_local.csv'
#
df_list = spider_lib.julian_row_compare_alternate(week_records_df)


# print(df_list[0])
# print("that was 0 \n")
#       transect time week julian row nonZero
# 0    oakMargin   pm   23    156  79       2
# 1    oakMargin   pm   23    156  81       2
# 2    oakMargin   pm   23    156  83       1
# 3      control   pm   23    156  48       2
# 4      control   pm   23    156  50       2
# ..         ...  ...  ...    ...  ..     ...
# 361    control   pm   34    236  51       1
# 362    control   pm   34    236  53       1
# 363    control   am   34    236  49       0
# 364    control   am   34    236  51       0
# 365    control   am   34    236  53       0
# 
# [366 rows x 6 columns]

#print(df_list[1])
#print("that was 1 \n")
#       transect julian time week  ...           row_c_text row1_row2 row1_row3  row2_row3
# 0    oakMargin    156   pm   23  ...  f f f f T f f f f f   1.000000  0.703704  0.703704
# 1      control    156   pm   23  ...  f f f f T f f f f f   0.703704  0.703704  0.840000
# 2    oakMargin    157   pm   23  ...  f f T f f f f f f f   0.840000  0.703704  0.586207
# 3    oakMargin    157   am   23  ...  f f f f f f f f f f   0.703704  0.483871  0.703704
# 4      control    157   pm   23  ...  f f f T f T f f f T   0.703704  0.586207  0.703704
# ..         ...    ...  ...  ...  ...                   ...       ...       ...       ...
# 115    control    235   am   34  ...  f f f f f f f f f f   1.000000  1.000000  1.000000
# 116  oakMargin    236   pm   34  ...  f f f f f f f f f f   1.000000  1.000000  1.000000
# 117  oakMargin    236   am   34  ...  f f f f f f f f f f   1.000000  1.000000  1.000000
# 118    control    236   pm   34  ...  f f f f f f f f f T   0.703704  0.703704  0.703704
# 119    control    236   am   34  ...  f f f f f f f f f f   1.000000  1.000000  1.000000
# 
# [120 rows x 10 columns]

sys.exit(1)


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# get posterior distributions by cluster to eventually compare the credible intervals (in R)
#
# get binomial position counts by row calculate NGRAM similarity
# return two dataframes and write
#
#           filename = './metrics/binomial_success_row.csv' transect time week julian row  nonZero
#           filename = './metrics/NGRAM_row.csv' transect, week, julian, time, row1_to_row2, row1_to_row3, row2_to_row3
#
df_list = spider_lib.julian_row_compare_alternate(week_records_df)


# for each weekly cluster, calculate "success" and "trials"
df = spider_lib.binomial_success_week(df_list[0])


# for each transect / time / week_cluster
# calculate total trials and successes
# pipe to binomial() and save the posterior distribution to csv
#     - use R to create distribution graphics
#     - package coda: HPD/HDI interval: Narrowest interval containing the specified 
#       probability mass (better for skewed posteriors)
#     - calculate a credible interval for the success probability mean
# 
df = spider_lib.binomial_credible_interval(df, graphics="False", csv_ID='hoser')
# now compare credible intervals in R

#
print("compare_alternate done")



# get the binomial probabilities and their variance by position and time clusters
# variance graphics in R chunk 'makeVariance'

null = spider_lib.analyze_position_time_clusters(df=week_records_df)

#
# # write file to record trials count mean  variance
#  filename = './metrics/cluster-probability-variance.csv' :

# 0   oakMargin   am    -w1-p1-      96     25  0.260417  0.255100
# 1   oakMargin   pm    -w1-p1-     108     48  0.444444  0.617284
# 2     control   am    -w1-p1-      96     24  0.250000  0.229167
# 3     control   pm    -w1-p1-     108     45  0.416667  0.631944
# 4   oakMargin   am    -w1-p2-      72     33  0.458333  0.553819
# 5   oakMargin   pm    -w1-p2-      81     32  0.395062  0.436519
# 6     control   am    -w1-p2-      72     11  0.152778  0.157215
# 7     control   pm    -w1-p2-      81     55  0.679012  0.835239
# 8   oakMargin   am    -w1-p3-      72     20  0.277778  0.339506
# 9   oakMargin   pm    -w1-p3-      81     42  0.518519  0.817558
# 10    control   am    -w1-p3-      72     27  0.375000  0.595486

print("csv written")
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


