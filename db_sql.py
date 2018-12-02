import json
import mysql
import mysql.connector

def twitter_data(lines):
	line_new = lines.split('"')
	substring_1 = "media_url"
	if substring_1 in lines:
		# Print Yes if tweet contains Media URL
		# print("Yes")		
		num_1 = line_new.index('media_url')
		media_url = line_new[num_1+2]
		media_url = media_url.replace("\\", "")
	else:
		media_url = 'None'
	substring_2 = "user"
	if substring_2 in lines:
		num_2 = line_new.index('user')
		user_name = line_new[num_2+10]
	else:
		user_name = 'None'
		# Name = media_url.replace("\\", "")
	substring_3 = "user"
	if substring_2 in lines:
		num_2 = line_new.index('user')
		handle = line_new[num_2+14]
		handle = '@'+handle
	else:
		handle = 'None'
	return (user_name, handle, media_url)


#################################################################

def main():
	filename = "fetched_tweets.json"
	file = open(filename)

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
		mycursor.execute("CREATE TABLE Twitter (Name VARCHAR(100), Handle VARCHAR(100), Media VARCHAR(200));")
	except:
		print("Table exists")

	for lines in file:
		sql = "INSERT INTO Twitter (Name, Handle, Media) VALUES (%s, %s, %s)"
		val = twitter_data(lines)
		mycursor.execute(sql, val)
		mydb.commit()

	return 0

###################################################################

if __name__ == "__main__":
	main()
