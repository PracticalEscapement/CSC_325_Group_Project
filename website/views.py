from flask import Blueprint, render_template,jsonify

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return jsonify({"Page":"Home"})