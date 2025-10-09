from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from qns2b import login_manager
from models.users import User
from models.forms import RegForm


auth = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.getUserById(user_id)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegForm()
    if form.validate_on_submit():
        existing_user = User.getUser(email=form.email.data)
        if not existing_user:
            hashpass = generate_password_hash(
                form.password.data, 
                method = 'pbkdf2:sha256'
            )
            user = User.createUser(
                email=form.email.data, 
                password=hashpass, 
                name=form.name.data
            )
            flash(f'{user.name} registered with email {user.email}')
            return redirect(url_for('auth.login'))
        else:
            flash(f'{form.email.data} was previously registered already.')
            form.email.errors.append("User already existed")
            return render_template(
                'register.html', 
                form = form, 
                panel = "Register"
            )
    
    return render_template('register.html', form=form, panel="Register")


@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = RegForm()
    if form.validate_on_submit():
        user = User.getUser(email=form.email.data)
        if user:
            if check_password_hash(user["password"], form.password.data):
                login_user(user)
                return redirect(url_for("home"))
            else:
                form.password.errors.append("User Password Not Correct")
        else:
            form.email.errors.append("No Such User")

    return render_template('login.html', form=form, panel="Login")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
