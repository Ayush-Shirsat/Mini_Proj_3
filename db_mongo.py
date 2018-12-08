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

def graph(obj, val, y_pos):
	'''Plots graph for all labels'''
	plt.barh(y_pos, val, align='center')
	plt.yticks(y_pos, obj)
	plt.xlabel('Occurance of Label')
	plt.title('Labels in Media')
	plt.show()
	return 0

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

def main():
	# loads a file with Twitter data
	filename = "fetched_tweets.json"
	file = open(filename)
	# Exports Google credentials
	os.system("export GOOGLE_APPLICATION_CREDENTIALS='google_credentials.json'")

	# Used to delete images that may be downloaded multiple times
	test=os.listdir("/home/ayush34/Desktop/Mini_Proj_3/Mini_Proj_3/")
	for item in test:
	    if item.endswith(".jpg"):
	        os.remove(item)

	count = 0

	# Connect to MongoDB
	myclient = pymongo.MongoClient()
	try:
		myclient.drop_database("Mini_Proj_3")
	except:
		pass
	mydb = myclient["Mini_Proj_3"]
	mycol = mydb["Twitter"]

	line_count = 1

	for lines in file:
		count = int(count) + 1
		name, handle, media, label = twitter_data(lines, count)

		mydict = {"Name" : name, "Handle" : handle, "Media" : media, "Label" : label}

		result = mycol.insert_one(mydict)
		line_count += 1

	# Used to print Label and their occurance
	num_images = []
	Label_1 = []
	for result in mycol.find():
		occurance, num = analysis(result, Label_1, num_images)
	print("\n")
	obj = []
	val = []
	for key in occurance:
		print(key, " : ", occurance[key])
		obj.append(key)
		val.append(occurance[key])
	y_pos = np.arange(len(obj))

	# Prints Total Handles and Handles with Media files
	print("\nTotal Handles: ", line_count) 
	print("Handles with media file: ", len(num))

	print("\nCheck all labels in database")

	# Used to ask query (label in this case)
	q_num = 1
	while(q_num == 1):
		q_num = input("\nTo check label data [press 1]    Quit [press any]: ")
		try:
			q_num = int(q_num)
			q = input("Type a label name to check their handles: ")
			q = str(q)
			Q = {"Label" : q}
		except:
			q_num = 2
		if (q_num == 1):
			try:
				mydoc = mycol.find(Q)
				for queries in mydoc:
					print(queries)
			except:
				print("Label does not exist")
		else:
			pass

	# Displays a graph with all labels and their occurances
	g = input("\nTo check graph [press 1]    Quit [press any]: ")
	try:
		g = int(g)
	except:
		g = 2
	if g == 1:
		graph(obj, val, y_pos)
	else:
		print("Graph not displayed")
	return 0

# Main is executed first
if __name__ == "__main__":
	main()
