from flask import Blueprint

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard')

from .views import * 
from .admin import *
