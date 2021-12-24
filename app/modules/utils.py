import random
import string
from bson.objectid import ObjectId
from .mongo import Mongo_Utils
from werkzeug.security import generate_password_hash, check_password_hash
import json, bson 
from bson.json_util import default
from bson import ObjectId

CHAR = string.ascii_lowercase + string.digits

def json_decoder(json_response):
    return json.loads(
        json.dumps(json_response, 
                   default=default)
    )

def generate_code(nums: int=6):
    return ''.join(random.choice(CHAR) for _ in range(nums))

def generate_password(password):
    return generate_password_hash(password, method='sha512')

def check_password(pw_hash, password):
    return check_password_hash(pw_hash, password)

