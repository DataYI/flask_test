from flask import flash, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed

bcrypt = Bcrypt()
principals = Principal()

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

login_manager = LoginManager()
login_manager.login_view = 'main.log'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please login to access this page'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.get(userid)


