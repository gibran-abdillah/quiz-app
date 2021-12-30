from app.main import main_blueprint as main 
from flask import render_template

@main.route('/')
def main_index():
    return render_template('main/index.html')