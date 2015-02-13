import tweepy

import calendar
import time

import commands
import os, sys
from datetime import datetime
#import threading

#from urlparse import urlparse
import requests

# Consumer keys and access tokens, used for OAuth
consumer_key = 'DzOQzhefR1KUZU6o9K3KpUGe8'
consumer_secret = 'ywrRDh364xyCsihVcGP5KhgJAAC5qYgDWCwTO6y6PlK4nZSZct'
access_token = '2592291038-McunBCHwoIDi7u7ehUSgtSyQmQTfIIBIhVNo14F'
access_token_secret = 'IjkHA5yDn3UdHeGWaRNr3epJYNGTvYOHMCayYv2lLoQ4V'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

def followAndCountTheRedirect(url):

	url = url.strip()
	redirectionCount = 0
	if( len(url) > 0 ):

		indexOfLocation = 0
		httpResponseCodes = ''
		while indexOfLocation > -1:

			co = 'curl -s -I ' + url
			output = commands.getoutput(co)

			indexOfFirstNewLine = output.find('\n')
			if( indexOfFirstNewLine > -1 ):
				httpResponseCodes = output[0:indexOfFirstNewLine].split(' ')[1] + ' ' + httpResponseCodes

			#if( len(httpResponseCodes) > 0 ):
			#	httpResponseCodes = httpResponseCodes[:-1]
			
			indexOfLocation = output.find('location:')
			if( indexOfLocation == -1 ):
				indexOfLocation = output.find('Location:')


			if( indexOfLocation > -1 ):
				indexOfNewLine = output.find('\n', indexOfLocation + 9)
				url = output[indexOfLocation + 9:indexOfNewLine]
				url = url.strip()
				redirectionCount = redirectionCount + 1

	return redirectionCount, url, httpResponseCodes
				
def followTheRedirectCurl(url):
	if(len(url) > 0):

		try:
			r = requests.head(url, allow_redirects=True)
			return r.url
		except:
			return ''
	else:

		return ''
		
def getUrisArray(potentialUrls):

	expandedUrlsList = []
	if(len(potentialUrls) > 0):

		for u in potentialUrls:

			url = (u['expanded_url'])
			#url = urlparse(url)
			#url = url.scheme + '://' + url.netloc
			#url = followTheRedirectCurl(url)

			originalUrl = url
			redirectionCount, url, httpResponseCode = followAndCountTheRedirect(url)
			url = url + ', ' + str(redirectionCount) + ', ' + httpResponseCode

			expandedUrlsList.append(url)

	return expandedUrlsList

def isInsideList(listOfItems, url):
	if(len(listOfItems) > 0 and len(url)> 0):

		for u in listOfItems:
			if(u.lower().strip() == url.lower().strip()):
				return True

	return False

#http://stackoverflow.com/questions/4770297/python-convert-utc-datetime-string-to-local-datetime
def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def fetchResultsFromTwitter(urlsDataFile, searchQuery='www%2E-filter:link', sinceIDValue=0):

	#queries
	#http:// - http%3A%2F%2F
	#http://www. - http%3A%2F%2Fwww%2E-filter:link
	#www. - www%2E

	#http://www. -filter:link; only tweets with links
	if( len(searchQuery) < 1 ):
		return 0

	requestsRemaining = api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']
	#requestsRemaining = 10
	print "Before Request remaining: ", requestsRemaining
	
	#get tweets newer than sinceIDValue
	#print "...if: getting tweets newer than since_id"
	#print "...since_value: ", sinceIDValue

	#for tweet in tweepy.Cursor(api.search, q=searchQuery).items():
	#for tweet in tweepy.Cursor(api.search, q=searchQuery, since="2014-01-01",until="2014-09-19").items(15):
	#for tweet in tweepy.Cursor(api.search, q=searchQuery, since_id=long(sinceIDValue)).items(15):
	for tweet in tweepy.Cursor(api.search, q=searchQuery).items(30):

		localTimeTweet = datetime_from_utc_to_local(tweet.created_at)
		#print tweet.id, tweet.created_at
		if( tweet.id > sinceIDValue ):
			sinceIDValue = tweet.id

		expandedUrlsList = getUrisArray(tweet.entities['urls'])

		if(len(expandedUrlsList) > 0):

			for u in expandedUrlsList:
				if(len(u) > 0):
					u = u.lower().strip()

					print "...adding: ", tweet.id, u, localTimeTweet
					urlsDataFile.write(str(tweet.id) + ', ' + u + ', ' + str(localTimeTweet) + '\n' )


	return sinceIDValue

def entryPointToFetchTweets(outputFileName):

	outputFileName = outputFileName.strip()
	if( len(outputFileName) < 1 ):
		return

	lengthOfLinksFile = 0
	sinceIDValue = 0
	while(lengthOfLinksFile < 15000):
		try:
			urlsDataFile = open(outputFileName, 'a+')
			lengthOfLinksFile = len(urlsDataFile.readlines())
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )
			urlsDataFile.close()

		sinceIDValue = fetchResultsFromTwitter(urlsDataFile, searchQuery='www%2E-filter:link', sinceIDValue=sinceIDValue)
		print "...lengthOfLinksFile/sinceIDValue: ", lengthOfLinksFile, sinceIDValue
		print
		urlsDataFile.close()
		time.sleep(15)
'''
Total Tweet IDs: 10000
Unique Tweet IDs: 9442

Total URIs: 10000
Unique URIs: 2165
'''
def countDuplicatesAndMakeUniqueLinksFile(inputFileName):

	inputFileName = inputFileName.strip()
	if( len(inputFileName) > 0 ):

		lines = []
		try:
			inputFile = open(inputFileName.strip(), 'r')
			lines = inputFile.readlines()
			inputFile.close()
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )

		uniqueListOfURIs = []
		dataToWriteToFile = []
		#URI: <TWEET ID, URI, REDIRECTION COUNT, [REDIRECTION CODES], TWEET CREATED AT>
		for URI in lines:
			tuples = URI.strip().split(', ')

			if( tuples[1] not in uniqueListOfURIs ):
				uniqueListOfURIs.append(tuples[1])
				dataToWriteToFile.append(URI.decode('ascii', 'ignore'))

		try:
			outputFile = open('unique_'+inputFileName, 'w')
			outputFile.writelines(dataToWriteToFile)
			outputFile.close()
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )

def removeDuplicates(originalFile, inputFileName):

	inputFileName = inputFileName.strip()
	originalFile = originalFile.strip()
	if( len(inputFileName) > 0 and len(originalFile) > 0 ):

		lines = []
		oriLines2 = []
		try:
			inputFile = open(inputFileName, 'r')
			originalInputFile = open(originalFile, 'r')

			lines = inputFile.readlines()
			oriLines2 = originalInputFile.readlines()

			originalInputFile.close()
			inputFile.close()
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )

		listForChecking = []
		listForWriting = []
		for l in lines:

			URI = l.strip().split(', ')[1].strip()
			if( URI not in listForChecking ):
				listForChecking.append(URI)
				listForWriting.append(l)

		
		listOfRemainingItemsToCD = []
		print '...nonDuplicateLines', len(listForChecking)

		
		for l in oriLines2:
			URI = l.strip().split(', ')[1].strip()
			
			if( URI not in listForChecking ):
				listOfRemainingItemsToCD.append(l)
		


		print '...remainder to carbon date', len(listOfRemainingItemsToCD)

		'''
		outputFile = open('remainderToCD2.txt', 'w')
		outputFile.writelines(listOfRemainingItemsToCD)
		outputFile.close()
		'''

		outputFile = open('final_'+inputFileName, 'w')
		outputFile.writelines(listForWriting)
		outputFile.close()

def generateStatusCodesData0(fileName):

	fileName = fileName.strip()
	if( len(fileName) > 0 ):

		lines = []
		try:
			inputFile = open(fileName, 'r')
			lines = inputFile.readlines()
			inputFile.close()
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )


		for entry in lines:
			#entry: <TWEET ID, URI, REDIRECTION COUNT, [REDIRECTION CODES], TWEET CREATED AT>
			tuples = entry.strip().split(', ')
			del tuples[0]
			del tuples[0]
			del tuples[0]

			if( len(tuples) == 2 ):
				statusCodes = tuples[0].strip().split(', ')

def generateStatusCodesData1(fileName):
	fileName = fileName.strip()
	if( len(fileName) > 0 ):

		lines = []
		try:
			inputFile = open(fileName, 'r')
			outputFile = open('STATUS_CODE_FREQUENCY.txt', 'w')

			lines = inputFile.readlines()
			inputFile.close()
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )

		dictionaryOfStatusCodesFrequency = {}
		for entry in lines:
			statusCodes = entry.strip().split(' ')
			for code in statusCodes:

				if( code in dictionaryOfStatusCodesFrequency ):
					dictionaryOfStatusCodesFrequency[code] += 1
				else:
					dictionaryOfStatusCodesFrequency[code] = 1

		for statusCode, statusCodeFrequency in dictionaryOfStatusCodesFrequency.items():
			outputFile.write(str(statusCode) + ' ' + str(statusCodeFrequency) + '\n')

		outputFile.close()

def generateRedirectionCountData0(fileName):
	fileName = fileName.strip()
	if( len(fileName) > 0 ):

		lines = []
		try:
			inputFile = open(fileName, 'r')
			lines = inputFile.readlines()
			inputFile.close()
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )


		for entry in lines:
			#entry: <TWEET ID, URI, REDIRECTION COUNT, [REDIRECTION CODES], TWEET CREATED AT>
			tuples = entry.strip().split(', ')
			print tuples[2]

def generateRedirectionCountData1(fileName):
	fileName = fileName.strip()
	if( len(fileName) > 0 ):

		lines = []
		try:
			inputFile = open(fileName, 'r')
			outputFile = open('REDIRECTION_COUNT_FREQUENCY.txt', 'w')

			lines = inputFile.readlines()
			inputFile.close()
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )


		dictionarOfRedirectionCountFrequency = {}
		for entry in lines:

			entry = entry.strip()
			dictionarOfRedirectionCountFrequency.setdefault(entry, 0)
			dictionarOfRedirectionCountFrequency[entry] += 1

		print dictionarOfRedirectionCountFrequency
		for redirectionCount, redirectionCountFrequency in dictionarOfRedirectionCountFrequency.items():
			outputFile.write(redirectionCount + ' ' + str(redirectionCountFrequency) + '\n' )



		outputFile.close()

def generateAgeData(fileName):

	fileName = fileName.strip()
	if( len(fileName) > 0 ):

		lines = []
		try:
			inputFile = open(fileName, 'r')
			lines = inputFile.readlines()
			inputFile.close()
		except:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(fname, exc_tb.tb_lineno, sys.exc_info() )


		for entry in lines:
			#entry: <TWEET ID, URI, REDIRECTION COUNT, [REDIRECTION CODES], TWEET CREATED AT, (OPTIONAL EST. CREATION DATE)>
			tuples = entry.strip().split(', ')
			
			try:
				dateTimeCD = datetime.strptime(tuples[-1], '%Y-%m-%dT%H:%M:%S')
				dateTimeTweet = datetime.strptime(tuples[-2], '%Y-%m-%d %H:%M:%S')

				
			
				daysDelta = (dateTimeTweet - dateTimeCD).days
				if( daysDelta < 0 ):
					daysDelta = daysDelta * (-1)
				print daysDelta
			except:
				pass


			

generateAgeData('final_cd_unique_originalLinksFile.txt')
#generateRedirectionCount1('raw_redirectionCount.txt')		
#generateStatusCodesData1('statusCodes.txt')
#generateStatusCodesData0('unique_originalLinksFile.txt')
#countDuplicatesAndMakeUniqueLinksFile('originalLinksFile.txt')
#removeDuplicates('unique_originalLinksFile.txt', 'cd_unique_originalLinksFile.txt')

#cd remainder into cd_unique_originalLinksFile.txt
#check duplicate for cd_unique_originalLinksFile.txt