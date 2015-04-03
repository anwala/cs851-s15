#Remove boilerplate snippet
def extractText(listOfURIs):
	...
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
...

