import justext
import urllib2
import sys, os


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

def extractText(listOfURIs):

	if( len(listOfURIs) == 0 ):
		return

	try:
		outputFile = open('urlsPlaintext.txt', 'a')
		statOutputFile = open('urlsStat.txt', 'a')
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(fname, exc_tb.tb_lineno, sys.exc_info() )
		return

	alreadyAddedList = []
	for i in range(0, len(listOfURIs) ):

		try:
			URI = listOfURIs[i].split(', ')[1].strip()
			print i, URI

			page = urllib2.urlopen(URI).read()
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
					
			
lines = getInput('unique_originalLinksFile.txt')
extractText(lines)

