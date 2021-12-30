from datetime import datetime
from app import create_app
from app.modules.utils import generate_password
from flask_wtf.csrf import CSRFError
from flask import jsonify
import os

app = create_app(os.environ.get('FLASK_ENV','development'))

from app.db import db, quiz

@app.before_first_request 
def seed_data():
    """"
    if there was no user with admin role, add new one
    login with 
        * username : admin
        * password : admin1
    
    you can change the email, username, password in dashboard
    """
    cek = db.users.find_one({})
    if not cek:
        
        data = {}

        data['full_name'] = 'Admin Web'
        data['username'] = 'admin'
        data['password'] = generate_password('admin1')
        data['joined_at'] = datetime.utcnow()
        data['email'] = 'yourmail@gmail.com'
        data['type'] = 1 

        insert_data = db.users.insert_one(data)
        if insert_data.inserted_id:
            app.logger.info('new user added')
    
@app.errorhandler(CSRFError)
def error_csrf(e):
    return jsonify(status='fail', errors='CSRF Error, please refresh the page')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
