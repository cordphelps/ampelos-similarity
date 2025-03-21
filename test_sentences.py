
def s1_s2():

	#s1 = '162 am 24 oakMargin 2 1 1 0 1 0 2 1 0 0'
	#s2 = '164 am 24 oakMargin 2 2 2 3 1 1 4 4 0 2'
	# 0.86889887
	#
	#s1 = '2 1 1 0 1 0 2 1 0 0'
	#s2 = '2 2 2 3 1 1 4 4 0 2'
	# 0.84713835
	# 
	#s1 = '162 am 24 oakMargin 2 1 1 0 1 0 2 1 0 0'
	#s2 = '164 am 24 control 2 2 2 3 1 1 4 4 0 2'
	# 0.6710193
	# 
	s1 = '162 am 24 oakMargin 2 1 1 0 1 0 2 1 0 0'
	s2 = '162 am 24 control 2 2 2 3 1 1 4 4 0 2'
	# 0.75689423 
	# 
	s1 = '162 am 24 oakMargin 0 0 0 0 0 1 1 1 1 1'
	s2 = '162 am 24 control 1 1 1 1 1 0 0 0 0 0'
	#  0.76549196
	# 
	s1 = '0 0 0 0 0 1 1 1 1 1'
	s2 = '1 1 1 1 1 0 0 0 0 0'
	# 0.96113205

	# result = thad_o_mizer.compute_cosine_similarity(sentence1=s1, sentence2=s2)


	s1 = 'zero zero zero zero zero one one one one one'
	s2 = 'one one one one one zero zero zero zero zero'
	# 0.9418598128719009 

	#s1 = 'zero zero'
	#s2 = 'one one'
	# 0.0

	#s1 = 'zero one'
	#s2 = 'one zero'
	# 0.0

	#s1 = 'zero one one zero'
	#s2 = 'one zero one zero'
	# 0.6728984701822545 
	#2

	s1 = 'one one one zero'
	s2 = 'one zero one zero'
	# 0.27423415918033694
	# 1

	#s1 = 'TRUEFALSETRUE TRUETRUETRUE FALSEFALSEFALSETRUE'
	#s2 = 'FALSEFALSEFALSEFALSE TRUETRUETRUE TRUETRUETRUE'
	# 0.0

	#s1 = 'TRUEFALSETRUE falsefalsefalse FALSEFALSEFALSETRUE'
	#s2 = 'FALSEFALSEFALSEFALSE TRUETRUETRUE FALSEFALSEFALSETRUE'
	# 0.
	# 2

	s1 = 'TRUEFALSETRUE TRUETRUETRUE FALSEFALSEFALSETRUE'
	s2 = 'FALSEfalseFALSE TRUETRUETRUE FALSEFALSEFALSETRUE'
	# 0.33609692727625756
	# 1

	#s1 = 'TRUEFALSETRUE TRUETRUETRUE FALSEFALSEFALSETRUE TRUEFALSETRUE TRUETRUETRUE FALSEFALSEFALSETRUE'
	#s2 = 'FALSEFALSEFALSEFALSE TRUETRUETRUE TRUETRUETRUE TRUEFALSETRUE TRUETRUETRUE FALSEFALSEFALSETRUE'
	# 0.4498517039243882
	#2


	return([s1, s2])
