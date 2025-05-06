from flask import current_app
from flask import Blueprint, render_template, request, flash, redirect, url_for, session,jsonify,make_response
from . import db
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import re
import jwt
import datetime
from functools import wraps

auth = Blueprint('auth', __name__)
auth.permanent_session_lifetime=timedelta(days=365*10)



def token_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token = request.headers.get('Authorization')        # Retrieve token from Authorization header
        if not token:
            return jsonify({'Alert!':'Token is missing'}),403
        
        # Handle "Bearer <token>" format
        if token.startswith("Bearer "):
            token = token.split(" ")[1]  # Extract the actual token

        try:
            decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        return func(decoded_token, *args,**kwargs)
    return decorated

@auth.route('api/is_logged_in', methods=['GET'])
@token_required
def is_logged_in(decoded_token):
    """
    Check if the user is logged in.
    """
    print("Authentification request!")

    user_id = decoded_token.get('user_id')
    user = User.query.get(user_id)
    if user:
        print("Succeed")
        print(user.username)
        return jsonify({
            "logged_in": True,
            "user_id": user_id,
            "username": user.username
        }), 200
    else:
        print("Failed")
        return jsonify({"is_logged_in": False}), 200

# --- Login Route ---
@auth.route('api/login', methods =['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    # Parse JSON data from the request body
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

        
    email = data.get('email')
    password = data.get('password')

    print('Email', email)
    print("Password:", password)
        
    user = User.query.filter_by(email=email).first()

       
    if user and check_password_hash(user.password, password):
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=200)  # Token expires in 1 hour
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            "message": "Login successful",
            "token": token
        }), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401
    

@auth.route('/<user_id>')
def info(user_id):
    user= User.query.get_or_404(user_id)
    return jsonify(f"ID: {user.id}")

# --- Logout Route ---
# @auth.route('/logout',methods =['GET'])
# @token_required
# def logout():
#     logout_user()
#     user = session.pop("user", None)
#     flash(f"You have been logged out, {user if user else 'user'}.", category='info')
#     return jsonify({"response":f"You have been logged out, {user if user else 'user'}."})


# --- Sign Up Route ---
@auth.route('/sign-up', methods=['POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        Fname = request.form.get("firstName", "").strip()
        Lname = request.form.get("lastName", "").strip()
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Email format validation
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            flash("Invalid email address.", category='error')
            return jsonify({"response":"Invalid email address."})
        email_exists = User.query.filter_by(email=email).first()

        if email_exists:
            flash("Email already exists.", category='error')
            return jsonify({"response":"Email already exists."})
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
            return jsonify({"response":"Passwords don't match."})
        else:
            new_user = User(
                email=email,
                username = f"{Fname}{Lname}".strip(),
                password=generate_password_hash(password1)
            )
            db.session.add(new_user)
            db.session.commit()

            flash("User created successfully!", category='success')
            return jsonify({"response":"User created successfully!"})