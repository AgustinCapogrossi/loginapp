from flask import Blueprint, render_template, request, flash
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
        in_dni = request.form.get("dni")
        full_user_pre = []
        full_user = []
        for user in users:
            user_info = [user.name, user.last_name, str(user.dni), str(user.date)]
            full_user_pre.append(user_info)
        for i in range(1,len(full_user_pre),1):
            if full_user_pre[i][2] == str(in_dni):
                full_user.append(full_user_pre[i])
        if full_user == []:
            flash("There are no users with said DNI", category = "error")
    return render_template('home.html', user = current_user, list_users = full_user) #Check if the current user is authenticated
