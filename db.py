import pymongo
from flask import request
import datetime
from bson.objectid import ObjectId

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
userdb = client['userdb']
users = userdb.participants

def insert_data():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['pass']

		participant = {}
		participant['name'] = name
		participant['email'] = email
		participant['password'] = password

		if users.find_one({"email":email}) == None:
			users.insert_one(participant)
			return True
		else:
			return False


def check_user():

	if request.method == 'POST':
		email = request.form['email']
		password = request.form['pass']

		user = {
			"email": email,
			"password": password
		}

		user_data = users.find_one(user)
		if user_data == None:
			return False, ""
		else:
			current_time = datetime.datetime.now()
			users.update_one({"_id": user_data["_id"]}, {"$set": {"logged_in": True, "login_time": current_time}})
			return True, user_data["name"]
		
def fetch_data():
	user_data = users.find()
	if user_data == None:
		return False, ""
	else:
		data =[]
		for user in user_data:
			print("user ",user)
			data.append({"_id": user["_id"] , "name": user["name"],"email": user["email"]})
		return True, data
	
		
def delete_data(participant_id):
	users.delete_one({"_id": ObjectId(participant_id)})
	user_data = users.find()
	if user_data == None:
		return False, ""
	else:
		data =[]
		for user in user_data:
			print("user ",user)
			data.append({"_id": user["_id"] , "name": user["name"],"email": user["email"]})
		return True, data