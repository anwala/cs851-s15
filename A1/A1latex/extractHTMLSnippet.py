def extractHTMLAndSave():

	if( len(uriHashDictionary) > 0 ):
		count = 1
		for uri in uriHashDictionary:

			filename =  str(count) + '-' + uriHashDictionary[uri] + '.html'
			co = 'curl -s -L ' + uri + ' > ./RawHtml/' + filename
			
			commands.getoutput(co)
			print '...saved', filename, count
			count = count + 1