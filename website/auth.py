from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Client
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Permite al usuario iniciar sesión en su cuenta.

    Returns:
        Genera un cliente asociado al usuario en la base de datos y redirige a la pagina de home.
    """
    if request.method == "POST":
        #Obtener la información del post
        email = request.form.get("email")
        password = request.form.get("password")
        #Filtrar solo al usuario con el email ingresado
        user = User.query.filter_by(email = email).first()
        #Revisar si existe
        if user:
            #Revisar si es su contraseña
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
    """Permite que el usuario recupere su contraseña al ingresar su DNI y Email.

    Returns:
        Redirige a la pagina de inicio de sesión.
    """
    if request.method == "POST":
        #Obtener valores del formulario
        email = request.form.get("email")
        dni = request.form.get("dni")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #Obtener usuario
        user = User.query.filter_by(email = email).first()
        user2 = User.query.filter_by(dni = dni).first()
        if(len(email)<5):
            flash("Email is too short", category = "error")
        if(len(password1)<6):
            flash("Email is too short", category = "error")
        #Revisar que el email esté en la base de datos
        if user:
            #Revisar que el dni esté en la base de datos
            if user2:
                #Revisar que tanto el dni como el email sean del mismo usuario
                if (user.email == email):
                    if(str(user.dni) == str(dni)):
                        #Revisar que las contraseñas coincidan
                        if password1 == password2:
                            #Generar hashing para contraseña y asignarsela al usuario
                            user.password = generate_password_hash(password1, method = "sha256")
                            db.session.commit()
                            flash("Account updated", category= "success")
                            return redirect(url_for("auth.login"))
                        else:
                            flash("Passwords don't match.", category = "error")    
                    else:
                        flash("Incorrect DNI.", category = "error")
                else:
                    flash("Incorrect email.", category = "error")
            else:
                flash("User does not exist.", category = "error")    
        else:
            flash("User does not exist.", category = "error")
    return render_template("restore.html",user = current_user)


@auth.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Elimina un usuario y su cliente asociado de la base de datos.

    Returns:
        Redirige a la pagina de inicio de sesión.
    """
    if request.method == "POST":
        #Obtener información.
        email = request.form.get("email")
        password = request.form.get("password")

        #Obtener usuario y el cliente correspondiente.
        user = User.query.filter_by(email = email).first()
        client = Client.query.filter_by(email = email).first()
        #Revisar que el usuario existe.
        if user:
            if user.name == current_user.name:
                #Si la contraseña coincide eliminar usuario
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
                flash("The account you're trying to delete is not the one you're logged in to.", category = "error")
        else:
            flash("Email does not exst.", category = "error")
    return render_template("delete.html", user= current_user)

@auth.route("/update", methods=["GET", "POST"])
@login_required
def update():
    """Permite al usuario cambiar los parámetros de su perfil.

    Returns:
        Valores del cliente y usuario actualizados en la base de datos.
    """
    if request.method == "POST":
        #Obtener información
        email = request.form.get("email")
        name = request.form.get("name")
        last_name = request.form.get("last_name")
        dni = request.form.get("dni")
        password = request.form.get("password")

        #Verificar que el usuario exista
        user = User.query.filter_by(email = email).first()
        user2 = User.query.filter_by(dni = dni).first()

        if user:
            flash("Email is already in use", category= "error")
        else:
            flash("User does not exist", category= "error")
        if user2:
            flash("DNI already in use.",category = "error")
        else:
            flash("Email is already in use", category= "error")
        if(len(email) < 4):
            flash("Email must be greater than 3 characters", category= "error")
        elif len(name) < 2:
            flash("Name must be greater than 1 characters", category= "error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters", category= "error")
        else:
            #Actualiza los parámetros del cliente los parámetros obtenidos del formulario
            client = Client.query.filter_by(user_id = current_user.id).first() 
            client.name = name
            client.last_name = last_name
            client.email= email
            client.dni = dni
            db.session.commit()
            #Actualiza los parámetros del usuario con los parámetros obtenidos del formulario
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
    """Cierra la sesión de un usuario y elimina el cliente asociado de la base de datos.

    Returns:
        Redirige a la pagina de inicio de sesión.
    """
    #Buscamos al usuario que esté en sesión que quiere cerrarla.
    email = current_user.email
    client = Client.query.filter_by(email = email).first()
    #Elimina el cliente
    db.session.delete(client)
    db.session.commit()
    #Cierra la sesión del usuario
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    """Permite crear una nueva cuenta

    Returns:
        Se agrega el ususario a la base de datos junto a su cliente asociado y redirige a la página home.
    """
    if request.method == "POST":
        #Obtiene los datos del formulario.
        email = request.form.get("email")
        name = request.form.get("name")
        last_name = request.form.get("last_name")
        dni = request.form.get("dni")
        password = request.form.get("password")

        #Revisa que el usuario no exista aún.
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
            #Crea un nuevo usuario en la base de datos
            new_user = User(email=email,password=generate_password_hash(password, method = "sha256"),name=name,last_name=last_name,dni=dni)
            db.session.add(new_user)
            db.session.commit() 
            #Crea un nuevo cliente asociado al usuario
            new_client = Client(email=email,name=name,last_name=last_name,dni=dni, user_id= new_user.id)
            db.session.add(new_client)
            db.session.commit()
            #Inicia la sesion del usuario creado
            login_user(new_user,remember=True)
            flash("Account created", category= "success")
            return redirect(url_for("views.home"))
    return render_template("signup.html", user = current_user)
