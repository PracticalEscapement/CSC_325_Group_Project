from flask import Flask,jsonify
app = Flask(__name__)

@app.route("/")
def index():
    return {"PageName":"index"}

@app.route("/login")
def login():
    return {"PageName":"login"}

@app.route("/signup")
def signup():
    return {"PageName":"signup"}

@app.route("/user/<user_id>")
def user(user_id):
    return {"PageName":f"user {user_id}"}

if __name__ =="__main__":
    app.run(debug=True)

