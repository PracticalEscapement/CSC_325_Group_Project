from flask import Blueprint, jsonify, request, make_response
from website.models import *
from website.auth import token_required  # Import token_required from the appropriate module

comments_routes = Blueprint('comments_routes', __name__)

# Adding a comment
@comments_routes.route('/api/comment', methods=['POST'])
@token_required
def add_comment(decoded_token):
    """
    API route to add a new community.
    """
    data = request.get_json()  # Get JSON data from the request
    if not data:
        return jsonify({"error": "No data provided"}), 400

    author_id = data.get('author_id')
    post_id = data.get('post_id')
    content = data.get('content')

    # Validate required fields
    if not content:
        return jsonify({"error": "content Required"}), 400


    # Get the user ID from the decoded token
    user_id = decoded_token.get('user_id')

   
    new_Comment = Comment(
        author_id=user_id, # Set the current user as the author
        post_id=post_id,
        content=content,
    )

    # Add to the database
    db.session.add(new_Comment)
    db.session.commit()

    return jsonify({"message": "Comment created successfully", "comment": {
        "id":new_Comment.id,
        "post_id": new_Comment.post_id,
        "content": new_Comment.content,
        "author_id": new_Comment.author_id
    }}), 201

# Fatching all comments
@comments_routes.route('/api/comments/<int:post_id>', methods=['GET'])
def fetch_Posts_comments(post_id):
    """
    API route to fetch comments.
    """
    return get_comments(post_id)

# Fatching current user's comments
# Handle preflight requests for CORS
@comments_routes.route('/api/comments/<int:post_id>', methods=['OPTIONS'])
def fetch_Posts_comments_preflight(user_id):
     # Handle preflight request
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
    return response, 200

