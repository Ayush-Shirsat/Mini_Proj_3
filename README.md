# Mini_Proj_3: Databases
Analysis of Tweets using Tweepy and Google Vision API. Stores data in 2 databases: MySQL and MongoDB

# Built using
*Python 3.6.6*

*Tweepy 3.6.0*

*google-cloud-vision 0.35.1*

*Ubuntu 18.04.1 LTS*

*MySQL 5.7.24*

*pymongo 3.7.2*

*numpy 1.13.3*

*matplotlib 2.2.2*

# How the program works

### Step-1:
Run the program: ```main_code.py```

Make sure that a file containing twitter credentials is imported as shown in line: 8. File "twitter_credentials.py" has the necessary credentials required to run. This program uses streaming class of tweepy.

User input is taken to stream the maximum number of tweets as shown in line: 44. Setting a limit is generally good as it gives data as per user specifications. The user also inputs a keyword, based on which the Tweets are streamed as shown in line: 47.

All tweets are in json format and get saved in a file named "fetched_tweets.json".

A file named ```fetched_tweets.json``` is already in this repository with necessary data. So no need to run this program again.

### Step-2:

Make sure file path on ```line: 92``` for MySQL and on ```line: 86``` for MongoDB are correct.

Before running ```db_mongo.py``` please type the following on command line:

```sudo service mongod start```

Both MySQL and MongoDB are built in same manner and will give same outputs for a query. They are running on localhost.

Run the following commads on terminal:

```python db_sql.py```

```python db_mongo.py```

Just follow the instructions on terminal to continue.

# Results

```main_code.py``` will stream tweets and save them to file fetched_tweets.json.

Both the database programs will download media files (if any) using ```wget```.

Google Vision API will label the data. Name and handle denote username and twitter handle of user respectively. Media contains an image which is downloaded. Label tells us the content of the image. If there are no Media files then, Media and Label are tagged as 'None'.

Database has following architecture:

```Name | Handle | Media | Label```

After running the programs, Labels and their number of occurances are printed. An user can look at the labels and ask query (label) which is prompted on the screen. This will output the details of all the users with that particular label. Finally a bar graph is plotted which demonstrates the label and its occurances. 

**Result images are available in img folder.**



# Bugs/ Errors
Sometimes files "db_sql.py" and "db_mongo.py" throw an error about google application credentials. To fix that run the following command on terminal:

```
export GOOGLE_APPLICATION_CREDENTIALS='google_credentials.json'
```
Make sure file 'google_credentials.json' has correct path.

# Conclusion

Tweepy was used to stream tweets and store them. Google Vision API labelled the media files contained in the tweets. Two databases were implemented -MySQL and MongoDB. User can ask a query based on labels and user details are outputted correctly. Bar graph is plotted to map the labels with its occurance for statistical analysis. 
