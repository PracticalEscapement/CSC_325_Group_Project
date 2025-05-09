from flask import Blueprint, jsonify, request, make_response
from website.models import *
from website.auth import token_required  # Import token_required from the appropriate module

Posts_routes = Blueprint('Posts_routes', __name__)

# Adding a Post
@Posts_routes.route('/api/Posts', methods=['POST'])
@token_required
def add_Post(decoded_token):
    """
    API route to add a new community.
    """
    data = request.get_json()  # Get JSON data from the request
    if not data:
        return jsonify({"error": "No data provided"}), 400

    
    com_name = data.get('com_name')
    title= data.get('title')
    content =data.get('content')
    comments = data.get('comments')

    # Validate required fields
    if not com_name:
        return jsonify({"error": "community name Required"}), 400


    # Get the user ID from the decoded token
    user_id = decoded_token.get('user_id')

   
    new_Post = Post(
        author_id=user_id, # Set the current user as the author
        com_name=com_name,
        title=title,
        content=content,
        comments=comments,
    )

    # Add to the database
    db.session.add(new_Post)
    db.session.commit()

    return jsonify({"message": "Post created successfully", "Post": {
        "Post_id":new_Post.id,
        "author_id":new_Post.author_id,
        "com_name":new_Post.com_name,
        "title":new_Post.title,
        "content":new_Post.content,
        "comments":new_Post.comments,
    }}), 201


@Posts_routes.route('/api/Posts/<string:com_name>', methods=['GET'])
def fetch_community_Posts(com_name):
    """
    API route to fetch community Posts.
    """
    
    return get_community_posts(com_name)

@Posts_routes.route('/api/Posts/<int:Post_id>', methods=['GET'])
def fetch_Posts(Post_id):
    """
    API route to fetch Posts.
    """
    return get_posts(Post_id)

@Posts_routes.route('/api/Posts/<int:com_name>', methods=['OPTIONS'])
def fetch_Posts_preflight(user_id):
     # Handle preflight request
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
    return response, 200

