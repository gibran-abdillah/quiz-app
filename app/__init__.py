from flask import Flask
from .modules.utils import Mongo_Utils
from config import configuration
from flask_wtf.csrf import CSRFProtect

# additional modules

mongo_utils = Mongo_Utils()
csrf_protect = CSRFProtect()

def create_app(env_type: str='development'):
    app = Flask(__name__)

    # init configuration from flask app 

    app.config.from_object(configuration[env_type])
    mongo_utils.init_app(app)
    csrf_protect.init_app(app)

    # import and register the blueprints to flask app

    from app.dashboard import dashboard_blueprint
    from app.auth import auth_blueprint
    from app.main import main_blueprint
    from app.api import api_blueprint
    from app.quiz import quiz_blueprint


    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(quiz_blueprint)


    return app 

