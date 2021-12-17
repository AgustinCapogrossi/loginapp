from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Client
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
                new_client = Client(email=email,name=current_user.name,last_name=current_user.last_name,dni=current_user.dni, user_id= current_user.id)
                db.session.add(new_client)
                db.session.commit()

                return redirect(url_for("views.home"))
            else:
                flash("Either password or email are incorrect", category = "error")
        else:
            flash("Email does not exist.", category = "error")
    return render_template("login.html",user = current_user)

@auth.route("/restore", methods=["GET", "POST"])
def restore():
    if request.method == "POST":
        email = request.form.get("email")
        dni = request.form.get("dni")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email = email).first()
        user2 = User.query.filter_by(dni = dni).first()
        if (user.email == email):
            if(str(user2.dni) == str(dni)):
                user.password = generate_password_hash(password1, method = "sha256")
                db.session.commit()
                flash("Account updated", category= "success")
                return redirect(url_for("auth.login"))
            else:
                flash("Incorrect DNI.", category = "error")
        else:
            flash("User does not exist.", category = "error")
        if(password1 != password2):
            flash("Password does not match.", category = "error")
        elif(len(email)<5):
            flash("Email is too short", category = "error")

    return render_template("restore.html",user = current_user)


@auth.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email = email).first()
        client = Client.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Account successfully deleted!", category = "success")
                db.session.delete(client)
                db.session.commit()
                db.session.delete(user)
                db.session.commit()
                return redirect(url_for("auth.login"))
            else:
                flash("Either the password or the email are incorrect", category = "error")
        else:
            flash("Email does not exst.", category = "error")
    return render_template("delete.html", user= current_user)

@auth.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        last_name = request.form.get("last_name")
        dni = request.form.get("dni")
        password = request.form.get("password")
        
        user = User.query.filter_by(email = email).first()
        user2 = User.query.filter_by(dni = dni).first()
        if user:
            flash("Email is already in use", category= "error")
        elif user2:
            flash("DNI already in use.",category = "error")
        elif(len(email) < 4):
            flash("Email must be greater than 3 characters", category= "error")
        elif len(name) < 2:
            flash("Name must be greater than 1 characters", category= "error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters", category= "error")
        else:
            client = Client.query.filter_by(id = current_user.id).first() 
            client.name = name
            client.last_name = last_name
            client.email= email
            client.dni = dni
            db.session.commit()

            current_user.email = email 
            current_user.name = name
            current_user.last_name = last_name
            current_user.dni = dni
            current_user.password = generate_password_hash(password, method = "sha256") 
            db.session.commit()
            flash("Account updated", category= "success")
            return redirect(url_for("views.home"))
    return render_template("update.html", user = current_user)

@auth.route("/logout")
@login_required
def logout():
    email = current_user.email
    client = Client.query.filter_by(email = email).first()
    db.session.delete(client)
    db.session.commit()
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
        user2 = User.query.filter_by(dni = dni).first()
        if user:
            flash("User already exists",category= "error")
        elif user2:
            flash("DNI already exists",category= "error")
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
            new_client = Client(email=email,name=name,last_name=last_name,dni=dni, user_id= new_user.id)
            db.session.add(new_client)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("Account created", category= "success")
            return redirect(url_for("views.home"))
    return render_template("signup.html", user = current_user)
