url1 = 'http://tinyurl.com/'
url1FirstMemento = 'http://web.archive.org/web/20020212130833/http://tinyurl.com/'

outputFile = open('sim1.txt', 'a')

allStringsFirstMemento = extractTextForURI(url1FirstMemento)
tokens = allStringsFirstMemento.split(' ')
tokens = list(set(tokens))
firstMementoVersionOneGrams = find_ngrams(tokens, 1)

pages = getMementosPages(url1)
if(len(pages) != 0):
	
	for i in range(0,len(pages)):
		mementos, listOfItemsDateTime = getItemGivenSignature(pages[i])

		for j in range(0, len(mementos)):
			url = mementos[j]
			if( url1FirstMemento != url ):

				#print url
				allStrings = extractTextForURI(url)
				s0Tokens = allStrings.split(' ')
				s0Tokens = list(set(s0Tokens))
				subsequentVersionOneGrams = find_ngrams(s0Tokens, 1)

				#print firstMementoVersionOneGrams
				#print
				#print subsequentVersionOneGrams
				
				oneGramSimilarity = computeJaccardSimilarity(firstMementoVersionOneGrams, subsequentVersionOneGrams)
				print i, len(pages), oneGramSimilarity, listOfItemsDateTime[j]
				outputFile.write(str(oneGramSimilarity) + ' <> ' + listOfItemsDateTime[j] + '\n')