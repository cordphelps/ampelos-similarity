def square(number):
    # Calculate the square of the input number
    return number * number

# Call the function with an input
#result = square(4)
#print(result)  # Output: 16

def makeSentance():


    return ten_position_list_txt

import requests
import csv 
import io

def read_raw_bugs_data(url):

    result_list = []
    
    # get the bugs data

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
    
        csv_data = response.text

        # Use csv.reader to read the CSV data
        # Use io.StringIO to convert the bytes to a string
        records = []
        reader = csv.reader(io.StringIO(csv_data), delimiter=',')
    
        for row in reader:
            if row:  # Ensure the row is not empty
                records.append(row)

        result_list = records
        
    else:
        # print(f"Failed to retrieve data: {response.status_code}")

        result_list = ["error", "Failed to retrieve data", response.status_code]

    return(result_list)


def rough_dataset_clean(df):

    ##########################################################################################
    # return a df of spider counts for all positions and all rows of a specific transect, week and time
    #
    # 
    ##########################################################################################


    import pandas as pd

    # convert the list to dataframe
    #df = pd.DataFrame(records_list)

    # Set the first row as column headers
    df.columns = df.iloc[0]  # Assign first row to columns
    df = df.rename(columns=df.iloc[0]).iloc[1:]  # Remove the first row

    #The `.loc[]` method allows you to select rows and columns by labels. 
    #To select specific columns, use `:` for all rows and specify the column names.
    selected_columns_df = df.loc[:, ['transect', 'row', 'time', 'week', 'julian', 'Thomisidae (crab spider)', 'position']]

    return(selected_columns_df)


def daily_spider_count(df):

    ########################################################################
    #
    # sum spider counts by julian day
    # input can mix records for 'transect', 'week', and 'time'. 
    # 
    # return a dataframe with text identifiers, a delimeter, and the totalized count by position
    ########################################################################

    import pandas as pd
    
    unique_weeks = df['week'].unique()
    unique_time = df['time'].unique()

    #if len(unique_weeks) != 1:
        # choke
        #print("daily_spider_count(): the input dataframe must contain data from only 1 week")
        #sys.exit(1)  # graceful exit on error condition with cleanup
    #if len(unique_time) != 1:
        # choke
        #print("daily_spider_count(): the input dataframe must contain data from only 1 time")
        #sys.exit(1)  # graceful exit on error condition with cleanup

    # prep a list of lists to load a dataframe for return
    list_holding_tank = []

    # without specifying the specific vineyard rows sampled, we can sum the spider counts
    # by row for each day for the week and time represented in the dataframe

    # create records that represent the number of spiders occurring in sequential positions
    # read each record, examine the position, and place the spider count for that position in 
    # the matching column. Then we have ordered sequences of counts (that represent a pattern)

    # for each julian day, there are 3 rows that were sampled
    
    #unique_julian_list = df['julian'].unique().tolist()
    #unique_time_list = df['time'].unique().tolist()
    #unique_transect_list = df['transect'].unique().tolist()
    #unique_week_list = df['week'].unique().tolist()


    unique_julian = df['julian'].unique()
    unique_time = df['time'].unique()
    unique_transect = df['transect'].unique()
    unique_week = df['week'].unique()

    #print(unique_time)
    #print(unique_transect)
    #print(unique_week)

    #['156', '157', '158', '162', '163', '164', '170', '171', '172', '177', '178', 
    # '179', '183', '184', '191', '192', '193', '201', '202', '203', '204', '205', 
    # '206', '212', '213', '214', '218', '219', '220', '234', '235', '236']
    #['pm', 'am']
    #['oakMargin', 'control']
    #['23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '34']

    incoming_df = df

    
    for julian in unique_julian:

        for transect in unique_transect:

            for time in unique_time:


                filtered_df = pd.DataFrame()

                #  !!!!!!!  'f' is curly brace support !!!!!!!
                filtered_df = incoming_df.query( f" transect == '{transect}' and julian == '{julian}' and time == '{time}' ")
                # 0    transect row time week julian Thomisidae (crab spider) position

                unique_rows = filtered_df['row'].unique()

                #print("type= ", type(unique_rows)) 
                # type=  <class 'numpy.ndarray'>

                if  unique_rows.size == 0:
                    break

                #print("transect ", transect, " time ", time, " rows :", unique_rows)

                # build a sentence in the language of spider counts that will ultimatedly be
                # used to compare to other sentances
                daily_spider_total_int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


                # the df represents the counts for transect day and time 
                # for each position across each sampled vineyard row
                # now sum all the counts by position

                # filter on 'position'; (so now the df contains positional spiders by row)
                for i in range(10):

                    temp_df = filtered_df
                    temp_df = temp_df.query( f" position == '{i+1}' ")
                    daily_spider_total_int[i] = temp_df['Thomisidae (crab spider)'].astype(int).sum()

                #print(":::::::::::::::::::::count total for filtered_df :::::::::::::::::::::::::::")
                #print(filtered_df)
                #print(daily_spider_total_int)
                #print(":::::::::::::::::::::: end count total ::::::::::::::::::::::::::")
                
                # print(daily_spider_total_int)
                # Convert each integer to a string using list comprehension
                # (this s a concise and Pythonic way to convert each integer in the list to a string)
                daily_spider_total_txt = [str(x) for x in daily_spider_total_int]
                #
                # insert context (what julian, time, week, and transect is that daya from)
                # (when you insert an element, all existing elements after the specified index are shifted 
                #  one position to the right)

                # insert context (what julian, time, week, and transect is that day from)
                # (when you insert an element, all existing elements after the specified index are shifted 
                #  one position to the right)

                daily_spider_total_txt.insert(0, filtered_df.iloc[0,4]) # julian
                daily_spider_total_txt.insert(0, filtered_df.iloc[0,3]) # week
                daily_spider_total_txt.insert(0, filtered_df.iloc[0,2]) # time
                daily_spider_total_txt.insert(0, filtered_df.iloc[0,0]) # transect


                # these are the daily totals, by position, summed across 3 vineyard rows, for a specific 
                # week, time, and transect
                #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>> daily_spider_total_txt >>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                #print(daily_spider_total_txt)
                #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>> end daily_spider_total_txt >>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                # ['oakMargin', 'pm', '23', '156', '0', '0', '0', '0', '2', '0', '1', '1', '1', '0']
                # ['control', 'pm', '23', '156', '0', '0', '1', '0', '1', '0', '1', '1', '0', '2']

                    
                list_holding_tank.insert(0, daily_spider_total_txt)

    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>.list_holding_tank>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #print(list_holding_tank)
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>.end list_holding_tank>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # [[['control', 'am', '34', '236', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
    #   ['control', 'pm', '34', '236', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1'], 
    #   ['oakMargin', 'am', '34', '236', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    #

    # build a dataframe
    import pandas as pd
    df = pd.DataFrame(list_holding_tank, columns=['transect', 'time', 'week', 'julian',  
                                                 'p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9'])

    # print(df)
    #   julian time week   transect p0 p1 p2 p3 p4 p5 p6 p7 p8 p9
    # 0    164   am   24  oakMargin  2  2  2  3  1  1  4  4  0  2
    # 1    163   am   24  oakMargin  1  1  0  1  2  3  6  1  1  2
    # 2    162   am   24  oakMargin  2  1  1  0  1  0  2  1  0  0

    # # Insert a delimeter (index 4) to support string truncation 
    df.insert(4, 'delimeter', ':')


    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>.delimeter>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #print(df)
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>.end delimeter>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

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

    return(df)


def weekly_spider_count(df):

    ########################################################################
    #
    # sum spider counts by julian day
    # input can mix records for 'transect', 'week', and 'time'.
    # dataframe should be compressed by vindeyard row 
    # 
    # return a dataframe with text identifiers, a delimeter, and the totalized count by position
    ########################################################################

    
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


    import pandas as pd
    
    unique_weeks = df['week'].unique()
    unique_time = df['time'].unique()

    # prep a list of lists to load a dataframe for return
    list_holding_tank = []

    # without specifying the specific vineyard weeks sampled, we can sum the spider counts
    # by week, transect, and time represented in the dataframe

    # create records that represent the number of spiders occurring in sequential positions
    # read each record, examine the position, and place the spider count for that position in 
    # the matching column. Then we have ordered sequences of counts (that represent a pattern)


    unique_julian = df['julian'].unique()
    unique_time = df['time'].unique()
    unique_transect = df['transect'].unique()
    unique_week = df['week'].unique()

    #print(unique_time)
    #print(unique_transect)
    #print(unique_week)

    #['156', '157', '158', '162', '163', '164', '170', '171', '172', '177', '178', 
    # '179', '183', '184', '191', '192', '193', '201', '202', '203', '204', '205', 
    # '206', '212', '213', '214', '218', '219', '220', '234', '235', '236']
    #['pm', 'am']
    #['oakMargin', 'control']
    #['23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '34']

    incoming_df = df

    
    for week in unique_week:

        for transect in unique_transect:

            for time in unique_time:


                filtered_df = pd.DataFrame()

                #  !!!!!!!  'f' is curly brace support !!!!!!!
                filtered_df = incoming_df.query( f" transect == '{transect}' and week == '{week}' and time == '{time}' ")
                # 0    transect row time week julian Thomisidae (crab spider) position

                unique_julian = filtered_df['julian'].unique()

                #print("type= ", type(unique_rows)) 
                # type=  <class 'numpy.ndarray'>

                if  unique_julian.size == 0:
                    print("julian size was 0")
                    break

                #print("transect ", transect, " time ", time, " rows :", unique_rows)

                # build a sentence in the language of spider counts that will ultimatedly be
                # used to compare to other sentances
                daily_spider_total_int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


                # the df represents the counts for transect day and time 
                # for each position across each sampled vineyard row
                # now sum all the counts by position

                # filter on 'position'; (so now the df contains positional spiders by row)
                for i in range(10):

                    temp_df = filtered_df
                    temp_df = temp_df.query( f" position == '{i+1}' ")
                    daily_spider_total_int[i] = temp_df['Thomisidae (crab spider)'].astype(int).sum()

                #print(":::::::::::::::::::::count total for filtered_df :::::::::::::::::::::::::::")

                # print(daily_spider_total_int, ' ', week, ' ', time, ' ', transect)

                # [1, 3, 2, 3, 5, 0, 3, 3, 4, 3]   23   pm   oakMargin
                # [1, 3, 0, 0, 0, 0, 4, 0, 0, 1]   23   am   oakMargin
                # [1, 3, 4, 5, 1, 5, 6, 5, 1, 4]   23   pm   control
                # [0, 2, 1, 1, 0, 1, 1, 3, 0, 1]   23   am   control
                # [10, 9, 6, 2, 7, 5, 7, 9, 14, 6]   24   pm   oakMargin
                # [5, 4, 3, 4, 4, 4, 12, 6, 1, 4]   24   am   oakMargin
                # [8, 6, 10, 3, 10, 7, 10, 5, 14, 15]   24   pm   control
                # [3, 2, 4, 5, 3, 2, 1, 3, 9, 6]   24   am   control

                
                # Convert each integer to a string using list comprehension
                # (this s a concise and Pythonic way to convert each integer in the list to a string)
                daily_spider_total_txt = [str(x) for x in daily_spider_total_int]
                #
                # insert context (what time, week, and transect is that daya from)
                # (when you insert an element, all existing elements after the specified index are shifted 
                #  one position to the right)

                # insert context (what julian, time, week, and transect is that day from)
                # (when you insert an element, all existing elements after the specified index are shifted 
                #  one position to the right)

                daily_spider_total_txt.insert(0, filtered_df.iloc[0,3]) # week
                daily_spider_total_txt.insert(0, filtered_df.iloc[0,2]) # time
                daily_spider_total_txt.insert(0, filtered_df.iloc[0,0]) # transect


                # these are the daily totals, by position, summed across 3 vineyard rows, for a specific 
                # week, time, and transect
                #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>> daily_spider_total_txt >>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                #print(daily_spider_total_txt)
                #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>> end daily_spider_total_txt >>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                # ['oakMargin', 'pm', '23', '156', '0', '0', '0', '0', '2', '0', '1', '1', '1', '0']
                # ['control', 'pm', '23', '156', '0', '0', '1', '0', '1', '0', '1', '1', '0', '2']

                    
                list_holding_tank.insert(0, daily_spider_total_txt)

    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>.list_holding_tank>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #print(list_holding_tank)
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>.end list_holding_tank>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # [[['control', 'am', '34', '236', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], 
    #   ['control', 'pm', '34', '236', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1'], 
    #   ['oakMargin', 'am', '34', '236', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    #

    # build a dataframe
    import pandas as pd
    df = pd.DataFrame(list_holding_tank, columns=['transect', 'time', 'week',  
                                                 'p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9'])

    # print(df)
    #      transect time week  p0 p1  p2 p3  p4 p5  p6 p7  p8  p9
    # 0     control   am   34   0  0   0  0   0  0   0  0   1   0
    # 1     control   pm   34   0  1   0  0   0  0   0  0   1   1
    # 2   oakMargin   am   34   0  0   0  0   0  0   0  0   0   0
    # 3   oakMargin   pm   34   1  0   0  0   0  0   0  0   0   0
    # 4     control   am   32   1  1   0  0   0  0   1  1   0   0
    # 5     control   pm   32   0  0   1  0   0  0   0  3   0   2
    # 6   oakMargin   am   32   1  0   0  0   0  0   0  0   1   0
    # 7   oakMargin   pm   32   1  0   0  2   0  2   3  0   1   0
    #
    # 

    # # Insert a delimeter (index 4) to support string truncation 
    df.insert(4, 'delimeter', ':')


    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>.delimeter>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #print(df)

    #       transect time week delimeter p0 p1 p2 p3 p4 p5 p6 p7 p8 p9
    # 0      control   am   34    :      0  0  0  0  0  0  0  0  0  0
    # 1      control   pm   34    :      0  0  0  0  0  0  0  0  1  1
    # 2    oakMargin   am   34    :      0  0  0  0  0  0  0  0  0  0
    # 3    oakMargin   pm   34    :      0  0  0  0  0  0  0  0  0  0
    # 4      control   am   34    :      0  0  0  0  0  0  0  0  0  0
    # ..         ...  ...  ...    ...       ... .. .. .. .. .. .. .. .. .. ..
    # 117    control   pm   23    :      0  0  1  4  0  2  2  1  0  1
    # 118  oakMargin   am   23    :      0  1  0  0  0  0  2  0  0  0
    # 119  oakMargin   pm   23    :      0  0  1  1  3  0  1  0  1  0
    # 120    control   pm   23    :      0  0  1  0  1  0  1  1  0  2
    # 121  oakMargin   pm   23    :      0  0  0  0  2  0  1  1  1  0
    # 
    # [122 rows x 15 columns]

    filename = './metrics/week_counts_df' + '-.csv'
    df.to_csv(filename, header=True, index=True, mode='w')

    cols_to_normalize = ['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9']
    df[cols_to_normalize] = df[cols_to_normalize].astype(int)
    df[cols_to_normalize] = df[cols_to_normalize].div(df[cols_to_normalize].sum(axis=1), axis=0)
    # (the cols of the df have been converted from counts to proportions)
    # print(df)
    #      transect time week        p0  ...        p6        p7        p8        p9
    # 0     control   am   34  0.000000  ...  0.000000  0.000000  1.000000  0.000000
    # 1     control   pm   34  0.000000  ...  0.000000  0.000000  0.333333  0.333333
    # 2   oakMargin   am   34       NaN  ...       NaN       NaN       NaN       NaN
    # 3   oakMargin   pm   34  1.000000  ...  0.000000  0.000000  0.000000  0.000000
    # 4     control   am   32  0.250000  ...  0.250000  0.250000  0.000000  0.000000
    # 5     control   pm   32  0.000000  ...  0.000000  0.500000  0.000000  0.333333
    # 6   oakMargin   am   32  0.500000  ...  0.000000  0.000000  0.500000  0.000000


    #prob_df = probs.reset_index()
    #prob_df.columns = ['count', 'probability']

    #filename = './metrics/week_df' + '-.csv'
    #prob_df.to_csv(filename, header=True, index=True, mode='w')

    return(df)

def df_to_corpus_text(df_compressed):

    #selected_columns = df.loc[:, ['transect', 'row', 'time', 'week', 'julian', 'Thomisidae (crab spider)', 'position']]
    #df = df.loc[:, ['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9']]

    corpus = []

    df = df_compressed
        
    for i in range(len(df_compressed)): 
        # Read the first row and concatenate values into a single line
        row = df.iloc[i]
        row_string = ' '.join(row.astype(str))
        #print(row_string) 
            
        corpus.insert(0, row_string)

    #print(">>>>>>>>>>>>> row string >>>>>>>>>>>>")
    #print(row_string)
    #print(">>>>>>>>>>>>> row string end >>>>>>>>>>>>")
    # oakMargin pm 23 156 : 0 0 0 0 2 0 1 1 1 0

    return(corpus)

    
def corpus_text_df(compressed_df, kmeans):



    ###############################################################################
    #
    # if KMEANS
    #
    # create 4 encoded words for return as a text separated by space
    # (earlier analysis with kmeans() suggests that there are 3
    #  similar domains per vineyard row. these are:
    # positions 0, 1, 2  (first_count_position_list)
    # positions 3, 4, 5
    # positions 6, 7, 8, 
    # positioin 9
    #
    # returning the context string and a 'sentence' formed by 4 encoded words
    #
    # note: similarity comparison with ngram=2 suggests that the first 3 'words'
    # should be equal in length to do a more robust pair-by-pair analysis
    #----------------------------------------------------------------------------

    # input df
    #      transect    time week julian delimeter p0 p1 p2 p3 p4 p5 p6 p7 p8 p9
    # 115  oakMargin   pm   23    158           :  1  3  1  2  0  0  1  2  2  3
    # 119  oakMargin   pm   23    157           :  0  0  1  1  3  0  1  0  1  0
    # 121  oakMargin   pm   23    156           :  0  0  0  0  2  0  1  1  1  0

    # output df
    #       transect time  ...    squashed                                        transformed
    # 115  oakMargin   pm  ...  1312001223      TRUETRUETRUE TRUEfalsefalse TRUETRUETRUE TRUE
    # 119  oakMargin   pm  ...  0011301010   falsefalseTRUE TRUETRUEfalse TRUEfalseTRUE false
    # 121  oakMargin   pm  ...  0000201110  falsefalsefalse falseTRUEfalse TRUETRUETRUE false
    # 
    # [3 rows x 17 columns]

    ###############################################################################

    import pandas as pd 

    part1_df = compressed_df.iloc[:, :5]
    #print(part1_df)
    #       transect time week julian delimeter
    # 115  oakMargin   pm   23    158         :
    # 119  oakMargin   pm   23    157         :
    # 121  oakMargin   pm   23    156         :

    part2_df = compressed_df.iloc[:, 5:]
    #print(part2_df)
    #     p0 p1 p2 p3 p4 p5 p6 p7 p8 p9
    # 115  1  3  1  2  0  0  1  2  2  3
    # 119  0  0  1  1  3  0  1  0  1  0
    # 121  0  0  0  0  2  0  1  1  1  0

    part2_df['squashed'] = part2_df['p0'] + part2_df['p1'] + part2_df['p2'] + part2_df['p3'] + part2_df['p4'] + part2_df['p5'] + part2_df['p6'] + part2_df['p7'] + part2_df['p8'] + part2_df['p9'] 
    #print(part2_df)
    #     p0 p1 p2 p3 p4 p5 p6 p7 p8 p9    squashed
    # 115  1  3  1  2  0  0  1  2  2  3  1312001223
    # 119  0  0  1  1  3  0  1  0  1  0  0011301010
    # 121  0  0  0  0  2  0  1  1  1  0  0000201110  
    
    '''
    # isolate the 10 integers
    part1, separator, part2 = text.partition(":")  
    # print("text :", text, "  part1: ", part1, "    part2: ", part2)
    # print(part2) 
    #  2 1 1 0 1 0 2 1 0 0

    # remove the whitespace from the section of 10 "integers" 
    part2_no_spaces = part2.replace(" ", "")
    # print("part2_no_spaces " , part2_no_spaces)

    # there should be only 10 characters
    if len(part2_no_spaces) != 10:
        return(["choked ", "no_space_counts != 10  ", part2_no_spaces])

    # make some bogus words for use in sentence comparison
    '''
    
    sentence_list = []

    for contents in part2_df['squashed']:

        if kmeans:

            print("len= ", len(contents), " contents[0] :", contents[0], "  contents[9] :", contents[9])
            word_one = ""
            word_two = ""
            word_three = ""
            word_four = ""
            #sentence_list = []

            if contents[0] == "0":
                word_one = "false"
            else:
                word_one = "TRUE"
            #print("contents0: ", contents, " word_one: .", word_one, ".")

            if contents[1] == "0":
                word_one = word_one + "false"
            else:
                word_one = word_one + "TRUE"
            #print("contents1: ", contents, " word_one: .", word_one, ".")

            if contents[2] == "0":
                word_one = word_one + "false"
            else:
                word_one = word_one + "TRUE"
            #print("contents2: ", contents, " word_one: .", word_one, ".")


            if contents[3] == "0":
                word_two = "false"
            else:
                word_two = "TRUE"

            if contents[4] == "0":
                word_two = word_two + "false"
            else:
                word_two = word_two + "TRUE"

            if contents[5] == "0":
                word_two = word_two + "false"
            else:
                word_two = word_two + "TRUE"


            if contents[6] == "0":
                word_three = "false"
            else:
                word_three = "TRUE"

            if contents[7] == "0":
                word_three = word_three + "false"
            else:
                word_three = word_three + "TRUE"

            if contents[8] == "0":
                word_three = word_three + "false"
            else:
                word_three = word_three + "TRUE"


            if contents[9] == "0":
                word_four = "false"
            else:
                word_four = "TRUE"


            new_sentence = word_one + " " + word_two + " " + word_three + " " + word_four

        else:

            w0 = 'TRUE'
            w1 = 'TRUE'
            w2 = 'TRUE'
            w3 = 'TRUE'
            w4 = 'TRUE'
            w5 = 'TRUE'
            w6 = 'TRUE'
            w7 = 'TRUE'
            w8 = 'TRUE'
            w9 = 'TRUE'

            if contents[0] == "0":
                w0 = "false"
            if contents[1] == "0":
                w1 = "false"
            if contents[2] == "0":
                w2 = "false"
            if contents[3] == "0":
                w3 = "false"
            if contents[4] == "0":
                w4 = "false"
            if contents[5] == "0":
                w5 = "false"
            if contents[6] == "0":
                w6 = "false"
            if contents[7] == "0":
                w7 = "false"
            if contents[8] == "0":
                w8 = "false"
            if contents[9] == "0":
                w9 = "false"

            new_sentence = w0 + " " + w1 + " " + w2 + " " + w3 + " " + w4 + " " + w5 + " " + w6 + " " + w7 + " " + w8 + " " + w9

        sentence_list.append(new_sentence)
        #print("sentence_list: ", sentence_list)
        
    #print("adding new column: ", sentence_list)
    part2_df['transformed'] = sentence_list

    #print(">>>>>>>>>>>>> transformed>>>>>>>>>>>>>>")
    #print(part2_df)
    #print(">>>>>>>>>>>>> end transformed>>>>>>>>>>>>>>") 

    #     p0 p1 p2 p3  ... p8 p9    squashed                                        transformed
    # 115  1  3  1  2  ...  2  3  1312001223      TRUETRUETRUE TRUEfalsefalse TRUETRUETRUE TRUE
    # 119  0  0  1  1  ...  1  0  0011301010   falsefalseTRUE TRUETRUEfalse TRUEfalseTRUE false
    # 121  0  0  0  0  ...  1  0  0000201110  falsefalsefalse falseTRUEfalse TRUETRUETRUE false
    # 
    # [3 rows x 12 columns]

    # join the dataframes side-by-side
    result = pd.concat([part1_df, part2_df], axis=1)

    #print(result)
    #       transect time  ...    squashed                                        transformed
    # 115  oakMargin   pm  ...  1312001223      TRUETRUETRUE TRUEfalsefalse TRUETRUETRUE TRUE
    # 119  oakMargin   pm  ...  0011301010   falsefalseTRUE TRUETRUEfalse TRUEfalseTRUE false
    # 121  oakMargin   pm  ...  0000201110  falsefalsefalse falseTRUEfalse TRUETRUETRUE false
    # 
    # [3 rows x 17 columns]

    return(result)


def TWT_row_similarity(records_list, transect, week, time):

    ####################################################################################################
    # for each sampling day in a specific week
    # make count totals for each vineyard sampling position by adding counts for each vinyard row sampled
    # these count totals are converted to 3 word senences that are compared for similarity
    #   (in the output below, 
    #    '162' is a julian day, 'am' is the time, '24' is the week, 'control' is the transect).
    #    there are two other sampling days in that week ('163' and '164'). Each data-sentence
    #    is compared to itself and to the others, similarity metrics are stacked in the array
    #    along with the strings representing the data-pairs evaluated against each other)
    ####################################################################################################

    import thad_o_mizer

    # ------------------------------------------------------------------------------
    # get the daily counts by combining counts for the vineyard rows that were sampled
    # compress the daily counts by row into daily total counts (add counts by position)
    df = daily_spider_count(df=week_records_df)

    # //////////////////////////////TWT_row_similarity////////////////////////////////////////////////
    # print(df)
    # //////////////////////////////////////////////////////////////////////////////
    #   julian time week transect delimeter p0 p1 p2 p3 p4 p5 p6 p7 p8 p9
    # 0    164   am   24  control         :  2  0  1  2  1  2  0  2  5  2
    # 1    163   am   24  control         :  0  2  2  2  1  0  1  0  3  4
    # 2    162   am   24  control         :  1  0  1  1  1  0  0  1  1  0
    # //////////////////////////////////////////////////////////////////////////////

    # create a list of text strings for each week representing the 


    corpus_text_list = df_to_corpus_text(df_list=[df])

    # print(corpus_text_list)
    # ['162 am 24 control : 1 0 1 1 1 0 0 1 1 0', 
    #  '163 am 24 control : 0 2 2 2 1 0 1 0 3 4', 
    #  '164 am 24 control : 2 0 1 2 1 2 0 2 5 2']


    for k in range(len(corpus_text_list)):
        # sending k sentences : '163 am 24 oakMargin : 2 1 1 0 1 0 2 1 0 0' 
        corpus_text_list[k] = row_text_to_three_words(corpus_text_list[k]) 

    #print(corpus_text_list)
    # //////////////////////////////////////////////////////////////////////////////
    # [['162 am 24 control ', 'TRUEfalseTRUE TRUETRUEfalse falseTRUETRUE false'], 
    #  ['163 am 24 control ', 'falseTRUETRUE TRUETRUEfalse TRUEfalseTRUE TRUE'], 
    #  ['164 am 24 control ', 'TRUEfalseTRUE TRUETRUETRUE falseTRUETRUE TRUE']]
    # //////////////////////////////////////////////////////////////////////////////


    # for a specific transect/time/day, compare each day's totalized spider counts to 
    # the other days in the same week
    #
    metrics_array = thad_o_mizer.stacked_similarity(corpus=corpus_text_list, raw=True)

    # [[0.9999999  0 1.0                0.9999999  0 1.0                '162 am 24 control ' '162 am 24 control ']
    #  [0.97768813 3 0.7272727272727273 0.97768813 3 0.7272727272727273 '162 am 24 control ' '163 am 24 control ']
    #  [0.95014405 2 0.6206896551724138 0.95014405 2 0.6206896551724138 '162 am 24 control ' '164 am 24 control ']
    #  [0.97768813 3 0.7272727272727273 0.97768813 3 0.7272727272727273 '163 am 24 control ' '162 am 24 control ']
    #  [1.0        0 1.0                1.0        0 1.0                '163 am 24 control ' '163 am 24 control ']
    #  [0.9795705  3 0.7222222222222222 0.9795705  3 0.7222222222222222 '163 am 24 control ' '164 am 24 control ']
    #  [0.95014405 2 0.6206896551724138 0.95014405 2 0.6206896551724138 '164 am 24 control ' '162 am 24 control ']
    #  [0.9795705  3 0.7222222222222222 0.9795705  3 0.7222222222222222 '164 am 24 control ' '163 am 24 control ']
    #  [1.0000001  0 1.0                1.0000001  0 1.0                '164 am 24 control ' '164 am 24 control ']]


    import pandas as pd

    # Convert to a DataFrame
    df = pd.DataFrame(metrics_array)

    df.columns = ['BOW cosine similarity', 'levenshtein distance', 
    'NGRAM cosine similarity', 'BPW flip', 'LD flip', 'NGRAM flip', 'data ID 1', 'data ID 2']

    return(df)



    # ------------------------------------------------------------------------------

def julian_row_compare(df):

    ########################################################################
    #
    # compare spider count text similarity by julian day for each row by transect and time
    # for each julian day, there are 3 rows that were sampled
    # 
    # return a dataframe 
    #
    #      transect, week, julian, time, row1_to_row2, row1_to_row3, row2_to_row3
    #
    ########################################################################

    import pandas as pd
    import sys
    
    unique_weeks = df['week'].unique()
    unique_time = df['time'].unique()

    # prep a list of lists to load a dataframe for return
    list_holding_tank = []


    unique_julian = df['julian'].unique()
    unique_time = df['time'].unique()
    unique_transect = df['transect'].unique()
    unique_week = df['week'].unique()

    #print(unique_time)
    #print(unique_transect)
    #print(unique_week)

    #['156', '157', '158', '162', '163', '164', '170', '171', '172', '177', '178', 
    # '179', '183', '184', '191', '192', '193', '201', '202', '203', '204', '205', 
    # '206', '212', '213', '214', '218', '219', '220', '234', '235', '236']
    #['pm', 'am']
    #['oakMargin', 'control']
    #['23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '34']

    incoming_df = df
    
    for julian in unique_julian:

        for transect in unique_transect:

            for time in unique_time:

                filtered_df = pd.DataFrame()

                #  !!!!!!!  'f' is curly brace support !!!!!!!
                filtered_df = incoming_df.query( f" transect == '{transect}' and julian == '{julian}' and time == '{time}' ")
                # 0    transect row time week julian Thomisidae (crab spider) position

                unique_rows = filtered_df['row'].unique()

                if  unique_rows.size == 0:
                    break

                #print(filtered_df)
                # 0    transect row time week julian Thomisidae (crab spider) position
                # 3661  control  49   pm   34    236                        0        1
                # 3662  control  49   pm   34    236                        0        2
                # 3663  control  49   pm   34    236                        0        3
                # 3664  control  49   pm   34    236                        0        4
                # 3665  control  49   pm   34    236                        0        5
                # 3666  control  49   pm   34    236                        0        6
                # 3667  control  49   pm   34    236                        0        7
                # 3668  control  49   pm   34    236                        0        8
                # 3669  control  49   pm   34    236                        0        9
                # 3670  control  49   pm   34    236                        0       10
                # 3671  control  51   pm   34    236                        0        1
                # 3672  control  51   pm   34    236                        0        2
                # 3673  control  51   pm   34    236                        0        3
                # 3674  control  51   pm   34    236                        0        4
                # 3675  control  51   pm   34    236                        0        5
                # 3676  control  51   pm   34    236                        0        6
                # 3677  control  51   pm   34    236                        0        7
                # 3678  control  51   pm   34    236                        0        8
                # 3679  control  51   pm   34    236                        1        9
                # 3680  control  51   pm   34    236                        0       10
                # 3681  control  53   pm   34    236                        0        1
                # 3682  control  53   pm   34    236                        0        2
                # 3683  control  53   pm   34    236                        0        3
                # 3684  control  53   pm   34    236                        0        4
                # 3685  control  53   pm   34    236                        0        5
                # 3686  control  53   pm   34    236                        0        6
                # 3687  control  53   pm   34    236                        0        7
                # 3688  control  53   pm   34    236                        0        8
                # 3689  control  53   pm   34    236                        0        9
                # 3690  control  53   pm   34    236                        1       10


                spider_list = []
                i=0

                for row in unique_rows:

                    # build a sentence in the language of spider counts that will ultimatedly be
                    # used to compare to other sentances
                    spider_list = []

                    temp_df = filtered_df.query( f" row == '{row}' ")

                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> unique_rows >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    #print(temp_df.to_string())
                    #print("to_string done")
                    #sys.exit()
                    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> end unique_rows >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    
                    # 0     transect row time week julian Thomisidae (crab spider) position
                    # 121  oakMargin  79   pm   23    157                        0        1
                    # 122  oakMargin  79   pm   23    157                        0        2
                    # 123  oakMargin  79   pm   23    157                        0        3
                    # 124  oakMargin  79   pm   23    157                        0        4
                    # 125  oakMargin  79   pm   23    157                        2        5
                    # 126  oakMargin  79   pm   23    157                        0        6
                    # 127  oakMargin  79   pm   23    157                        1        7
                    # 128  oakMargin  79   pm   23    157                        0        8
                    # 129  oakMargin  79   pm   23    157                        0        9
                    # 130  oakMargin  79   pm   23    157                        0       10

                    spider_list.insert(0, temp_df.loc[:,'Thomisidae (crab spider)'].values.flatten().tolist() ) # (all rows)

                    #print("spider_list: ", spider_list)
                    # spider_list:  [['1', '0', '0', '1', '0', '0', '0', '1', '0', '0']]
                    result = " ".join(spider_list[0])  # Use space as a delimiter
                    i=i+1
                    print("i: ", i, "  result: ", result, "  type: ", type(result))
                    # result:  1 0 0 1 0 0 0 1 0 0   type:  <class 'str'>


                    # insert context (what julian, time, week, and transect is that day is from)
                    # (when you insert an element, all existing elements after the specified index are shifted 
                    #  one position to the right)

                    # insert context (what julian, time, week, and transect is that day from)
                    # (when you insert an element, all existing elements after the specified index are shifted 
                    #  one position to the right)

                    # and, "access a cell value using only the row number and column label"
                    # # Row number (e.g., 1) and column label (e.g., "Age")
                    # value = df.iloc[row_number, df.columns.get_loc(column_label)]

                    daily_spider_list = ["", "", "", "", "", ""]
                    
                    daily_spider_list[0] = transect 
                    daily_spider_list[1] = row 
                    daily_spider_list[2] = time  
                    daily_spider_list[3] = temp_df.iloc[1, temp_df.columns.get_loc('week')]
                    daily_spider_list[4] = julian 
                    daily_spider_list[5] = result

                    #print(daily_spider_list)
                    # ['oakMargin', '81', 'pm', '34', '235', '0 0 0 0 0 0 0 0 0 0']

                    # append new_list to the end of parent_list
                    # parent_list.append(new_list)
                    list_holding_tank.append(daily_spider_list) 
              

    # print(list_holding_tank)
    # [['oakMargin', '79', 'pm', '23', '156', '0 0 0 0 0 0 1 0 1 0'], 
    #  ['oakMargin', '81', 'pm', '23', '156', '0 0 0 0 1 0 0 1 0 0'], 
    #

    # build a dataframe
    import pandas as pd
    df = pd.DataFrame(list_holding_tank, columns=['transect','row', 'time', 'week', 'julian', 'counts'])


    # print(df)
    #        transect row time week julian               counts
    # 0     oakMargin  79   pm   23    156  0 0 0 0 0 0 1 0 1 0
    # 1     oakMargin  81   pm   23    156  0 0 0 0 1 0 0 1 0 0
    # 2     oakMargin  83   pm   23    156  0 0 0 0 1 0 0 0 0 0
    # 3       control  48   pm   23    156  0 0 1 0 0 0 0 0 0 2
    # 4       control  50   pm   23    156  0 0 0 0 0 0 1 1 0 0
    #  ..         ...  ..  ...  ...    ...                  ...
    # 361     control  51   pm   34    236  0 0 0 0 0 0 0 0 1 0
    # 362     control  53   pm   34    236  0 0 0 0 0 0 0 0 0 1
    # 363     control  49   am   34    236  0 0 0 0 0 0 0 0 0 0
    # 364     control  51   am   34    236  0 0 0 0 0 0 0 0 0 0
    # 365     control  53   am   34    236  0 0 0 0 0 0 0 0 0 0
    # 
    # [366 rows x 6 columns]


    # # Insert a delimeter (index 5) to support string truncation 
    df.insert(5, 'delimeter', ':')

    # squash to count text and construct words
    df = squash_and_translate(df)


    return(df)


def squash_and_translate(df):

    #print("input")
    #print(df)
    #print("end input")


    ###############################################################################
    #
    #
    # create 4 encoded words for return as a text separated by space
    #
    # returning the context string and a 'sentence' formed by 4 encoded words
    #
    #----------------------------------------------------------------------------
    #
    # input df
    #   
    #        transect row time week julian  delimeter                 counts
    # 0     oakMargin  79   pm   23    156          :    0 0 0 0 0 0 1 0 1 0
    # 1     oakMargin  81   pm   23    156          :    0 0 0 0 1 0 0 1 0 0
    # 2     oakMargin  83   pm   23    156          :    0 0 0 0 1 0 0 0 0 0
    # 3       control  48   pm   23    156          :    0 0 1 0 0 0 0 0 0 2
    # 4       control  50   pm   23    156          :    0 0 0 0 0 0 1 1 0 0
    #  ..         ...  ..  ...  ...    ...                  ...
    # 361     control  51   pm   34    236          :    0 0 0 0 0 0 0 0 1 0
    # 362     control  53   pm   34    236          :    0 0 0 0 0 0 0 0 0 1
    # 363     control  49   am   34    236          :    0 0 0 0 0 0 0 0 0 0
    # 364     control  51   am   34    236          :    0 0 0 0 0 0 0 0 0 0
    # 365     control  53   am   34    236          :    0 0 0 0 0 0 0 0 0 0
    # 
    # [366 rows x 6 columns]
    #
    # output df
    #
    #       transect time  ...    squashed                                        transformed
    # 115  oakMargin   pm  ...  1312001223      TRUETRUETRUE TRUEfalsefalse TRUETRUETRUE TRUE
    # 119  oakMargin   pm  ...  0011301010   falsefalseTRUE TRUETRUEfalse TRUEfalseTRUE false
    # 121  oakMargin   pm  ...  0000201110  falsefalsefalse falseTRUEfalse TRUETRUETRUE false
    # 
    # [3 rows x 17 columns]
    #
    ###############################################################################

    import sys
    import pandas as pd 

    compressed_df = df

    print(df.to_string())
    print("to_string done")
    sys.exit()

    part1_df = compressed_df.iloc[:, :6]
    #print(part1_df)
    #       transect row time week julian delimeter
    # 0    oakMargin  79   pm   23    156         :
    # 1    oakMargin  81   pm   23    156         :
    # 2    oakMargin  83   pm   23    156         :
    # 3      control  48   pm   23    156         :
    # 4      control  50   pm   23    156         :
    # ..         ...  ..  ...  ...    ...       ...
    # 361    control  51   pm   34    236         :
    # 362    control  53   pm   34    236         :
    # 363    control  49   am   34    236         :
    # 364    control  51   am   34    236         :
    # 365    control  53   am   34    236         :
    # 
    # [366 rows x 6 columns]

    

    part2_df = compressed_df.iloc[:, 6:]
    #print(part2_df.to_string())
    #                   counts
    # 0    0 0 0 0 0 0 1 0 1 0
    # 1    0 0 0 0 1 0 0 1 0 0
    # 2    0 0 0 0 1 0 0 0 0 0
    # 3    0 0 1 0 0 0 0 0 0 2
    # 4    0 0 0 0 0 0 1 1 0 0
    # ..                   ...
    # 361  0 0 0 0 0 0 0 0 1 0
    # 362  0 0 0 0 0 0 0 0 0 1
    # 363  0 0 0 0 0 0 0 0 0 0
    # 364  0 0 0 0 0 0 0 0 0 0
    # 365  0 0 0 0 0 0 0 0 0 0
    # 
    # [366 rows x 1 columns]

    #print("to_string done")
    #sys.exit()

    # remove the whitespace from the section of 10 "integers" 
    # Remove all spaces from the 'City' column
    part2_df['squashed'] = part2_df['counts'].str.replace(" ", "", regex=False)

    #                   counts    squashed
    # 0    0 0 0 0 0 0 1 0 1 0  0000001010
    # 1    0 0 0 0 1 0 0 1 0 0  0000100100
    # 2    0 0 0 0 1 0 0 0 0 0  0000100000
    # 3    0 0 1 0 0 0 0 0 0 2  0010000002
    # 4    0 0 0 0 0 0 1 1 0 0  0000001100
    # ..                   ...         ...
    # 361  0 0 0 0 0 0 0 0 1 0  0000000010
    # 362  0 0 0 0 0 0 0 0 0 1  0000000001
    # 363  0 0 0 0 0 0 0 0 0 0  0000000000
    # 364  0 0 0 0 0 0 0 0 0 0  0000000000
    # 365  0 0 0 0 0 0 0 0 0 0  0000000000
    # 
    # [366 rows x 2 columns]

    # make some bogus words for use in sentence comparison

    
    sentence_list = []
    i=-1

    for contents in part2_df['squashed']:

        i=i+1

        print("part1: ", "contents: ", contents, " i= ", i, " part1: ", part1_df.iloc[i])

        w0 = 'TRUE'
        w1 = 'TRUE'
        w2 = 'TRUE'
        w3 = 'TRUE'
        w4 = 'TRUE'
        w5 = 'TRUE'
        w6 = 'TRUE'
        w7 = 'TRUE'
        w8 = 'TRUE'
        w9 = 'TRUE'

        if contents[0] == "0":
            w0 = "false"
        if contents[1] == "0":
            w1 = "false"
        if contents[2] == "0":
            w2 = "false"
        if contents[3] == "0":
            w3 = "false"
        if contents[4] == "0":
            w4 = "false"
        if contents[5] == "0":
            w5 = "false"
        if contents[6] == "0":
            w6 = "false"
        if contents[7] == "0":
            w7 = "false"
        if contents[8] == "0":
            w8 = "false"
        if contents[9] == "0":
            w9 = "false"

        new_sentence = w0 + " " + w1 + " " + w2 + " " + w3 + " " + w4 + " " + w5 + " " + w6 + " " + w7 + " " + w8 + " " + w9

        sentence_list.append(new_sentence)

        
    print("adding new column: ", sentence_list)
    part2_df['transformed'] = sentence_list

    print(">>>>>>>>>>>>> transformed>>>>>>>>>>>>>>")
    print(part2_df)
    print(">>>>>>>>>>>>> end transformed>>>>>>>>>>>>>>") 

    #     p0 p1 p2 p3  ... p8 p9    squashed                                        transformed
    # 115  1  3  1  2  ...  2  3  1312001223      TRUETRUETRUE TRUEfalsefalse TRUETRUETRUE TRUE
    # 119  0  0  1  1  ...  1  0  0011301010   falsefalseTRUE TRUETRUEfalse TRUEfalseTRUE false
    # 121  0  0  0  0  ...  1  0  0000201110  falsefalsefalse falseTRUEfalse TRUETRUETRUE false
    # 
    # [3 rows x 12 columns]

    # join the dataframes side-by-side
    result = pd.concat([part1_df, part2_df], axis=1)

    print(result)
    #       transect time  ...    squashed                                        transformed
    # 115  oakMargin   pm  ...  1312001223      TRUETRUETRUE TRUEfalsefalse TRUETRUETRUE TRUE
    # 119  oakMargin   pm  ...  0011301010   falsefalseTRUE TRUETRUEfalse TRUEfalseTRUE false
    # 121  oakMargin   pm  ...  0000201110  falsefalsefalse falseTRUEfalse TRUETRUETRUE false
    # 
    # [3 rows x 17 columns]


    return(result)


def julian_row_compare_alternate(df):

    ########################################################################
    #
    # compare spider count text similarity by julian day for each row by transect and time
    # for each julian day, there are 3 rows that were sampled
    # 
    # return a dataframe 
    #
    #      transect, week, julian, time, row1_to_row2, row1_to_row3, row2_to_row3
    #
    ########################################################################

    import pandas as pd
    import sys

    # prep a list of lists to load a dataframe for return
    list_holding_tank = []

    sim_df = pd.DataFrame(columns=['transect', 'julian', 'time', 'week', \
        't1_text', 't2_text', 't3_text', 't1_t2', 't1_t3', 't2_t3'])


    unique_julian = df['julian'].unique()
    unique_time = df['time'].unique()
    unique_transect = df['transect'].unique()
    unique_week = df['week'].unique()

    #['156', '157', '158', '162', '163', '164', '170', '171', '172', '177', '178', 
    # '179', '183', '184', '191', '192', '193', '201', '202', '203', '204', '205', 
    # '206', '212', '213', '214', '218', '219', '220', '234', '235', '236']
    #['pm', 'am']
    #['oakMargin', 'control']
    #['23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '34']

    incoming_df = df

    n1_df = pd.DataFrame(columns=['transect','time', 'week', 'julian', 'row', 'counts']) 
    n2_df = pd.DataFrame(columns=['transect','time', 'week', 'julian', 'row', 'counts']) 

    for julian in unique_julian:

        for transect in unique_transect:

            for time in unique_time:

                #print("%%%%%%%%%%%%%\n", "julian: ", julian, " transect: ", transect, " time: ", time, "\n%%%%%%%%%")

                filtered_df = pd.DataFrame()

                #  !!!!!!!  'f' is curly brace support !!!!!!!
                filtered_df = incoming_df.query( f" transect == '{transect}' and julian == '{julian}' and time == '{time}' ")
                # 0    transect row time week julian Thomisidae (crab spider) position

                unique_rows = filtered_df['row'].unique()

                if  unique_rows.size == 0:
                    break

                # print(filtered_df)
                # 0    transect row time week julian Thomisidae (crab spider) position
                # 3661  control  49   pm   34    236                        0        1
                # 3662  control  49   pm   34    236                        0        2
                # 3663  control  49   pm   34    236                        0        3
                # 3664  control  49   pm   34    236                        0        4
                # 3665  control  49   pm   34    236                        0        5
                # 3666  control  49   pm   34    236                        0        6
                # 3667  control  49   pm   34    236                        0        7
                # 3668  control  49   pm   34    236                        0        8
                # 3669  control  49   pm   34    236                        0        9
                # 3670  control  49   pm   34    236                        0       10
                # 3671  control  51   pm   34    236                        0        1
                # 3672  control  51   pm   34    236                        0        2
                # 3673  control  51   pm   34    236                        0        3
                # 3674  control  51   pm   34    236                        0        4
                # 3675  control  51   pm   34    236                        0        5
                # 3676  control  51   pm   34    236                        0        6
                # 3677  control  51   pm   34    236                        0        7
                # 3678  control  51   pm   34    236                        0        8
                # 3679  control  51   pm   34    236                        1        9
                # 3680  control  51   pm   34    236                        0       10
                # 3681  control  53   pm   34    236                        0        1
                # 3682  control  53   pm   34    236                        0        2
                # 3683  control  53   pm   34    236                        0        3
                # 3684  control  53   pm   34    236                        0        4
                # 3685  control  53   pm   34    236                        0        5
                # 3686  control  53   pm   34    236                        0        6
                # 3687  control  53   pm   34    236                        0        7
                # 3688  control  53   pm   34    236                        0        8
                # 3689  control  53   pm   34    236                        0        9
                # 3690  control  53   pm   34    236                        1       10


                spider_list = [] 

                new_string_list = ['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9']


                for row in unique_rows:                  

                    # build a sentence in the language of spider counts that will ultimatedly be
                    # used to compare to other sentances

                    temp_df = filtered_df.query( f" row == '{row}' ")

                    week = temp_df.iloc[1, temp_df.columns.get_loc('week')]

                    if len(temp_df) != 10:

                        #print("weirdness: ") # julian 203, control, pm, week 29, row 48 
                        #print(temp_df)

                        filename = './metrics/discrepancy_log.csv'

                        # mode='w' indicates 'overwrite'
                        temp_df.to_csv(filename, header=True, index=True, mode='a')

                        print("*********  discrepancy written to ", filename) # julian 203, control, pm, week 29, row 48 
                        
                    else:

                        # (each row should have data from 10 different positions)

                        for i in range(10):

                            if temp_df.iloc[i, temp_df.columns.get_loc('Thomisidae (crab spider)')] == '0':

                                new_string_list[i] = 'f '  # spider count is zero for that position

                            else:

                                new_string_list[i] = 'T '  # spider count is non-zero for that position


                        new_string_text = new_string_list[0] + new_string_list[1] + new_string_list[2] + \
                         new_string_list[3] + new_string_list[4] + new_string_list[5] + \
                         new_string_list[6] + new_string_list[7] + new_string_list[8] + new_string_list[9]

                        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> unique_rows >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                        # print(temp_df.to_string())
                        #print("new_string: ", new_string_text)
                        #print("to_string done")
                        #sys.exit()
                        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> end unique_rows >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                        
                
                        # new row as a df in dictionary format
                        n2_df = pd.DataFrame({'transect': [transect], 'time' : [time], 'week' : [week], \
                            'julian' : [julian], 'row' : [row], 'counts' : [new_string_text]})
                        # 
                        #print(">>>>>>>>>>>> new string >>>>>>>>>>>>>>>>")
                        #print(n2_df)
                        #print(">>>>>>>>>>>> end new string >>>>>>>>>>>>>>>>")

                    n1_df = pd.concat([n1_df, n2_df], ignore_index=True)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> unique_rows >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # print(n1_df.to_string())
    #
    #       transect time week julian row                counts
    # 0    oakMargin   pm   23    156  79  f f f f f f T f T f 
    # 1    oakMargin   pm   23    156  81  f f f f T f f T f f 
    #  2    oakMargin   pm   23    156  83  f f f f T f f f f f 
    #  3      control   pm   23    156  48  f f T f f f f f f T 
    #  4      control   pm   23    156  50  f f f f f f T T f f 
    #  5      control   pm   23    156  52  f f f f T f f f f f 
    #  6    oakMargin   pm   23    157  79  f f f f T f T f f f 
    #  7    oakMargin   pm   23    157  81  f f f T T f f f T f 
    #  8    oakMargin   pm   23    157  83  f f T f f f f f f f 
    #  9    oakMargin   am   23    157  79  f T f f f f T f f f 
    #  10   oakMargin   am   23    157  81  f f f f f f T f f f 
    #  11   oakMargin   am   23    157  83  f f f f f f f f f f 
    #  12     control   pm   23    157  48  f f T T f f T T f f 
    #  13     control   pm   23    157  50  f f f T f f T f f f 
    #  14     control   pm   23    157  52  f f f T f T f f f T 
    #  15     control   am   23    157  48  f f T f f f f T f f 
    #  16     control   am   23    157  50  f f f f f f f f f f 
    #  17     control   am   23    157  52  f f f f f f f T f f 
    #
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> end unique_rows >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    #############################################################################################
    #
    # find all rows sampled in the same transect/time/julian (normally 3) and compute NGRAM cosine 
    # similarity between them
    #
    #############################################################################################

    import thad_o_mizer

    sim_df = pd.DataFrame(columns=['transect', 'julian', 'time', 'week', \
        't1_text', 't2_text', 't3_text', 't1_t2', 't1_t3', 't2_t3']) 

    for julian in unique_julian:

            for transect in unique_transect:

                for time in unique_time:

                    filtered_df = pd.DataFrame()

                    #  !!!!!!!  'f' is curly brace support !!!!!!!
                    filtered_df = n1_df.query( f" transect == '{transect}' and julian == '{julian}' \
                        and time == '{time}' ")
                    # 0    transect row time week julian Thomisidae (crab spider) position

                    print(">>>>>>> filtered df >>>>>>>>\n")
                    print(filtered_df)
                    print(">>>>>>> end filtered df >>>>>>>>\n")


                    if len(filtered_df) != 3:     # there should be 3 rows of data

                        filename = './metrics/discrepancy_log.csv'
                        # mode='w' indicates 'overwrite'
                        filtered_df.to_csv(filename, header=True, index=True, mode='a')
                        print("*********  discrepancy written to ", filename) # julian 203, control, pm, week 29, row 48 
                        #                                                     # julian 156 did not have am samples
                        
                    else:

                        week = filtered_df.iloc[1, filtered_df.columns.get_loc('week')]

                        # get the T/f text strings associated with each vineyard row and compute the
                        # NGRAM similarity 

                        t1_text = filtered_df.iloc[0, filtered_df.columns.get_loc('counts')] 
                        t2_text = filtered_df.iloc[1, filtered_df.columns.get_loc('counts')] 
                        t3_text = filtered_df.iloc[2, filtered_df.columns.get_loc('counts')]

                        print("triplet: ", t1_text, "     ", t2_text, "    ", t3_text)

                        t1_t2 = thad_o_mizer.compute_ngram_quick(sentence1 = t1_text, sentence2 = t2_text, ngrams=4)
                        t1_t3 = thad_o_mizer.compute_ngram_quick(sentence1 = t1_text, sentence2 = t3_text, ngrams=4)
                        t2_t3 = thad_o_mizer.compute_ngram_quick(sentence1 = t2_text, sentence2 = t3_text, ngrams=4)

                        print("sims: ", t1_t2, "     ", t1_t3, "    ", t2_t3)

                        new_sim_df = pd.DataFrame({'transect': [transect], \
                            'julian' : [julian], 'time' : [time], 'week' : [week], \
                            't1_text' : [t1_text], 't2_text' : [t2_text], 't3_text' : [t3_text], \
                            't1_t2' : [t1_t2], 't1_t3' : [t1_t3], 't2_t3' : [t2_t3]})
  
                        #print(">>>>>>>>>>>>>>> similarity_df >>>>>>>>>>>>>>>")
                        #print(new_sim_df)

                        sim_df = pd.concat([sim_df, new_sim_df], ignore_index=True)

    filename = './metrics/row_similarity.csv'

    # mode='w' indicates 'overwrite'
    sim_df.to_csv(filename, header=True, index=False, mode='a')




    return(sim_df)


def negative_binomial(number_independent_trials, number_of_successes, csv_ID):

    # *********************** bayes ***********************
    # *********************** https://www.youtube.com/watch?v=3OJEae7Qb_o&t=1288s
    # *********************** https://github.com/rasmusab/bayesianprobabilitiesworkshop/blob/master/Exercise%201.ipynb
    # *********************** https://www.sumsar.net/files/posts/2017-bayesian-tutorial-exercises/modeling_exercise1.html
    # ***********************       ***********************

    # *********************** the Oceanic Tool Complexity data refresher ***********************
    # Bayesian statistical models are used to predict the total number of tools in a society based on 
    # he log of population size and contact rates. For example, in the “Kline” dataset, researchers model 
    # the number of tools as a function of log(population) and whether the population had high or low contact 
    # with others. This approach allows for probabilistic  inference about the drivers of technological 
    # complexity in oceanic populations
    #
    # Example Bayesian Model Structure:
    # •   Response variable: Number of tools in a society
    # •   Predictors: Log of population size, contact rate (high vs. low)
    # •   Bayesian inference: Used to estimate the posterior distributions of 
    #     model parameters, providing uncertainty quantification and the ability 
    #     to incorporate prior knowledge


    # *********************** the Swedish Fish Company example ***********************
    #
    #                         this is called "approximate Baysian computation"
    #

    # Import libraries
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Number of random draws from the prior
    n_draws = 10000

    # Here you sample n_draws draws from the prior into a pandas Series (to have convenient
    # methods available for histograms and descriptive statistics, e.g. median)
    #
    # In Bayesian statistics, the prior represents initial beliefs about a parameter before 
    # considering data. The prior does not need to be a valid probability distribution (i.e., 
    # a “proper” function that integrates/sums to 1), 
    # but it is always mathematically represented as a function. 
    #

    prior = pd.Series(np.random.uniform(0, 1, size = n_draws), name='values')  
    #     "any success percentage between 0 and 1 is equally likely" 

    #prior.hist() # It's always good to eyeball the prior to make sure it looks ok.
    #plt.show()

    # Here you define the generative model 
    #
    # (given params, generate simulated data numerous times to understand how much the data can change)
    # <or>
    # given data, what are reasonable parameter values that could have generated the data
    #
    # assume there is one rate at which people sign-up for a fish subscription
    # select a specific number of people to "ask" if they want to sign-up 
    # count how many people signed up (this is the "data")
    # do it a lot of times and this is the simulated data
    # "what is likely the rate of sign-up given that 6 of 16 signed-up"


    #see .txt for poisson over-disperion and notice 
    #rng = np.random.default_rng()
    #samples = rng.negative_binomial(n=1, p=0.1, size=100000)

    #Use `negative_binomial` in NumPy when modeling count data with overdispersion, 
    #    #such as insurance claims, disease cases, or equipment failures.
    #For new code, prefer `Generator.negative_binomial` over the legacy `random.negative_binomial`.
    # HOWEVER
    # Low variance: All counts are close to the mean (e.g., 8, 10, 11, 9, 12).
    # High variance: Counts are all over the place (e.g., 2, 4, 40, 1, 25).


    def generative_model(success_probability):
        #return(np.random.binomial(number_independent_trials, success_probability))   # 10 vineyard row positions
        return(np.random.negative_binomial(number_independent_trials, success_probability))    
        # (This simulates the number of successes in 16 independent Bernoulli trials (e.g., coin flips), 
        # where each trial has a probability `prob` of success.) )

        # NB allows for overdispersion (variance > mean), which can stretch its posterior 
        # rightward (higher median) if the data is skewed or has high variance.
        # NB Parameter p: Represents success probability per trial, 
        # but its posterior median depends on both r (dispersion) and μ (mean).


    # Here you simulate data using the parameters from the prior and the 
    # generative model
    sim_data = list()

    for p in prior:
        sim_data.append(generative_model(p))

    # Observed data
    observed_data = number_of_successes # vine positions with spiders
                        
    # Here you filter off all draws that do not match the data.
    posterior = prior[list(map(lambda x: x == observed_data, sim_data))]

    posterior.hist() # Eyeball the posterior
    plt.show()

    filename = './metrics/negative-binomial-posterior-' + csv_ID + '.csv'
    posterior.to_csv(filename, header=True, index=True, mode='w')

    # See that we got enought draws left after the filtering. 
    # There are no rules here, but you probably want to aim for >1000 draws.

    # Posterior Distribution: After observing data, Bayesian inference updates 
    # the prior belief to form the posterior distribution for a parameter.

    # Quantile Interval: A range of parameter values that captures a specified 
    # probability mass (e.g., 95%) from the posterior distribution.

    # Now you can summarize the posterior, where a common summary is to take the mean or the median posterior, 
    # and perhaps a 95% quantile interval.


    print('Number of draws left: %d, Posterior median: %.3f, Posterior quantile interval: %.3f-%.3f' % 
          (len(posterior), posterior.median(), posterior.quantile(.025), posterior.quantile(.975)))

    print('posterior mean: %.3f, Posterior variance: %.3f' % 
          (posterior.mean(), posterior.var()))

    # the 89% central credible interval (equal-tailed interval) of the probability mass is bounded by the 5.5th percentile 
    # and the 94.5th percentile of the posterior distribution.
    # Lower quantile:  (1-0.89)/2 = 0.055
    # Lower quantile:  (1-0.055) = 0.945
    return([posterior.median(), posterior.quantile(.055), posterior.quantile(.945)])


def central_limit(both_transects_dataframe, daytime, file_label):

    # *********************** central limit theorem ***********************
    # *********************** https://www.youtube.com/watch?v=zeJD6dqJ5lo 
    # ***********************       ***********************

    # input daily spider count
    # separate into control and oakMargin = by transect
    # find the max count
    # create the frequency of each count
    # histogram (mean aand confidence interval)
    #

    # Import libraries
    import pandas as pd
    import numpy as np

    df = both_transects_dataframe

    control_df = df[df['transect'] == 'control']
    oakMargin_df = df[df['transect'] == 'oakMargin']

    control_df = control_df.rename(columns={'Thomisidae (crab spider)': 'count'})
    oakMargin_df = oakMargin_df.rename(columns={'Thomisidae (crab spider)': 'count'})


    filename = './metrics/oakMargin_df-' + daytime + file_label + '-raw_count-.csv'
    oakMargin_df.to_csv(filename, header=True, index=True, mode='w')

    filename = './metrics/control_df-' + daytime + file_label + '-raw_count-.csv'
    control_df.to_csv(filename, header=True, index=True, mode='w')

    csv_count_variance(df=oakMargin_df, transect='oakMargin', time=daytime, label=file_label)
    csv_count_variance(df=control_df, transect='control', time=daytime, label=file_label)



    # "from a pandas dataframe column of count data, create a dataframe of normalized probabilities of each count value"

    # df = pd.DataFrame({'count': [3, 2, 3, 1, 2, 3, 1]})
    #### Step 1: Calculate Normalized Probabilities
    # probs = df['count'].value_counts(normalize=True)
    # This returns a Series where the index is the unique count value and the value is its probability.
    #### Step 2: Convert to DataFrame (optional)
    # prob_df = probs.reset_index()
    # prob_df.columns = ['count', 'probability']
    #### Output
    #   count  probability
    # 0      3     0.428571
    # 1      2     0.285714
    # 2      1     0.285714

    probs = oakMargin_df['count'].value_counts(normalize=True)
    prob_oakMargin_df = probs.reset_index()
    prob_oakMargin_df.columns = ['count', 'probability']

    filename = './metrics/oakMargin_df-' + daytime + file_label + '-prob-.csv'
    prob_oakMargin_df.to_csv(filename, header=True, index=True, mode='w')


    probs = control_df['count'].value_counts(normalize=True)
    prob_control_df = probs.reset_index()
    prob_control_df.columns = ['count', 'probability']

    filename = './metrics/control_df-' + daytime + file_label + '-prob-.csv'
    prob_control_df.to_csv(filename, header=True, index=True, mode='w')

    # take samples from the distribution 
    # record the sum (size = 10) of the sample on a plot

    return()


def chopPosition(df, position_list):

    # filtered_df = df[df['col'].isin(['A', 'B', 'C'])]
    filtered_df = df[df['position'].isin(position_list)]


    return(filtered_df)


def chopWeek(df, week_list):

    filtered_df = df[df['week'].isin(week_list)]

    return(filtered_df)

def csv_count_variance(df, transect, time, label):

    import pandas as pd
    import numpy as np

    count_list = []
    count_list = df['count'].astype(int).tolist()
    m = np.mean(count_list)
    v = np.var(count_list)
    s = np.sum(count_list)
    # new record
    record = {'transect' : transect, 'time' : time, 'data_label' : label, 'count' : s, 'mean' : m, 'variance' : v}
    count_variance_df = pd.DataFrame([record])

    filename = './metrics/count-variance.csv'
    count_variance_df.to_csv(filename, header=False, index=False, mode='a')

    print(record)

    return()
