from flask import Blueprint

quiz_blueprint = Blueprint('quiz', 
                           __name__, 
                           url_prefix='/quiz'
                )

from .views import * 