# services/users/project/__init__.py


import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

# instanciado la db
db = SQLAlchemy()
toolbar = DebugToolbarExtension()  # nuevo


# nuevo
def create_app(script_info=None):
    # instanciando app
    app = Flask(__name__)

    
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    
    db.init_app(app)
    toolbar.init_app(app)  

   
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

  
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
