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