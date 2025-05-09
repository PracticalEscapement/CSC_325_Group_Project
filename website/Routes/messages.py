from flask import Blueprint, jsonify, request, make_response
from website.models import *
from website.auth import token_required  # Import token_required from the appropriate module

Messages_routes = Blueprint('Messages_routes', __name__)

# Adding a comment
@Messages_routes.route('/api/Messages', methods=['POST'])
@token_required
def add_Message(decoded_token):
    """
    API route to add a new Message
    """
    data = request.get_json()  # Get JSON data from the request
    if not data:
        return jsonify({"error": "No data provided"}), 400

    
    sender_id = data.get('sender_id')
    reciever_id= data.get('reciever_id')
    content =data.get('content')
    is_read = data.get('is_read')

    # Validate required fields
    if not content:
        return jsonify({"error": "content Required"}), 400


    # Get the user ID from the decoded token
    user_id = decoded_token.get('user_id')

   
    new_Message = Message(
        sender_id=sender_id, # Set the current user as the author
        reciever_id=reciever_id,
        is_read=is_read,
        content=content,
    )

    # Add to the database
    db.session.add(new_Message)
    db.session.commit()

    return jsonify({"message": "Post created successfully", "Post": {
        "Sender_id":new_Message.sender_id,
        "is_read":new_Message.is_read,
        "reciever_id":new_Message.receiver_id,
        "Content":new_Message.content,
        "Id":new_Message.id,
        "Created_at":new_Message.created_at,
    }}), 201


@Messages_routes.route('/api/Message/<int:receiver_id>', methods=['GET'])
def fetch_Messages(receiver_id):
    """
    API route to fetch community Posts.
    """
    
    return get_messages(receiver_id)



@Messages_routes.route('/api/Message/<int:receiver_id>', methods=['OPTIONS'])
def fetch_Messages_preflight(receiver_id):
     # Handle preflight request
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
    return response, 200

