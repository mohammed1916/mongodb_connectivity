import db
import json
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template("signin.html")


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")


@app.route('/participants', methods = ['GET', 'POST'])
def participants():
    status, data= db.fetch_data()
    return render_template("participants.html", data = data, status = status)

@app.route('/update/<participant_id>')
def update(participant_id):
    status, data= db.fetch_data(participant_id)
    return render_template("update.html", data = data, status = status)
@app.route('/update/<participant_id>')
def updateData(participant_id,  methods = ['GET', 'POST']):
    status, data= db.update_data(participant_id)
    return render_template("update.html", data = data, status = status)

@app.route("/delete/<participant_id>", methods = ['GET', 'POST'])
def delete(participant_id):
    status, data= db.delete_data(participant_id)
    return render_template("participants.html", data = data, status = status)


@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    status, username = db.check_user()

    data = {
        "username": username,
        "status": status
    }

    return json.dumps(data)



@app.route('/register', methods = ['GET', 'POST'])
def register():
    status = db.insert_data()
    return json.dumps(status)


if __name__ == '__main__':
    app.run(debug = True)