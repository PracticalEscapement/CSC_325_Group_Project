from flask import Blueprint, jsonify, request
from website.models import *
from flask_login import current_user, login_required

community_routes = Blueprint('community_routes', __name__)

# Adding a community
@community_routes.route('/api/communities', methods=['POST'])
@login_required
def add_community():
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

    # Create a new community
    new_community = Community(
        name=name,
        description=description,
        image_url=image_url,
        author_id=current_user.id  # Set the current user as the author
    )

    # Add to the database
    db.session.add(new_community)
    db.session.commit()

    return jsonify({"message": "Community created successfully", "community": {
        "name": new_community.name,
        "description": new_community.description,
        "imageUrl": new_community.image_url,
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
@community_routes.route('/api/communities/<int:user_id>', methods=['GET'])
@login_required
def fetch_user_communities_logged_in():
    """
    API route to fetch communities for the currently logged-in user.
    """
    return get_user_community(current_user.id)

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
            "imageUrl": community.image_url,  # Assuming you have an image_url field
            "num_members": community.num_members
        }
        for community in communities
    ]
    return jsonify(data_list), 200