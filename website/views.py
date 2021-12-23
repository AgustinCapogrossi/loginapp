from flask import Blueprint, render_template, request, flash
from flask_login import login_required,current_user
views = Blueprint("views", __name__)
from .models import User
from operator import itemgetter

@views.route("/",methods = ["GET", "POST"])
def home():
    """Carga la pagina principal con una lista de usuarios y posibilidad de filtrar por DNI

    Returns:
        Pagina principal.
    """
    #Revisa que tipo de método es
    if request.method == "GET":
        #Consigue una lista con todos los User de la base de datos
        users = User.query.all()
        full_user = []
        #Agrega la informacion de cada usuario de manera organizada a un arreglo
        for user in users:
            user_info = [user.name, user.last_name, str(user.dni), str(user.date)]
            full_user.append(user_info)
    if request.method == "POST":
        #Consigue una lista con todos los User de la base de datos
        users = User.query.all()
        #Consigue el valor del dni del formulario
        in_dni = request.form.get("dni")
        full_user_pre = []
        full_user = []
        #Agrega la informacion de cada usuario de manera organizada a un arreglo
        for user in users:
            user_info = [user.name, user.last_name, str(user.dni), str(user.date)]
            full_user_pre.append(user_info)
        #Filtra el arreglo organizado y devuelve el usuario cuyo DNI coincida con el del formulario.
        for i in range(1,len(full_user_pre),1):
            if full_user_pre[i][2] == str(in_dni):
                full_user.append(full_user_pre[i])
        if full_user == []:
            flash("There are no users with said DNI", category = "error")
    return render_template('home.html', user = current_user, list_users = full_user) #Check if the current user is authenticated
