# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 11:58:59 2018

@author: DataAnt
"""
from flask import Flask, redirect, url_for
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed

from .config import DevConfig
from .models import db
from .extensions import bcrypt, login_manager, principals
from .controllers.blog import blog_blueprint
from .controllers.main import main_blueprint

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)  
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))


    # @app.route('/')
    # def index():
    #     return redirect(url_for('blog.home'))
    
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(blog_blueprint)
    return app


if __name__ == '__main__':
    app = create_app(DevConfig)
    app.run()