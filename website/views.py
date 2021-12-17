from flask import Blueprint, render_template, request
from flask_login import login_required,current_user
views = Blueprint("views", __name__)
from .models import User
from operator import itemgetter

@views.route("/",methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        users = User.query.all()
        full_user = []
        for user in users:
            user_info = [user.name, user.last_name, str(user.dni), str(user.date)]
            full_user.append(user_info)
    if request.method == "POST":
        users = User.query.all()
        full_user = []
        for user in users:
            user_info = [user.name, user.last_name, str(user.dni), str(user.date)]
            full_user.append(user_info)
        full_user = sorted(full_user, key=itemgetter(2))
    return render_template('home.html', user = current_user, list_users = full_user) #Check if the current user is authenticated
