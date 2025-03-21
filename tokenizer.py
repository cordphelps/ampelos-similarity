def tokenizer(sample1, sample2):

	# 
	import torch
	from transformers import BertTokenizer, BertModel

	# Load pre-trained BERT model and tokenizer
	tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
	model = BertModel.from_pretrained('bert-base-uncased')

	# Convert samples to text representations
	#sample1 = "0 2 1 3 0 1 2 0 1 0"
	#sample2 = "1 1 2 2 1 0 1 1 0 0"
	


	# Tokenize and get embeddings
	inputs1 = tokenizer.encode_plus(sample1, 
	                                  add_special_tokens=True, 
	                                  max_length=10, 
	                                  return_attention_mask=True, 
	                                  return_tensors='pt')
	inputs2 = tokenizer.encode_plus(sample2, 
	                                  add_special_tokens=True, 
	                                  max_length=10, 
	                                  return_attention_mask=True, 
	                                  return_tensors='pt')

	# Get embeddings
	outputs1 = model(inputs1['input_ids'], attention_mask=inputs1['attention_mask'])
	outputs2 = model(inputs2['input_ids'], attention_mask=inputs2['attention_mask'])

	# Calculate similarity using cosine similarity
	from sklearn.metrics.pairwise import cosine_similarity
	similarity = cosine_similarity(outputs1.last_hidden_state[:, 0, :].detach().numpy(), 
	                                outputs2.last_hidden_state[:, 0, :].detach().numpy())


	return(similarity)

