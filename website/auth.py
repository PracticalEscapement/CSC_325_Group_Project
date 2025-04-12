from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from . import db
from .models import User
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import re


auth = Blueprint('auth', __name__)
auth.permanent_session_lifetime=timedelta(days=365*10)

# --- Login Route ---
@auth.route('/login', methods =['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash("Already Logged in","info")
        return redirect(url_for('views.home'))
    if request.method=='POST':
        session.permanent=True
        email = request.form.get('email')
        
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()


        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                session["user"]=email
                flash(f"Logged in successfully. Your user ID is: {user.id}", category='success')
                return redirect(url_for('views.home'))
            else:
                flash("WroIncorrectng password",category='error')
            
        else:
            flash('Email doesnt exists.', category='error')
    return render_template("login.html")


# --- Logout Route ---
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    user = session.pop("user", None)
    flash(f"You have been logged out, {user if user else 'user'}.", category='info')
    return redirect(url_for('views.home'))


# --- Sign Up Route ---
@auth.route('/sign-up', methods=['POST','GET'])
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
            return render_template("sign_up.html")

        email_exists = User.query.filter_by(email=email).first()

        if email_exists:
            flash("Email already exists.", category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        else:
            new_user = User(
                email=email,
                username = f"{Fname} {Lname}".strip(),
                password=generate_password_hash(password1)
            )
            db.session.add(new_user)
            db.session.commit()

            flash("User created successfully!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")

    