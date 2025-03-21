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


def rough_dataset_clean(records_list, transect, week, time):

    import pandas as pd
    df = pd.DataFrame(records_list)

    # Set the first row as column headers
    df.columns = df.iloc[0]  # Assign first row to columns
    df = df.rename(columns=df.iloc[0]).iloc[1:]  # Remove the first row

    # Filter rows using query()
    df_high_fee = df.query("transect == @transect and time == @time and week == @week ")

    #The `.loc[]` method allows you to select rows and columns by labels. 
    #To select specific columns, use `:` for all rows and specify the column names.
    selected_columns = df_high_fee.loc[:, ['transect', 'row', 'time', 'week', 'julian', 'Thomisidae (crab spider)', 'position']]

    return(selected_columns)


def daily_spider_count(df):

    ########################################################################
    #
    # sum spider counts by julian day
    # input can mix records for 'transect', 'week', and 'time'. 
    # 
    # return a dataframe with text identifiers, a delimeter, and the totalized count by position
    ########################################################################

    # sanity check on the data
    
    unique_weeks = df['week'].unique()
    unique_time = df['time'].unique()

    if len(unique_weeks) != 1:
        # choke
        print("daily_spider_count(): the input dataframe must contain data from only 1 week")
        sys.exit(1)  # graceful exit on error condition with cleanup
    if len(unique_time) != 1:
        # choke
        print("daily_spider_count(): the input dataframe must contain data from only 1 time")
        sys.exit(1)  # graceful exit on error condition with cleanup

    # prep a list of lists to load a dataframe for return
    list_holding_tank = []

    # without specifying the specific vineyard rows sampled, we can sum the spider counts
    # by row for each day for the week and time represented in the dataframe

    # create records that represent the number of spiders occurring in sequential positions
    # read each record, examine the position, and place the spider count for that position in 
    # the matching column. Then we have ordered sequences of counts (that represent a pattern)

    # for each julian day, there are 3 rows that were sampled
    
    unique_julian_list = df['julian'].unique().tolist()

    for k in range(len(unique_julian_list)):
        # use .loc to filter based on julian ID
        temp_julian_df = df.loc[df['julian'] == unique_julian_list[k]]
    
        unique_rows_list = temp_julian_df['row'].unique().tolist()

        # build a sentence in the language of spider counts that will ultimatedly be
        # used to compare to other sentances
        daily_spider_total_int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for j in range(len(unique_rows_list)):
            # use .loc to filter based on row ID
            temp_row_df = temp_julian_df.loc[temp_julian_df['row'] == unique_rows_list[j]]

            for i in range(len(temp_row_df)):

                # write the counts for each position
                # (access a single dataframe value using iloc)
                value = temp_row_df.iloc[i, 5]  #  

                #### useful for debug ####
                # print("julian ", unique_julian_list[k], " row= ", unique_rows_list[j], " value= ", value)
                ####                  ####
                
                # construct a list of counts for 10 positions
                # the counts need to be 'text'
                # the counts are accumulated across the selected rows for each position
                
                daily_spider_total_int[i] = int(temp_row_df.iloc[i, 5]) + daily_spider_total_int[i]
  
    
        # print(daily_spider_total_int)
        # Convert each integer to a string using list comprehension
        # (this s a concise and Pythonic way to convert each integer in the list to a string)
        daily_spider_total_txt = [str(x) for x in daily_spider_total_int]
        #
        # insert context (what julian, time, week, and transect is that daya from)
        # (when you insert an element, all existing elements after the specified index are shifted 
        #  one position to the right)
        daily_spider_total_txt.insert(0, df.iloc[0,0])
        daily_spider_total_txt.insert(0, df.iloc[0,3])
        daily_spider_total_txt.insert(0, df.iloc[0,2])
        daily_spider_total_txt.insert(0, unique_julian_list[k])

        # these are the daily totals, by position, across 3 vineyard rows, for a specific week
        # time and transect
        # print(daily_spider_total_txt)
        #['162', 'am', '24', 'oakMargin', '2', '1', '1', '0', '1', '0', '2', '1', '0', '0']
        #['163', 'am', '24', 'oakMargin', '1', '1', '0', '1', '2', '3', '6', '1', '1', '2']
        #['164', 'am', '24', 'oakMargin', '2', '2', '2', '3', '1', '1', '4', '4', '0', '2']

        
        list_holding_tank.insert(0, daily_spider_total_txt)

    # that's a list of lists
    # print(list_holding_tank)
    # [['164', 'am', '24', 'oakMargin', '2', '2', '2', '3', '1', '1', '4', '4', '0', '2'], 
    #  ['163', 'am', '24', 'oakMargin', '1', '1', '0', '1', '2', '3', '6', '1', '1', '2'], 
    #  ['162', 'am', '24', 'oakMargin', '2', '1', '1', '0', '1', '0', '2', '1', '0', '0']]

    # build a dataframe
    import pandas as pd
    df = pd.DataFrame(list_holding_tank, columns=['julian', 'time', 'week', 'transect', 
                                                 'p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9'])

    # print(df)
    #   julian time week   transect p0 p1 p2 p3 p4 p5 p6 p7 p8 p9
    # 0    164   am   24  oakMargin  2  2  2  3  1  1  4  4  0  2
    # 1    163   am   24  oakMargin  1  1  0  1  2  3  6  1  1  2
    # 2    162   am   24  oakMargin  2  1  1  0  1  0  2  1  0  0

    # # Insert a delimeter (index 4) to support string truncation 
    df.insert(4, 'delimeter', ':')

    #     julian time week   transect delimeter p0 p1 p2 p3 p4 p5 p6 p7 p8 p9
    # 0     164   am   24  oakMargin         :  2  2  2  3  1  1  4  4  0  2
    # 1     163   am   24  oakMargin         :  1  1  0  1  2  3  6  1  1  2
    # 2     162   am   24  oakMargin         :  2  1  1  0  1  0  2  1  0  0
    #    julian time week transect delimeter p0 p1 p2 p3 p4 p5 p6 p7 p8 p9
    # 0     164   am   24  control         :  2  0  1  2  1  2  0  2  5  2
    # 1     163   am   24  control         :  0  2  2  2  1  0  1  0  3  4
    # 2     162   am   24  control         :  1  0  1  1  1  0  0  1  1  0

    return(df)



def df_to_corpus_text(df_list):

    #selected_columns = df.loc[:, ['transect', 'row', 'time', 'week', 'julian', 'Thomisidae (crab spider)', 'position']]
    #df = df.loc[:, ['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9']]

    corpus = []

    for k in range(len(df_list)):
        
        df = df_list[k]
        
        for i in range(len(df)): 
            # Read the first row and concatenate values into a single line
            row = df.iloc[i]
            row_string = ' '.join(row.astype(str))
            #print(row_string) 
            
            corpus.insert(0, row_string)

    return(corpus)

    
def row_text_to_three_words(text):

    ###############################################################################
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

    # input:  162 am 24 control : 1 0 1 1 1 0 0 1 1 0
    #         (part2_no_spaces  1011100110)
    # output: 162 am 24 control  ,  TRUEfalseTRUE TRUETRUEfalse falseTRUETRUE false
    # 
    # input:  163 am 24 control : 0 2 2 2 1 0 1 0 3 4
    #         (part2_no_spaces  0222101034)
    # output: 163 am 24 control  ,  falseTRUETRUE TRUETRUEfalse TRUEfalseTRUE TRUE
    #
    # input:  164 am 24 control : 2 0 1 2 1 2 0 2 5 2
    #         (part2_no_spaces  2012120252)
    # output: 164 am 24 control  ,  TRUEfalseTRUE TRUETRUETRUE falseTRUETRUE TRUE

    ###############################################################################



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

    if part2_no_spaces[0] == "0":
        word_one = "false"
    else:
        word_one = "TRUE"

    if part2_no_spaces[1] == "0":
        word_one = word_one + "false"
    else:
        word_one = word_one + "TRUE"

    if part2_no_spaces[2] == "0":
        word_one = word_one + "false"
    else:
        word_one = word_one + "TRUE"


    if part2_no_spaces[3] == "0":
        word_two = "false"
    else:
        word_two = "TRUE"

    if part2_no_spaces[4] == "0":
        word_two = word_two + "false"
    else:
        word_two = word_two + "TRUE"

    if part2_no_spaces[5] == "0":
        word_two = word_two + "false"
    else:
        word_two = word_two + "TRUE"


    if part2_no_spaces[6] == "0":
        word_three = "false"
    else:
        word_three = "TRUE"

    if part2_no_spaces[7] == "0":
        word_three = word_three + "false"
    else:
        word_three = word_three + "TRUE"

    if part2_no_spaces[8] == "0":
        word_three = word_three + "false"
    else:
        word_three = word_three + "TRUE"


    if part2_no_spaces[9] == "0":
        word_four = "false"
    else:
        word_four = "TRUE"



    result = word_one + " " + word_two + " " + word_three + " " + word_four

    # print(part1, ", ", result)

    # (showing 3 different results for clarification, only 1 returned per)
    # 162 am 24 oakMargin  ,  TRUETRUETRUE falseTRUEfalse TRUETRUEfalse false
    # 163 am 24 oakMargin  ,  TRUETRUEfalse TRUETRUETRUE TRUETRUETRUE TRUE
    # 164 am 24 oakMargin  ,  TRUETRUETRUE TRUETRUETRUE TRUETRUEfalse TRUE

    # returning the context string and the 3 encoded words in a string (= 'sentence')


    return([part1, result])




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
    week_records_df = rough_dataset_clean(records_list, transect, week, time)
    # get the daily counts by combining counts for the vineyard rows that were sampled
    df = daily_spider_count(df=week_records_df)

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

    