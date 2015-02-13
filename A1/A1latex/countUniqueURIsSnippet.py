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