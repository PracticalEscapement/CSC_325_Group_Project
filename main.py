import signal
import sys
from flask import Flask, jsonify
import json
from website import create_app
import os


app = create_app()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
if __name__ == '__main__':
    app.run(debug=True)

    