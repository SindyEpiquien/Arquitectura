# services/users/project/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
# instanciado la db
db = SQLAlchemy()
toolbar = DebugToolbarExtension()


def create_app(script_info=None):

    app = Flask(__name__)
<<<<<<< HEAD
    # habilitando CORS
    CORS(app)  # nuevo
    # estableciendo configuración
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    # configurando extensiones
    db.init_app(app)
    toolbar.init_app(app)
    # register blueprints
=======
    CORS(app)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    db.init_app(app)
    toolbar.init_app(app)
>>>>>>> refs/remotes/origin/master
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)
    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app
