from flask import Blueprint, jsonify, request, make_response
from website.models import *
from website.auth import token_required  # Import token_required from the appropriate module

Users_routes = Blueprint('Users_routes', __name__)



@Users_routes.route('/api/User/<int:User_id>', methods=['GET'])
def fetch_User(User_id):
    """
    API route to fetch community Posts.
    """
    
    return get_user(User_id)

@Users_routes.route('/api/User', methods=['GET'])
def fetch_all_Users():
    """
    API route to fetch community Posts.
    """
    
    return get_all_users()

@Users_routes.route('/api/User/<int:User_id>', methods=['OPTIONS'])
def fetch_Users_preflight(User_id):
     # Handle preflight request
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
    return response, 200

