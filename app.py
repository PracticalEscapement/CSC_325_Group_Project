import signal
import sys
from flask import Flask
import json
from website import create_app
from website.models import User
from website.Routes.Communities import community_routes
from dotenv import load_dotenv
from flask_cors import CORS


import os


app = create_app()

CORS(app, supports_credentials=True, origins=["http://localhost:3000", "https://reddit-clone-frontend-p4hwidw9d-practicalescapements-projects.vercel.app/"])   # Allow cross-origin requests with credentials

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

if __name__ == '__main__':
    app.run(debug=True)

