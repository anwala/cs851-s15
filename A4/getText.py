import justext
import urllib2
import sys, os

import os, sys
import commands
import json
import requests
from datetime import datetime

globalMementoUrlDateTimeDelimeter = "*+*+*"
# getText.py - start
def getInput(filename):

	filename = filename.strip()
	if(len(filename) == 0):
		return []

	lines = []
	try:
		inputFile = open(filename, 'r')
		lines = inputFile.readlines()
		inputFile.close()
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(fname, exc_tb.tb_lineno, sys.exc_info() )

	return lines

def extractTextForURI(URI):
	page = urllib2.urlopen(URI).read()
	paragraphs = justext.justext(page, justext.get_stoplist('English'))

	allText = ''
	for paragraph in paragraphs:
		if paragraph['class'] == 'good':
			processedText = paragraph['text']
			processedText = processedText.encode('ascii', 'ignore')

			allText += processedText

	return allText

def extractText(listOfURIs):

	if( len(listOfURIs) == 0 ):
		return

	try:
		outputFile = open('urlsPlaintext.txt', 'w')
		statOutputFile = open('urlsStat.txt', 'w')
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(fname, exc_tb.tb_lineno, sys.exc_info() )
		return

	alreadyAddedList = []
	for i in range(0, len(listOfURIs) ):

		try:
			URI = listOfURIs[i].strip()

			page = urllib2.urlopen(URI).read()
			#paragraphs = justext.justext(page, set("~"))
			paragraphs = justext.justext(page, justext.get_stoplist('English'))


			for paragraph in paragraphs:
				if paragraph['class'] == 'good':
					processedText = paragraph['text']

					processedText = processedText.encode('ascii', 'ignore')
					outputFile.write(URI + ':\n' + processedText + '\n\n')
				else:
					print 'class:', paragraph['class']

					if( URI in alreadyAddedList ):
						pass
					else:
						statOutputFile.write(URI + ' bad\n\n')
						alreadyAddedList.append(URI)
					
					print
		except:
			statOutputFile.write(URI + ': ERROR\n\n')
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )
			print
	outputFile.close()
	statOutputFile.close()
					
#lines = getInput('linksFile.txt')
#extractText(lines)

# getText.py - end

def getListPair(fileName0, fileName1):

	fileName0 = fileName0.strip()
	if( len(fileName0) == 0 ):
		return [], []

	fileName1 = fileName1.strip()
	if( len(fileName1) == 0 ):
		return [], []

	lines0 = []
	lines1 = []
	try:
		inputFile = open(fileName0, 'r')
		lines0 = inputFile.readlines()
		inputFile.close()

		inputFile = open(fileName1, 'r')
		lines1 = inputFile.readlines()
		inputFile.close()		
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(fname, exc_tb.tb_lineno, sys.exc_info() )
		return

	return lines0, lines1

def getDictFromUrlsPlaintextList(lines):

	if( len(lines) == 0 ):
		return {}

	urlsTextDict = {}
	previousURL = ''
	for i in range(0, len(lines)):
		l = lines[i].strip()

		if( l.find('http://') == 0 ):
			previousURL = l
			urlsTextDict.setdefault(l, [])
		else:
			urlsTextDict[previousURL].append(l)

	return urlsTextDict

def getDictPair(lines0, lines1):

	if( len(lines0) == 0 or len(lines1) == 0 ):
		return {}, {}

	urlsTextDict0 = {}
	urlsTextDict1 = {}
	
	urlsTextDict0 = getDictFromUrlsPlaintextList(lines0)
	urlsTextDict1 = getDictFromUrlsPlaintextList(lines1)

	return urlsTextDict0, urlsTextDict1

# http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
# precondition: n>1
def find_ngrams(input_list, n):
	return zip(*[input_list[i:] for i in range(n)])

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

#1b
def consolidateListOfStringsAndMakeSet(listOfStrings):

	consolidatedString = ''
	for l in listOfStrings:
			consolidatedString += l
	
	return consolidatedString

#1b
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

def getItemGivenSignature(page):

	listOfItems = []
	if( len(page) > 0 ):
		page = page.splitlines()
		for line in page:
			if(line.find('memento";') != -1):
				#uriRelDateTime: ['<http://www.webcitation.org/64ta04WpM>', ' rel="first memento"', ' datetime="Mon, 23 Jan 2012 02:01:29 GMT",']
				uriRelDateTime = line.split(';')
				if( len(uriRelDateTime) > 2 ):
					if( uriRelDateTime[0].find('://') != -1 ):
						if( uriRelDateTime[2].find('datetime="') != -1 ):


							uri = ''
							uri = uriRelDateTime[0].split('<')
							#print uri
							if( len(uri) > 1 ):
								uri = uri[1].replace('>', '')
								uri = uri.strip()

							datetime = ''
							datetime = uriRelDateTime[2].split('"')
							if( len(datetime) > 1 ):
								datetime = datetime[1]
							
							if( len(uri) != 0 and len(datetime) != 0 ):
								#print uri, '---', datetime
								#listOfItems.append(uri + globalMementoUrlDateTimeDelimeter + datetime)
								listOfItems.append(uri)

	return listOfItems

def getMementosPages(url):

	pages = []
	url = url.strip()
	if(len(url)>0):

		firstChoiceAggregator = "http://timetravel.mementoweb.org/timemap/json/"
		timemapPrefix = firstChoiceAggregator + url
		#timemapPrefix = 'http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/' + url

		'''
			The CS memento aggregator payload format:
				[memento, ..., memento, timemap1]; timemap1 points to next page
			The LANL memento aggregator payload format:
				1. [timemap1, ..., timemapN]; timemapX points to mementos list
				2. [memento1, ..., mementoN]; for small payloads

			For LANL Aggregator: The reason the link format is used after retrieving the payload
								 with json format is due to the fact that the underlying code is based
								 on the link format structure. json format was not always the norm 
		'''



		#select an aggregator - start
		aggregatorSelector = ''

		co = 'curl --silent -I ' + timemapPrefix
		head = commands.getoutput(co)

		indexOfFirstNewLine = head.find('\n')
		if( indexOfFirstNewLine > -1 ):

			if( head[:indexOfFirstNewLine].split(' ')[1] != '200' ):
				firstChoiceAggregator = "http://mementoproxy.cs.odu.edu/aggr/timemap/link/1/"
				timemapPrefix = firstChoiceAggregator + url

		if( firstChoiceAggregator.find('cs.odu.edu') > -1 ):
			aggregatorSelector = 'CS'
		else:
			aggregatorSelector = 'LANL'

		#print '...using aggregator:', aggregatorSelector
		#select an aggregator - end

		#CS aggregator
		if( aggregatorSelector == 'CS' ):
			while( True ):
				#old: co = 'curl --silent ' + timemapPrefix
				#old: page = commands.getoutput(co)

				
				page = ''
				r = requests.get(timemapPrefix)
				print 'status code:', r.status_code
				if( r.status_code == 200 ):
					page = r.text

				pages.append(page)
				indexOfRelTimemapMarker = page.rfind('>;rel="timemap"')

				if( indexOfRelTimemapMarker == -1 ):
					break
				else:
					#retrieve next timemap for next page of mementos e.g retrieve url from <http://mementoproxy.cs.odu.edu/aggr/timemap/link/10001/http://www.cnn.com>;rel="timemap"
					i = indexOfRelTimemapMarker -1
					timemapPrefix = ''
					while( i > -1 ):
						if(page[i] != '<'):
							timemapPrefix = page[i] + timemapPrefix
						else:
							break
						i = i - 1
		else:
			#LANL Aggregator
			#old: co = 'curl --silent ' + timemapPrefix
			#old: page = commands.getoutput(co)

			page = ''
			r = requests.get(timemapPrefix)
			if( r.status_code == 200 ):
				page = r.text

			try:
				payload = json.loads(page)

				if 'timemap_index' in payload:

					for timemap in payload['timemap_index']:
						
						timemapLink = timemap['uri'].replace('/timemap/json/', '/timemap/link/')
						#old: co = 'curl --silent ' + timemapLink
						#old: page = commands.getoutput(co)
						#old: pages.append(page)
						r = requests.get(timemapLink)
						if( r.status_code == 200 ):
							pages.append(r.text)
					
				elif 'mementos' in payload:
					#untested block
					timemapLink = payload['timemap_uri']['json_format'].replace('/timemap/json/', '/timemap/link/')
					#old: co = 'curl --silent ' + timemapLink
					#old: page = commands.getoutput(co)
					#old: pages.append(page)

					print 'timemap:', timemapLink
					r = requests.get(timemapLink)
					if( r.status_code == 200 ):
						pages.append(r.text)
					
				
				
			except:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(fname, exc_tb.tb_lineno, sys.exc_info() )

			
			
	return pages

def getFirstMemento(url):

	url = url.strip()
	if( len(url) == 0 ):
		return ('','')

	dictionaryOfMementos = {}
	count = 0
	#print "...getting memento pages"
	#pages is timemaps
	pages = getMementosPages(url)
	#print "...done getting memento pages"
	if(len(pages) != 0):
		#print 'pages:', len(pages)
		for i in range(0,len(pages)):
			mementos = getItemGivenSignature(pages[i])
			for m in mementos:
				mementoDatetime = m.split(globalMementoUrlDateTimeDelimeter);

				memento = mementoDatetime[0].strip()
				datetimeValue = str(mementoDatetime[1].strip())
				datetimeValue = datetime.strptime(datetimeValue, '%a, %d %b %Y %H:%M:%S %Z')

				dictionaryOfMementos[memento] = datetimeValue

	keys = sorted(dictionaryOfMementos, key=dictionaryOfMementos.get)

	if( len(keys) != 0 ):
		return (keys[0], dictionaryOfMementos[keys[0]])
	else:
		return ('','')


	#print pages

def countMementosForUrl(url):

	url = url.strip()
	if( len(url) == 0 ):
		return 0

	count = 0
	#print "...getting memento pages"
	pages = getMementosPages(url)
	#print "...done getting memento pages"
	if(len(pages) != 0):
		#print 'pages:', len(pages)
		for i in range(0,len(pages)):
			mementos = getItemGivenSignature(pages[i])
			count += len(mementos)

	return count

def countMementos(sNDict):

	if( len(sNDict) == 0 ):
		return

	count = 0
	#key is url
	for key, value in sNDict.items():
		
		countOfMementos = countMementosForUrl(key)
		print count, key, countOfMementos

		outputFile = open('urlsCountOfMementos2.txt', 'a')
		outputFile.write(key + ', ' + str(countOfMementos) + '\n')
		outputFile.close()

		count = count + 1

		#if( count == 5 ):
		#	break

#3.0
def getURLs():

	inputFile = open('urlsCountOfMementos2.txt', 'r')
	lines = inputFile.readlines()
	inputFile.close()

	urlMementoCountDict = {}
	for l in lines:
		urlMementoCount = l.split(', ')
		
		url = urlMementoCount[0].strip()
		mementoCount = urlMementoCount[1].strip()
		urlMementoCountDict[url] = mementoCount

	return urlMementoCountDict


#s0List, s1List = getListPair('formatted_urlsPlaintext_S0.txt', 'formatted_urlsPlaintext_S1.txt')
#s0Dict, s1Dict = getDictPair(s0List, s1List)

#1b
#genericSimilarity(s0Dict, s1Dict)

#2 - start

#countMementos(s1Dict)
#cdf.r, cdf2.r

#2 - end


#3 - start

url1 = 'http://tinyurl.com/'
url1FirstMemento = 'http://web.archive.org/web/20020212130833/http://tinyurl.com/'

#url2 = 'http://www-01.ibm.com/software/analytics/solutions/customer-analytics/social-media-analytics/'
#url2FirstMemento = 'http://web.archive.org/web/20120604080241/http://www-01.ibm.com/software/analytics/solutions/customer-analytics/social-media-analytics/'

outputFile = open('sim1.txt', 'a')


allStringsFirstMemento = extractTextForURI(url1FirstMemento)
tokens = allStringsFirstMemento.split(' ')
tokens = list(set(tokens))
firstMementoVersionOneGrams = find_ngrams(tokens, 1)

pages = getMementosPages(url1)
if(len(pages) != 0):
	
	for i in range(0,len(pages)):
		mementos = getItemGivenSignature(pages[i])

		for url in mementos:
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
				print i, len(pages), oneGramSimilarity
				outputFile.write(str(oneGramSimilarity) + '\n')

			#break
		#break
		

outputFile.close()

# for urls in urlsCountOfMementos2.txt get all plaintext mementos is mementos < 40 else get 100 of such
# for all such plaintext compute jaccard
#3 - end

