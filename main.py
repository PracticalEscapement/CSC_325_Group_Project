import signal
import sys
from flask import Flask, jsonify
import json
from website import create_app
from website.models import User
from website.models import *
import os


app = create_app()
app.config['SECRET_KEY'] = os.environ.get(SECRET_KEY)
if __name__ == '__main__':
    #with app.app_context():
       # response = get_user(1).get_json()
    app.run(debug=True)

    