from flask import Blueprint, render_template, request
from flask_login import login_required,current_user
views = Blueprint("views", __name__)
from .models import User

@views.route("/",methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        users = User.query.all()
        full_user = []
        for user in users:
            user_info = [user.name, user.last_name, user.dni, user.date]
            full_user.append(user_info)
    return render_template('home.html', user = current_user, list_users = users) #Check if the current user is authenticated
