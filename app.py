import db
import json
from flask import Flask, render_template, redirect, request, url_for

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

@app.route('/update/<participant_id>', methods = ['GET', 'POST'])
def update(participant_id):
    if request.method == "POST":
        updated_participant = {
            "$set": {
                "name": request.form["name"],
                "email": request.form["email"],
                "pass": request.form["pass"],
                "papername": request.form["papername"],
                "domain": request.form["domain"],
                "date": request.form["date"]
            }
        }
        db.users.update_one({"_id": db.ObjectId(participant_id)}, updated_participant)
        return redirect(url_for("participants"))

    participant = db.users.find_one({"_id": db.ObjectId(participant_id)})
    return render_template("update.html", data = participant)

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