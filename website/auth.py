from flask import current_app
from flask import Blueprint, render_template, request, flash, redirect, url_for, session,jsonify,make_response
from . import db
from .models import *
from flask_login import login_user,logout_user,login_required,current_user
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
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!':'Token is missing'}),403
        try:
            decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except: 
            return jsonify({'message':'token is invalid'}),401
        return func(*args,**kwargs)
    return decorated

@auth.route('api/is_logged_in', methods=['GET'])
def is_logged_in():
    """
    Check if the user is logged in.
    """
    print("Authentification request!")
    if current_user.is_authenticated:
        print("Succeed")
        return jsonify({
            "logged_in": True,
            "user_id": current_user.id,
            "username": current_user.username
        }), 200
    else:
        print("Failed")
        return jsonify({"is_logged_in": False}), 200

# --- Login Route ---
@auth.route('api/login', methods =['POST'])
def login():
    if current_user.is_authenticated:
        flash("Already Logged in","info")
        return jsonify({"response":"Already Logged in"}), 200
    
    if request.method=='POST':
        session.permanent=True

        # Parse JSON data from the request body
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get('email')
        password = data.get('password')

        print('Email', email)
        print("Password:", password)
        
        user = User.query.filter_by(email=email).first()

       
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                session["user"]=user.username
                token= jwt.encode({
                    'user':email,
                    'exp' :datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                },current_app.config['SECRET_KEY'])


                if isinstance(token, str):
                    token = token.encode('UTF-8')

                response = make_response(jsonify({"message": "Login successful"}), 200)
                response.set_cookie(
                    'token', # Cookie name
                    token.decode('UTF-8'), # Token value
                    httponly=True,  # Prevent JavaScript access to the cookie
                    secure=False,  # Set to True if using HTTPS
                    samesite='Lax'  # Restrict cross-site cookie sharing
                )
                #print()
                return response
            else:
                print('Invalid username or password')
                return jsonify({"error":"Invalid username or password"}), 401
            
        else:
            print('Email does not exist')
            return jsonify({"response": "Email does not exist", "status": "error"}), 401
    

@auth.route('/<user_id>')
def info(user_id):
    user= User.query.get_or_404(user_id)
    return jsonify(f"ID: {user.id}")

# --- Logout Route ---
@auth.route('/logout',methods =['GET'])
@login_required
def logout():
    logout_user()
    user = session.pop("user", None)
    flash(f"You have been logged out, {user if user else 'user'}.", category='info')
    return jsonify({"response":f"You have been logged out, {user if user else 'user'}."})


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