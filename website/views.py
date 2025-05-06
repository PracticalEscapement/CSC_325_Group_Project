from flask import Blueprint, render_template,jsonify
from .models import *
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return jsonify({
        "Page":"Home"
    })

@views.route('/community/<community_name>')
def community_name():
   return get_community()