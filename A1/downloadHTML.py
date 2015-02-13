import commands
import os, sys
import hashlib
#from bs4 import BeautifulSoup
from os import walk
import math

import re
#inputFileName: <, uri, ...>
inputFileName = 'unique_originalLinksFile.txt'
#<uri, md5hash>
uriHashDictionary = {}


def getInput():

	try:
		urlsFile = open(inputFileName)
		listOfURIs = urlsFile.readlines()
		print 'readlines', len(listOfURIs)

		if(len(listOfURIs) > 0):
			for u in listOfURIs:

				u = u.split(', ')
				u = u[1]
				#u = u.encode('ascii', 'ignore')
				md5hashFilename = getHashFromURI(u)
				uriHashDictionary[u] = md5hashFilename

	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(fname, exc_tb.tb_lineno, sys.exc_info() )
		return


	return listOfURIs

def getHashFromURI(uri):

	md5hash = ''

	if( len(uri) > 0 ):
		# Assumes the default UTF-8; http://www.pythoncentral.io/hashing-strings-with-python/
		hash_object = hashlib.md5(uri.encode())
		md5hash = hash_object.hexdigest()

	return md5hash

def extractHTMLAndSave():

	if( len(uriHashDictionary) > 0 ):
		count = 1
		for uri in uriHashDictionary:

			
			'''
			#wget -p -k http://www.cs.odu.edu
			The -p will get you all the required elements to view the site correctly (css, images, etc). The -k will change all links (to include those for CSS & images) to allow you to view the page offline as it appeared online.
			'''
			filename =  str(count) + '-' + uriHashDictionary[uri] + '.html'
			co = 'curl -s -L ' + uri + ' > ./RawHtml/' + filename
			
			commands.getoutput(co)
			print '...saved', filename, count
			count = count + 1
			


getInput()
extractHTMLAndSave()
