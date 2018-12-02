import json
import mysql
import mysql.connector
import wget
import argparse
import sys
from google.cloud import vision
from google.cloud.vision import types, ImageAnnotatorClient
import io
import os
import collections

#################################################################

def twitter_data(lines, count):
	line_new = lines.split('"')
	substring_1 = "media_url"
	if substring_1 in lines:		
		num_1 = line_new.index('media_url')
		media_url = line_new[num_1+2]
		media_url = media_url.replace("\\", "")
		img_name = "img" + str(count).zfill(4) + ".jpg"	
		wget.download(media_url, out=img_name)
		label = vision(img_name)
	else:
		media_url = 'None'
		label = 'None'
	substring_2 = "user"
	if substring_2 in lines:
		num_2 = line_new.index('user')
		user_name = line_new[num_2+10]
	else:
		user_name = 'None'
	substring_3 = "user"
	if substring_2 in lines:
		num_2 = line_new.index('user')
		handle = line_new[num_2+14]
		handle = '@'+handle
	else:
		handle = 'None'
	return (user_name, handle, media_url, label)

#################################################################

def vision(img_name):
	vision_client = ImageAnnotatorClient()
	file_name = str(img_name)

	with io.open(file_name,'rb') as image_file:
		content = image_file.read()
		image = types.Image(content=content)

	response = vision_client.label_detection(image=image)
	labels = response.label_annotations
	label = labels[0]

	return label.description
	# for label in labels:
	# 	print(label.description, label.score)

#################################################################
def main():
	filename = "fetched_tweets.json"
	file = open(filename)
	os.system("export GOOGLE_APPLICATION_CREDENTIALS='google_credentials.json'")
	count = 0

	mydb = mysql.connector.connect(
	  host = "localhost",
	  user = "ayush",
	  passwd = ""
	)

	mycursor = mydb.cursor()
	try:
		mycursor.execute("CREATE DATABASE Mini_Proj_3;")
	except:
		print("Database exists")

	try:
		mycursor.execute("USE Mini_Proj_3")
		mycursor.execute("CREATE TABLE Twitter (Name VARCHAR(100), Handle VARCHAR(100), Media VARCHAR(200), Label VARCHAR(100));")
	except:
		print("Table exists")

	for lines in file:
		count = int(count) + 1
		sql = "INSERT INTO Twitter (Name, Handle, Media, Label) VALUES (%s, %s, %s, %s)"
		val = twitter_data(lines, count)
		mycursor.execute(sql, val)
		mydb.commit()

	mycursor.execute("SELECT * FROM Twitter;")
	result = mycursor.fetchall()
	print(result)
	idk = analysis()
	something = query()

	return 0

def analysis():
	# mycursor.execute("SELECT Label,COUNT(*) as occurance FROM Twitter GROUP BY Label;")
	pass

def query():
	pass




###################################################################

if __name__ == "__main__":
	main()
