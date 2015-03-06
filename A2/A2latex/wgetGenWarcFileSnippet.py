
#generate warc files for multiple URIs
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

	try:
		co = 'wget --warc-file=grandWarc2 -p -l 1' + longURL 
		commands.getoutput(co)
	except:
		print 'WGET ERROR'
		

