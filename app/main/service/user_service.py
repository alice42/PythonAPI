import uuid
import datetime

from app.main import db
from app.main.model.user import User
from app.main.util.decorator import token_required

def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    username = User.query.filter_by(username=data['username']).first()
    if not user and not username:
        if not data["password"] \
            or not data["email"] \
            or not data["username"]:
            response_object = {
                'status': 'fail',
                'message': 'All fields excepts public_id are required',
            }
            return response_object, 409
        else :
            new_user = User(
                public_id=str(uuid.uuid4()),
                email=data['email'],
                username=data['username'],
                password=data['password'],
                registered_on=datetime.datetime.utcnow()
            )
            save_changes(new_user)
            return generate_token(new_user)
    else:
        if not user and username:
            response_object = {
                'status': 'fail',
                'message': 'Username already exists. Please choose a new one.',
            }
        elif user and not username:
            response_object = {
                'status': 'fail',
                'message': 'Email already exists. Please Log in.',
            }
        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
        return response_object, 409

def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()

def generate_token(user):
    try:
        # generate the auth token
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401