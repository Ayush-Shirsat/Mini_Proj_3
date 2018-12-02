import json
import pymongo
from pymongo import MongoClient, ReturnDocument

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

#################################################################

def main():
	filename = "fetched_tweets.json"
	file = open(filename)

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	myclient.drop_database("Mini_Proj_3")
	mydb = myclient["Mini_Proj_3"]
	mycol = mydb["Twitter"]

	for lines in file:
		name, handle, media = twitter_data(lines)

		mydict = {"Name" : name, "Handle" : handle, "Media" : media}
		x = mycol.insert_one(mydict)
	# print(x.inserted_ids)

	for x in mycol.find():
		print(x)

###################################################################

if __name__ == "__main__":
	main()
