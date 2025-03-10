from flask import Blueprint, render_template,request,flash,redirect,url_for
from . import db
from .models import user
from flask_login import login_user,logout_user,login_required,current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods =['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        email_exists= user.query.filter_by(email=email).first()


        if email_exists:
            
            if email_exists.password ==password:
                login_user(email_exists,remember=True)
                flash("logged in", category='success')
                return redirect(url_for('views.home'))
            else:
                flash("Wrong password",category='error')
            
        else:
            flash('email doesnt exists',category='success')
    return render_template("login.html")

@auth.route('/logout')
def logout():
    logout_user()
    return "<p>Logout</p>"

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
            new_User= user(email = email,username =Fname +" " +Lname, password=password1)
            db.session.add(new_User)
            db.session.commit()
            flash("user Created")
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")