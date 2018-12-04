import json
import pymongo
from pymongo import MongoClient, ReturnDocument
import json
import wget
import argparse
import sys
from google.cloud import vision
from google.cloud.vision import types, ImageAnnotatorClient
import io
import os
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

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

def main():
	filename = "fetched_tweets.json"
	file = open(filename)
	os.system("export GOOGLE_APPLICATION_CREDENTIALS='google_credentials.json'")

	test=os.listdir("/home/ece-student/EC_601/Mini_Proj_3/")
	for item in test:
	    if item.endswith(".jpg"):
	        os.remove(item)
	count = 0

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	myclient.drop_database("Mini_Proj_3")
	mydb = myclient["Mini_Proj_3"]
	mycol = mydb["Twitter"]

	for lines in file:
		count = int(count) + 1
		name, handle, media, label = twitter_data(lines, count)

		mydict = {"Name" : name, "Handle" : handle, "Media" : media, "Label" : label}
		result = mycol.insert_one(mydict)

	# print("\nTotal Handles: ", len(result))
	# print("Handles with media file: ", num_images)
	num_images = []
	Label_1 = []
	for result in mycol.find():
		# print(result)
		occurance, num = analysis(result, Label_1, num_images)
	print("\n")
	for key in occurance:
		print(key, " : ", occurance[key])

	print("\nTotal Handles: 100") 
	print("Handles with media file: ", len(num))


def analysis(result, Label_1, num_images):
	Label_1.append(result.get("Label"))
	occurance = Counter(Label_1)
	Media_1 = []
	Media_1 = result.get("Media")
	if Media_1 == 'None':
		pass
	else:
		num_images.append('1')

	return occurance, num_images

if __name__ == "__main__":
	main()

