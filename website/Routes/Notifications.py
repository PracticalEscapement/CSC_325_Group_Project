from flask import Blueprint, jsonify, request, make_response
from website.models import *
from website.auth import token_required  # Import token_required from the appropriate module

Notifications_routes = Blueprint('Notifications_routes', __name__)

# Adding a comment
@Notifications_routes.route('/api/Notifications', methods=['POST'])
@token_required
def add_Notification(decoded_token):
    """
    API route to add a new Notification.
    """
    data = request.get_json()  # Get JSON data from the request
    if not data:
        return jsonify({"error": "No data provided"}), 400

    Belongs_to_user_id = data.get('belongs_to_user_id')
    is_read = data.get('is_read')
    message = data.get('message')
    link=data.get('link')

    # Validate required fields
    if not message:
        return jsonify({"error": "message Required"}), 400


    # Get the user ID from the decoded token
    user_id = decoded_token.get('user_id')

   
    new_Notification =Notification(
        belongs_to_user_id=Belongs_to_user_id, # Set the current user as the author
        is_read=is_read,
        message=message,
        link=link,
    )

    # Add to the database
    db.session.add(new_Notification)
    db.session.commit()

    return jsonify({"message": "Notification created successfully", "Notification": {
        "belongs_to_user_id":new_Notification.belongs_to_user_id,
        "is_read": new_Notification.is_read,
        "message": new_Notification.content,
        "link": new_Notification.author_id,
        "id": new_Notification.id,
        "created_at":new_Notification.created_at,
    }}), 201


@Notifications_routes.route('/api/Notification/<int:user_id>', methods=['GET'])
def fetch_Notifications(user_id):
    """
    API route to fetch Notifications.
    """
    return get_notifications(user_id)


# Handle preflight requests for CORS
@Notifications_routes.route('/api/Notification/<int:user_id>', methods=['OPTIONS'])
def fetch_Notifications_preflight(user_id):
     # Handle preflight request
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
    return response, 200

