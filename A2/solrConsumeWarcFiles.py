import commands
import os
'''
https://github.com/ukwa/webarchive-discovery/wiki/Quick-Start
http://www.webupd8.org/2012/01/install-oracle-java-jdk-7-in-ubuntu-via.html
https://www.digitalocean.com/community/tutorials/how-to-install-java-on-ubuntu-with-apt-get
http://stackoverflow.com/questions/15630055/how-to-install-maven-3-on-ubuntu-14-10-14-04-lts-13-10-13-04-12-10-12-04-by-usin
'''
def consumeWarcFiles(folderName):

	folderName = folderName.strip()
	if( len(folderName) == 0 ):
		return

	for fileName in os.listdir(folderName):
		if(fileName.find('.gz') > -1):
			print fileName

	#tar warc file

	#index warc file
	#co = 'java -jar ./webarchive-discovery/warc-indexer-2.0.1-20150116.110435-2-jar-with-dependencies.jar -s http://localhost:8080/discovery ./arsenal.warc.gz'

	'''
	try:
		commands.getoutput(co)
	except:
		print 'ERROR'
		pass
	'''



folderName = './solrWarcs'
consumeWarcFiles(folderName)

#'java -jar ./webarchive-discovery/warc-indexer-2.0.1-20150116.110435-2-jar-with-dependencies.jar -s http://localhost:8080/discovery warc-indexer/src/test/resources/wikipedia-mona-lisa/flashfrozen-jwat-recompressed.warc.gz'