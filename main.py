import signal
import sys
from flask import Flask
import json
from website import create_app
from website.models import User
from website.routers import community_routes
from flask_cors import CORS


import os


app = create_app()

CORS(app, supports_credentials=True, origins=["http://localhost:3000"])   # Allow cross-origin requests with credentials

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

if __name__ == '__main__':
    #with app.app_context():
       # response = get_user(1).get_json()
    app.run(debug=True)

