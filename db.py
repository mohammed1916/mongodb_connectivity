import pymongo
from flask import request
import datetime
from bson.objectid import ObjectId

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
userdb = client['userdb']
users = userdb.participants

# Static admin ID and password
ADMIN_ID = "admin"
ADMIN_PASSWORD = "password"

# Insert admin data into the database
admin = {
	"name": "admin",
	"email": "admin@example.com",
	"password": 123
}



if users.find_one({"email": admin["email"]}) is None:
	users.insert_one(admin)

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
	
def fetch_data(participant_id):
	print("request: ", request.method)
	participant_data = users.find_one({"_id": ObjectId(participant_id)})
	if participant_data:
		return True, participant_data
	else:
		return False, ""

def update_data(participant_id):
	print("request: ", request.method)
	participant_data = users.find_one({"_id": ObjectId(participant_id)})
	print("participant_data: ", participant_data)
	if participant_data is not None:
		participant = {}
		if request.method == 'GET':
			participant = {
				"name": request.form['name'],
				"email": request.form['email'],
				"password": request.form['pass'],
				"papername": request.form['papername'],
				"domain": request.form['domain'],
				"date": request.form['date']
			}
			participant_update = {
				"$set": participant
			}
			users.update_one({"_id": ObjectId(participant_id)}, participant_update)
			return_participant = users.find_one({"_id": ObjectId(participant_id)})
			return True, return_participant
	else:
		return False, ""
		
def delete_data(participant_id):
	users.delete_one({"_id": ObjectId(participant_id)})
	return True