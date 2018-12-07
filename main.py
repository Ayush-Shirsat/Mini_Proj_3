# Step-1: Download Tweets using Tweepy

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import sys
import twitter_credentials

class StdOutListener(StreamListener):

	def __init__(self):
		# Initializing Tweet count to 0
		self.counter = 0
		
	def on_data(self, data):
		# Incrementing Tweet count
		self.counter += 1
		
		if self.counter > num:
			# Exit code once Tweet limit is reached
			sys.exit() 
		else:
			# Prints Tweets(in json) as they stream
			# print(data)
			
			# Save all Tweets to a file
			with open('fetched_tweets.json','a+') as tf:
				tf.write(data)

		return True

	def on_error(self, status):
		# Prints error (if any) 
		print(status)

if __name__== "__main__":

	listener = StdOutListener()
	auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
	auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
	
	# Takes user input for maximum Tweets to Analyze
	num = int(input("Enter maximum number of tweets to analyze: ")) 
	
	# Takes user input to search for a keyword while streaming Tweets
	word = input("Enter a keyword to search: ")
	
	stream = Stream(auth, listener)
	
	# Filters search track based on user keyword
	stream.filter(track=[word])

end

