from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Logged in successfully!", category = "success")
                login_user(user,remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Either password or email are incorrect", category = "error")
        else:
            flash("Email does not exst.", category = "error")
    return render_template("login.html",user = current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        last_name = request.form.get("last_name")
        dni = request.form.get("dni")
        password = request.form.get("password")

        user = User.query.filter_by(email = email).first()
        
        if user:
            flash("User already exists",category= "error")
        elif(len(email) < 4):
            flash("Email must be greater than 3 characters", category= "error")
        elif len(name) < 2:
            flash("Name must be greater than 1 characters", category= "error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters", category= "error")
        else:
            
            new_user = User(email=email,password=generate_password_hash(password, method = "sha256"),name=name,last_name=last_name,dni=dni)
            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash("Account created", category= "success")
            return redirect(url_for("views.home"))
    return render_template("signup.html", user = current_user)
