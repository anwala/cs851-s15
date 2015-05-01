# precondition: all tuples are from a set - no repetition
def computeJaccardSimilarity(firstListOfTuples, secondListOfTuples):

	similarity = -1
	if( len(firstListOfTuples) != 0 and len(secondListOfTuples) != 0 ):
		
		intersectionCount = 0
		unionDict = {}

		for firstTuple in firstListOfTuples:
			for secondTuple in secondListOfTuples:
				if( len(firstTuple) == len(secondTuple) ):

					unionDict.setdefault(firstTuple, 0)
					unionDict.setdefault(secondTuple, 0)

					if( firstTuple == secondTuple ):
						intersectionCount = intersectionCount + 1
		similarity = intersectionCount / (float) (len(unionDict))

	return similarity

def genericSimilarity(s0Dict, s1Dict):

	#print computeJaccardSimilarity( flt0, flt1 )
	if( len(s0Dict) != 0 and len(s1Dict) != 0 ):

		count = 0
		for url, plaintext in s0Dict.items():
			if url in s1Dict:
				count += 1
				allStrings = consolidateListOfStringsAndMakeSet( s0Dict[url] )
				s0Tokens = allStrings.split(' ')
				s0Tokens = list(set(s0Tokens))

				allStrings = consolidateListOfStringsAndMakeSet( s1Dict[url] )
				s1Tokens = allStrings.split(' ')
				s1Tokens = list(set(s1Tokens))

				firstVersionOneGrams = find_ngrams(s0Tokens, 1)
				firstVersionTwoGrams = find_ngrams(s0Tokens, 2)
				firstVersionThreeGrams = find_ngrams(s0Tokens, 3)

				secondVersionOneGrams = find_ngrams(s1Tokens, 1)
				secondVersionTwoGrams = find_ngrams(s1Tokens, 2)
				secondVersionThreeGrams = find_ngrams(s1Tokens, 3)

				oneGramSimilarity = computeJaccardSimilarity(firstVersionOneGrams, secondVersionOneGrams)
				
				twoGramSimilarity = computeJaccardSimilarity(firstVersionTwoGrams, secondVersionTwoGrams)

				threeGramSimilarity = computeJaccardSimilarity(firstVersionThreeGrams, secondVersionThreeGrams)

				print count, (oneGramSimilarity*100), (twoGramSimilarity*100), (threeGramSimilarity*100)
			else:
				print 'NOT: ', url