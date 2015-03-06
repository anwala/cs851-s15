import commands
import os, sys
import urlparse

def downloadWarc(inputFile):

	inputFile = inputFile.strip()

	if(len(inputFile) == 0):
		return

	lines = []
	try:
		inputFile = open(inputFile)
		lines = inputFile.readlines()
		print '...readlines:', len(lines)
		inputFile.close()
	except:
		print 'FILE ERROR'


	longURL = ''
	for url in lines:
		longURL = longURL + ' ' + url.strip()

	#print longURL

	
	try:
		co = 'wget --warc-file=grandWarc2 -p -l 1' + longURL 
		commands.getoutput(co)
	except:
		print 'WGET ERROR'
		pass

	'''
	for i in range(0, len(lines)):
		line = lines[i].strip()
		try:
			print '...warcing:', line
			co = 'wget --warc-file=./wgetWarcFiles/' + str(i) + ' -p -l 1 ' + line
			commands.getoutput(co)
		except:
			print 'WGET ERROR'
			pass
		
		#if(i == 5):
		#	break
	'''

inputFile = '100URIsWget.txt'
downloadWarc(inputFile)
