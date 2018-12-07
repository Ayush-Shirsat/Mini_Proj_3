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
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

def twitter_data(lines, count):
	'''Twitter data'''
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
	'''Labels for media file using Vision API'''
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
	plt.barh(y_pos, val, align='center', alpha=10)
	plt.yticks(y_pos, obj)
	plt.xlabel('Occurance of Label')
	plt.title('Labels in Media')
	plt.show()
	return 0

def analysis(result):
	'''Used to find labels and their occurances'''
	Label_1 = []
	for x in result:
		Label_1.append(x[3])
	occurance = Counter(Label_1)
	Media_1 = []
	num_images = 0
	for y in result:
		Media_1 = y[2]
		if Media_1 == 'None':
			num_images = num_images
		else:
			num_images += 1

	return occurance, num_images

def main():
	# loads a file with Twitter data
	filename = "fetched_tweets.json"
	file = open(filename)
	# Exports Google credentials
	os.system("export GOOGLE_APPLICATION_CREDENTIALS='google_credentials.json'")

	# Used to delete images that may be downloaded multiple times
	test=os.listdir("/home/ece-student/EC_601/Mini_Proj_3/")
	for item in test:
	    if item.endswith(".jpg"):
	        os.remove(item)
	count = 0

	# Connect to MySQL
	mydb = mysql.connector.connect(
	  host = "localhost",
	  user = "ayush",
	  passwd = "",
	)

	mycursor = mydb.cursor()

	# Create Database if it does not exist
	try:
		mycursor.execute("CREATE DATABASE Mini_Proj_3;")
	except:
		print("Database exists")

	# Create Table if it does not exist
	try:
		mycursor.execute("USE Mini_Proj_3")
		mycursor.execute("CREATE TABLE Twitter (Name VARCHAR(100), Handle VARCHAR(100), Media VARCHAR(200), Label VARCHAR(100));")
	except:
		print("Table exists appending values")

	# Insert values to Table
	for lines in file:
		count = int(count) + 1
		sql = "INSERT INTO Twitter (Name, Handle, Media, Label) VALUES (%s, %s, %s, %s)"
		val = twitter_data(lines, count)
		mycursor.execute(sql, val)
		mydb.commit()

	mycursor.execute("SELECT * FROM Twitter")
	result = mycursor.fetchall()

	# Used to print Label and their occurance
	occurance, num_images = analysis(result)
	print("\n")
	obj = []
	val = []
	for key in occurance:
		print(key, " : ", occurance[key])
		obj.append(key)
		val.append(occurance[key])
	y_pos = np.arange(len(obj))

	# Prints Total Handles and Handles with Media files
	print("\nTotal Handles: ", len(result))
	print("Handles with media file: ", num_images)

	print("\nCheck all labels in database")

	# Used to ask query (label in this case)
	q_num = 1
	while(q_num == 1):
		q_num = input("\nTo check label data [press 1]    Quit [press any]: ")
		try:
			q_num = int(q_num)
			q = input("Type a label name to check their handles: ")
			q = str(q)
			q = ("'"+q+"'")
		except:
			q_num = 2
		if (q_num == 1):
			try:
				query = ("SELECT * FROM Twitter WHERE Label = " + q)
				mycursor.execute(query)
				myresult = mycursor.fetchall()
				for queries in myresult:
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
