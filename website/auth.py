from flask import Blueprint, render_template,request,flash,redirect,url_for,session
from . import db
from .models import user
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
auth = Blueprint('auth', __name__)
auth.permanent_session_lifetime=timedelta(days=365*10)
@auth.route('/login', methods =['GET','POST'])
def login():
    if"user" in session:
        flash("Already Logged in","info")
        return redirect(url_for('views.home'))
    if request.method=='POST':
        session.permanent=True
        email = request.form.get('email')
        
        password = request.form.get('password')
        email_exists= user.query.filter_by(email=email).first()


        if email_exists:
            session["user"]=email
            if check_password_hash(email_exists.password,password):
                login_user(email_exists,remember=True)
                flash(f"logged in you id is: +{email_exists.id}", category='success')
                return redirect(url_for('views.home'))
            else:
                flash("Wrong password",category='error')
            
        else:
            flash('email doesnt exists',category='success')
    return render_template("login.html")

@auth.route('/logout')
def logout():
    if "user" in session:
        user = session["user"]
        
        flash(f"You have been logged out, {user}")
    else:
        flash("You are already logged out")
    session.pop("user",None)
    return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=['POST','GET'])
def sign_up():
    if request.method =="POST":
        email = request.form.get("email")
        Fname = request.form.get("firstName")
        Lname =request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 =request.form.get("password2")

        email_exists =user.query.filter_by(email=email).first()


        if email_exists:
            flash("Email already exists.", category='error')
        elif password1!=password2:
            flash("Passwords dont match.",  category = 'error')
        else:
            new_User= user(email = email,username =Fname +" " +Lname, password=generate_password_hash(password1))
            db.session.add(new_User)
            db.session.commit()
            
            flash("user Created")
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")

    