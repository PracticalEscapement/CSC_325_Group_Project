from flask import Blueprint, jsonify, request, make_response
from website.models import *
from website.auth import token_required  # Import token_required from the appropriate module

community_routes = Blueprint('community_routes', __name__)

# Adding a community
@community_routes.route('/api/communities', methods=['POST'])
@token_required
def add_community(decoded_token):
    """
    API route to add a new community.
    """
    data = request.get_json()  # Get JSON data from the request
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get('name')
    description = data.get('description', '')
    image_url = data.get('imageUrl', None)

    # Validate required fields
    if not name:
        return jsonify({"error": "Community name is required"}), 400

    # Check if the community already exists
    existing_community = Community.query.filter_by(name=name).first()
    if existing_community:
        return jsonify({"error": "Community with this name already exists"}), 400

    # Get the user ID from the decoded token
    user_id = decoded_token.get('user_id')

    # Create a new community
    new_community = Community(
        name=name,
        description=description,
        image_url=image_url,
        author_id=user_id,  # Set the current user as the author
        num_members=1  # Set initial number of members to 1
    )

    db.session.add(new_community)

    new_membership = Member(
    member_id=user_id,
    community_name=name
    )

    db.session.add(new_membership)

    db.session.commit()

    return jsonify({
        "message": "Community created successfully", 
        "community": {
        "name": new_community.name,
        "description": new_community.description,
        "image_url": new_community.image_url,
        "num_members" : 1,
        "author_id": new_community.author_id
    }}), 201

# Fatching all communities
@community_routes.route('/api/communities', methods=['GET'])
def fetch_all_communities():
    """
    API route to fetch all communities.
    """
    return get_all_comminities()

# Fatching current user's communities
# Handle preflight requests for CORS
@community_routes.route('/api/communities/<int:user_id>', methods=['OPTIONS'])
def fetch_user_communities_preflight(user_id):
     # Handle preflight request
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
    return response, 200

# Handle GET requests for fetching user communities
@community_routes.route('/api/communities/<int:user_id>', methods=['GET'])
@token_required
def fetch_user_communities_logged_in(decoded_token, user_id):
    """
    API route to fetch communities for the currently logged-in user.
    """
    # Ensure the user_id from the URL matches the user_id from the token
    if decoded_token.get('user_id') != user_id:
        return jsonify({"error": "Unauthorized access"}), 403
    
    # Fetch communities for the user
    return get_user_community(user_id)

# Fatching popular communities
@community_routes.route('/api/communities/popular', methods=['GET'])
def fetch_popular_communities():
    """
    API route to fetch popular communities.
    """
    # Example logic: Fetch communities sorted by the number of members
    communities = Community.query.order_by(Community.num_members.desc()).limit(10).all()
    data_list = [
        {
            "name": community.name,
            "description": community.description,
            "image_url": community.image_url,  # Assuming you have an image_url field
            "num_members": community.num_members
        }
        for community in communities
    ]
    return jsonify(data_list), 200

# Adding a new community member
@community_routes.route('/api/communities/<string:community_name>/add_member', methods=['POST'])
@token_required
def add_member(decoded_token, community_name):
    """
    API route to add a member to a community.
    """
    user_id = decoded_token.get('user_id')

    # Check if the community exists
    community = Community.query.filter_by(name=community_name).first()
    if not community:
        return jsonify({"error": "Community not found"}), 404

    # Check if the user is already a member
    existing_member = Member.query.filter_by(member_id=user_id, community_name=community_name).first()
    if existing_member:
        return jsonify({"error": "User is already a member of this community"}), 400

    # Add the user as a member
    new_member = Member(
        member_id=user_id,
        community_name=community_name
    )
    db.session.add(new_member)

    # Increment the num_members field
    community.num_members = (community.num_members or 0) + 1
    db.session.commit()

    return jsonify({"message": "User added to the community successfully"}), 200

# Removing a user from a community
@community_routes.route('/api/communities/<string:community_name>/remove_member', methods=['DELETE'])
@token_required
def remove_member(decoded_token, community_name):
    """
    API route to remove a member from a community.
    """
    user_id = decoded_token.get('user_id')

    # Check if the community exists
    community = Community.query.filter_by(name=community_name).first()
    if not community:
        return jsonify({"error": "Community not found"}), 404

    # Check if the user is a member
    member = Member.query.filter_by(member_id=user_id, community_name=community_name).first()
    if not member:
        return jsonify({"error": "User is not a member of this community"}), 400

    # Remove the user as a member
    db.session.delete(member)

    # Decrement the num_members field
    community.num_members = max((community.num_members or 1) - 1, 0)
    db.session.commit()

    return jsonify({"message": "User removed from the community successfully"}), 200

# Checks if a user is a member of a community
@community_routes.route('/api/communities/<string:community_name>/is_member', methods=['GET'])
@token_required
def check_membership(decoded_token, community_name):
    """
    API route to check if the logged-in user is a member of a specific community.
    """
    user_id = decoded_token.get('user_id')

    if is_user_member_of_community(user_id, community_name):
        return jsonify({"is_member": True}), 200
    else:
        return jsonify({"is_member": False}), 200