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