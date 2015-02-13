#for tweet in tweepy.Cursor(api.search, q=searchQuery).items():
#for tweet in tweepy.Cursor(api.search, q=searchQuery, since="2014-01-01",until="2014-09-19").items(15):
#for tweet in tweepy.Cursor(api.search, q=searchQuery, since_id=long(sinceIDValue)).items(15):
for tweet in tweepy.Cursor(api.search, q=searchQuery).items(30):

	localTimeTweet = datetime_from_utc_to_local(tweet.created_at)
	#print tweet.id, tweet.created_at
	if( tweet.id > sinceIDValue ):
		sinceIDValue = tweet.id

	expandedUrlsList = getUrisArray(tweet.entities['urls'])

	if(len(expandedUrlsList) > 0):

		for u in expandedUrlsList:
			if(len(u) > 0):
				u = u.lower().strip()

				print "...adding: ", tweet.id, u, localTimeTweet
				urlsDataFile.write(str(tweet.id) + ', ' + u + ', ' + str(localTimeTweet) + '\n' )