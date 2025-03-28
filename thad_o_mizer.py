

# 
import torch
from transformers import BertTokenizer, BertModel

from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

import spider_lib 

# Load a pre-trained Transformer model and tokenizer
model_name = "sentence-transformers/all-MiniLM-L6-v2"  # A lightweight sentence embedding model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


# Function to compute sentence embeddings
def get_sentence_embeddings(sentences):
    # Tokenize the input sentences
    inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
    
    # Get the output embeddings from the model
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Use the mean of the token embeddings (excluding [CLS] and [SEP]) as the sentence embedding
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings


# Function to compute cosine similarity between two sentences
def compute_cosine_similarity(sentence1, sentence2):
    # Get embeddings for both sentences
    embeddings = get_sentence_embeddings([sentence1, sentence2])
    
    # Convert PyTorch tensors to numpy arrays for compatibility with sklearn
    embeddings = embeddings.numpy()
    
    # Compute cosine similarity
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])

    return similarity[0][0]


###################################################################################
#  Use N-grams to Capture Word Sequences
#  Instead of representing sentences as a bag of words (which ignores order), 
#  use n-grams to capture sequences of words.
#  Explanation: By using bigrams or trigrams, the vector representation includes 
#  information about adjacent words, thus incorporating word order.

# Function to compute cosine similarity between two sentences
def compute_cosine_similarity_ngram(sentence1, sentence2):
    
	from sklearn.feature_extraction.text import TfidfVectorizer
	from sklearn.metrics.pairwise import cosine_similarity

	# Sample sentences
	sentence1 = "I love programming"
	#sentence2 = "Programming love I"
	sentence2 = "I love hc Programming"

	# Custom stop words
	custom_stop_words = ['hoser']

	# Use n-grams (e.g., bigrams) in TF-IDF
	vectorizer = TfidfVectorizer(ngram_range=(2, 2), stop_words=custom_stop_words)  # Use bigrams
	vectors = vectorizer.fit_transform([sentence1, sentence2])

	# Compute cosine similarity
	similarity = cosine_similarity(vectors[0], vectors[1])

	print("ngram similarity : ", similarity)


	return similarity[0][0]



###################################################################################
#   N-gram quick
#
def compute_ngram_quick(sentence1, sentence2):

	import ngram

	# Compare two strings using n-grams
	# similarity = ngram.NGram.compare('Ham', 'Spam', N=1) # Output: 0.4

	# bigram : N=2
	similarity = ngram.NGram.compare(sentence1, sentence2, N=2)

	return(similarity)  




###################################################################################
# the Levenshtein distance calculates the distance, which represents the minimum number 
# of edits (insertions, deletions, or substitutions) required to transform one sentence 
# into another.
#
def levenshtein_distance(sentence1, sentence2):
    # Tokenize sentences into words
    words1 = sentence1.split()
    words2 = sentence2.split()

    # Initialize the matrix
    n = len(words1)
    m = len(words2)
    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    # Fill the first row and column
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    # Fill the rest of the matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if words1[i - 1] == words2[j - 1]:  # No edit required
                dp[i][j] = dp[i - 1][j - 1]
            else:  # Minimum of insertion, deletion, or substitution
                dp[i][j] = min(
                    dp[i - 1][j] + 1,   # Deletion
                    dp[i][j - 1] + 1,   # Insertion
                    dp[i - 1][j - 1] + 1  # Substitution
                )

    # Return the Levenshtein distance (bottom-right corner of the matrix)
    return dp[n][m]


def stacked_df_similarity(df, raw):

	###################################################################################
	#
	# add similarity metrics to the df
	#
	#
	###################################################################################

	import pandas as pd

	# chop out columns p0 through p9 to make some room
	df = df.drop(['p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9'], axis=1)

	unique_julian = []
	unique_time = []

	unique_julian = df['julian'].unique()
	unique_time = df['time'].unique()

	#       transect time  ...    squashed                                        transformed
	# 0      control   am  ...  0000000000  falsefalsefalse falsefalsefalse falsefalsefals...
	# 1      control   am  ...  0000000000  falsefalsefalse falsefalsefalse falsefalsefals...
	# 2      control   am  ...  0000000010  falsefalsefalse falsefalsefalse falsefalseTRUE...
	# 3      control   pm  ...  0000000011  falsefalsefalse falsefalsefalse falsefalseTRUE...
	# 4      control   pm  ...  0100000000  falseTRUEfalse falsefalsefalse falsefalsefalse...
	# ..         ...  ...  ...         ...                                                ...
	# 117  oakMargin   am  ...  1200002001  TRUETRUEfalse falsefalsefalse TRUEfalsefalse TRUE
	# 118  oakMargin   am  ...  0100002000  falseTRUEfalse falsefalsefalse TRUEfalsefalse ...
	# 119  oakMargin   pm  ...  1312001223      TRUETRUETRUE TRUEfalsefalse TRUETRUETRUE TRUE
	# 120  oakMargin   pm  ...  0011301010   falsefalseTRUE TRUETRUEfalse TRUEfalseTRUE false
	# 121  oakMargin   pm  ...  0000201110  falsefalsefalse falseTRUEfalse TRUETRUETRUE false
	# 
	# [122 rows x 7 columns]

	incoming_df = df

	if not raw:

		# this is the compare "oakMargin to control" logic (raw == FALSE)
		# this function is designed to compare oakMargin records to matching control 
		# records based on an assumption of how the corpus is assembled

		# compare each sentance to its pair usually originalint from the oakMargin and control 
		# transects from the same time period.

		transect_compare_df = pd.DataFrame(columns=['julian', 'time', 'NGRAM cosine similarity', 'flip NGRAM CS','levenshtein_distance', 'LD flip'])

		for julian in unique_julian:

			for time in unique_time:

				filtered_df = incoming_df.query( f" julian == '{julian}' and time == '{time}' ")

				# that should be two records (oakMargin and control)

				#       transect time  ...    squashed                                    transformed
				# 50     control   am  ...  2012120252  TRUEfalseTRUE TRUETRUETRUE falseTRUETRUE TRUE
				# 111  oakMargin   am  ...  2223114402   TRUETRUETRUE TRUETRUETRUE TRUETRUEfalse TRUE
				# 
				# [2 rows x 7 columns]

				if len(filtered_df) != 2:  # something broke
					print("******** stacked_df_similarity() choked ************")
					print(filtered_df)
					break

				# access row and column value by index
				s1_text = df.iat[1, 6]
				s2_text = df.iat[2, 6]

				print("******** ssentence1 sentence2 ************")
				print(s1_text, " :::::::::::::: \n", s2_text, " :::::::::::::: ", )


				cs_real = compute_ngram_quick(sentence1 = s1_text, sentence2 = s2_text)
				cs_real_flip = compute_ngram_quick(sentence1 = s2_text, sentence2 = s1_text)
				ld_int = levenshtein_distance(sentence1 = s1_text, sentence2 = s2_text)
				ld_int_flip = levenshtein_distance(sentence1 = s2_text, sentence2 = s1_text)

				print("******** ssentence1 sentence2 ************")
				print(s1_text, " :::::::::::::: ", s2_text, " :::::::::::::: ", )

				new_record = pd.DataFrame([{'julian': julian, 'time': time, 'NGRAM cosine similarity' : cs_real, 'flip NGRAM CS' : cs_real_flip,'levenshtein_distance' : ld_int, 'LD flip' : ld_int_flip}])
				transect_compare_df = pd.concat([transect_compare_df, new_record], ignore_index=True)

				print(">>>>>>>>>>>>>>>>>>. new_record >>>>>>>>>>>>>>>>>>>")
				print(new_record)
				print(">>>>>>>>>>>>>>>>>>. end new_record >>>>>>>>>>>>>>>>>>>")


	return(transect_compare_df)



def stacked_similarity(corpus, raw):



	###########################################################################
	# 
	# with raw == TRUE, 
	# each row ('sentence') is compared to itself and every other row
	#
	# input: # [
	#  ['162 am 24 control ', 'TRUEfalseTRUE TRUETRUEfalse falseTRUETRUE false'],
	#  ['163 am 24 control ', 'falseTRUETRUE TRUETRUEfalse TRUEfalseTRUE TRUE'],
	#  ['164 am 24 control ', 'TRUEfalseTRUE TRUETRUETRUE falseTRUETRUE TRUE']
	# ]
	#
	# CAUTION: with raw == FALSE,
	# this function is designed to compare oakMargin records to matching control 
	# records based on an assumption of how the corpus is assembled
	#
	# input: # [
	#  ['162 am 24 oakMargin ', 'TRUETRUETRUE falseTRUEfalse TRUETRUEfalse false'],
	#  ['163 am 24 oakMargin ', 'TRUETRUEfalse TRUETRUETRUE TRUETRUETRUE TRUE'],
	#  ['164 am 24 oakMargin ', 'TRUETRUETRUE TRUETRUETRUE TRUETRUEfalse TRUE'],
	#  ['162 am 24 control '  , 'TRUEfalseTRUE TRUETRUEfalse falseTRUETRUE false'],
	#  ['163 am 24 control '  , 'falseTRUETRUE TRUETRUEfalse TRUEfalseTRUE TRUE'],
	#  ['164 am 24 control '  , 'TRUEfalseTRUE TRUETRUETRUE falseTRUETRUE TRUE']
	# ]
	#
	###########################################################################

	import numpy as np
	import pandas as pd
	

	number_of_sentences = len(corpus)

	prefix_text1 = []
	prefix_text2 = []


	if raw:

		# this is the "compare every record to every oher record" logic (raw == TRUE)

		# the corpus should only respresent data from one transect
		# compare each sentance to the others
		# a week of data represents 3 vineyard rows in one transect. 

		# numpy array set to 0s
		# first column is the cosine similarity of 2 sentences
		# second column is the levenshtein distance of 2 sentences

		# define a mixed numpy array
		np_array = np.zeros((number_of_sentences, number_of_sentences, 8), dtype=object)

	
		for k in range(number_of_sentences):

			for j in range(number_of_sentences):

				np_array[k, j, 0] = compute_cosine_similarity(sentence1 = corpus[k][1], sentence2 = corpus[j][1])

				print(corpus[k][1], " cosine:  ", corpus[j][1], "similarity: ", np_array[k, j, 0])

				np_array[k, j, 1] = levenshtein_distance(sentence1 = corpus[k][1], sentence2 = corpus[j][1])
				np_array[k, j, 2] = compute_ngram_quick(sentence1 = corpus[k][1], sentence2 = corpus[j][1])

				# flip the order to confirm the calculations

				np_array[k, j, 3] = compute_cosine_similarity(sentence1 = corpus[k][1], sentence2 = corpus[j][1])
				np_array[k, j, 4] = levenshtein_distance(sentence1 = corpus[k][1], sentence2 = corpus[j][1])
				np_array[k, j, 5] = compute_ngram_quick(sentence1 = corpus[k][1], sentence2 = corpus[j][1])

				np_array[k, j, 6] = corpus[k][0]
				np_array[k, j, 7] = corpus[j][0]

		# Flatten the first two dimensions into one
		np_array = np_array.reshape(-1, np_array.shape[-1])

		df = pd.DataFrame(np_array)

		# print(np_array)

		# [[0.9999999  0 1.0                0.9999999  0 1.0                '162 am 24 control ' '162 am 24 control ']
		#  [0.97768813 3 0.7272727272727273 0.97768813 3 0.7272727272727273 '162 am 24 control ' '163 am 24 control ']
  		#  [0.95014405 2 0.6206896551724138 0.95014405 2 0.6206896551724138 '162 am 24 control ' '164 am 24 control ']
		#  [0.97768813 3 0.7272727272727273 0.97768813 3 0.7272727272727273 '163 am 24 control ' '162 am 24 control ']

		#  [1.0        0 1.0                1.0        0 1.0                '163 am 24 control ' '163 am 24 control ']
		#  [0.9795705  3 0.7222222222222222 0.9795705  3 0.7222222222222222 '163 am 24 control ' '164 am 24 control ']
		#  [0.95014405 2 0.6206896551724138 0.95014405 2 0.6206896551724138 '164 am 24 control ' '162 am 24 control ']
  		#  [0.9795705  3 0.7222222222222222 0.9795705  3 0.7222222222222222 '164 am 24 control ' '163 am 24 control ']
		#  [1.0000001  0 1.0                1.0000001  0 1.0                '164 am 24 control ' '164 am 24 control ']]

		# print(df)

		#           0  1         2         3  4         5                  6                   7
		# 0       1.0  0       1.0       1.0  0       1.0  162 am 24 control   162 am 24 control 
		# 1  0.977688  3  0.727273  0.977688  3  0.727273  162 am 24 control   163 am 24 control 
		# 2  0.950144  2   0.62069  0.950144  2   0.62069  162 am 24 control   164 am 24 control 
		# 3  0.977688  3  0.727273  0.977688  3  0.727273  163 am 24 control   162 am 24 control 
		# 4       1.0  0       1.0       1.0  0       1.0  163 am 24 control   163 am 24 control 
		# 5  0.979571  3  0.722222  0.979571  3  0.722222  163 am 24 control   164 am 24 control 
		# 6  0.950144  2   0.62069  0.950144  2   0.62069  164 am 24 control   162 am 24 control 
		# 7  0.979571  3  0.722222  0.979571  3  0.722222  164 am 24 control   163 am 24 control 
		# 8       1.0  0       1.0       1.0  0       1.0  164 am 24 control   164 am 24 control


	else:

		# this is the compare "oakMargin to control" logic (raw == FALSE)
		# this function is designed to compare oakMargin records to matching control 
		# records based on an assumption of how the corpus is assembled

		# compare each sentance to its pair usually originalint from the oakMargin and control 
		# transects from the same time period.
		
		#
		# check if input records are an even number
		# (the numpy array is expected to be 'square') 
		#
		if len(corpus) % 2 != 0:
			print("The length is not an even integer.")
			return(np.zeros((1, 1), dtype=int))
		#

		# get the length of the large array (6)
		array_dimension = int(number_of_sentences/2)

		# numpy array set to 0s
		# first column is the cosine similarity of 2 sentences
		# second column is the levenshtein distance of 2 sentences
		# define a mixed numpy array
		np_array = np.zeros((array_dimension, 8), dtype=object)


		for k in range(array_dimension):

			# compare the first half to the second half
			# (this is the "oakMargin to control" model)

			np_array[k, 0] = compute_cosine_similarity(sentence1 = corpus[k][1], sentence2 = corpus[k + array_dimension][1])
			np_array[k, 1] = levenshtein_distance(sentence1 = corpus[k][1], sentence2 = corpus[k + array_dimension][1])
			np_array[k, 2] = compute_ngram_quick(sentence1 = corpus[k][1], sentence2 = corpus[k + array_dimension][1])

			# flip the order to confirm the calculations

			np_array[k, 3] = compute_cosine_similarity(sentence1 = corpus[k + array_dimension][1], sentence2 = corpus[k][1])
			np_array[k, 4] = levenshtein_distance(sentence1 = corpus[k + array_dimension][1], sentence2 = corpus[k][1])
			np_array[k, 5] = compute_ngram_quick(sentence1 = corpus[k + array_dimension][1], sentence2 = corpus[k][1])

			np_array[k, 6] = corpus[k][0]
			np_array[k, 7] = corpus[k + array_dimension][0]

		# Flatten the first two dimensions into one
		np_array = np_array.reshape(-1, np_array.shape[-1])

		df = pd.DataFrame(np_array)

		# print(np_array)

		# [[0.9709183  3 0.92               0.9709183  3 0.92               '162 am 24 oakMargin ' '162 am 24 control ']
		#  [0.94415224 3 0.6140350877192983 0.94415224 3 0.6140350877192983 '163 am 24 oakMargin ' '163 am 24 control ']
		#   0.94685566 2 0.7169811320754716 0.9468557 2  0.7169811320754716 '164 am 24 oakMargin ' '164 am 24 control ']]

		# print(df)

		# 0  1         2            ...         5                    6                   7
		# 0  0.970918  3      0.92  ...      0.92  162 am 24 oakMargin   162 am 24 control 
		# 1  0.944152  3  0.614035  ...  0.614035  163 am 24 oakMargin   163 am 24 control 
		# 2  0.946856  2  0.716981  ...  0.716981  164 am 24 oakMargin   164 am 24 control 

		#[3 rows x 8 columns]


	df.columns = ['BOW cosine similarity', 'levenshtein distance', 
	'NGRAM cosine similarity', 'BPW flip', 'LD flip', 'NGRAM flip', 'data ID 1', 'data ID 2']

	return( df )

