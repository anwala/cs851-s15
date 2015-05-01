def getFirstMemento(url):

	url = url.strip()
	if( len(url) == 0 ):
		return ('','')

	dictionaryOfMementos = {}
	count = 0
	#print "...getting memento pages"
	#pages is timemaps
	pages = getMementosPages(url)
	#print "...done getting memento pages"
	if(len(pages) != 0):
		#print 'pages:', len(pages)
		for i in range(0,len(pages)):
			mementos = getItemGivenSignature(pages[i])
			for m in mementos:
				mementoDatetime = m.split(globalMementoUrlDateTimeDelimeter);

				memento = mementoDatetime[0].strip()
				datetimeValue = str(mementoDatetime[1].strip())
				datetimeValue = datetime.strptime(datetimeValue, '%a, %d %b %Y %H:%M:%S %Z')

				dictionaryOfMementos[memento] = datetimeValue

	keys = sorted(dictionaryOfMementos, key=dictionaryOfMementos.get)

	if( len(keys) != 0 ):
		return (keys[0], dictionaryOfMementos[keys[0]])
	else:
		return ('','')
