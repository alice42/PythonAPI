import uuid
import datetime
from flask_restplus import inputs
from app.main import db
from app.main.model.user import User
from app.main.util.decorator import token_required

from app.main.service.auth_helper import Auth

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

def check_user_permission(user, token):
    try:
        if token:
            auth_token = token.split(" ")[0]
        else:
            response_object = {
                'status': 'fail',
                'message': 'You must be logged in to delete your account'
            }
            return response_object, 401
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            to_authentify = User.query.filter_by(id=resp).first()
            if to_authentify == user:
                authentified_user = True
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'You can only delete our own account'
                }
                return response_object, 401
        if authentified_user:
            Auth.logout_user(data=token)
            db.session.delete(user)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Successfully deleted.'
            }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def save_updated_user(user, data, token):
    if data['birthday']:
        data['birthday'] = inputs.datetime_from_iso8601(data['birthday'])
    user_update = User.query.filter_by(public_id=user.public_id).update(data)
    if not user_update :
        response_object = {
            'status': 'fail',
            'message': 'User doesn\'t exists. Please check given ID.',
        }
        return response_object, 409
    else:
        if token:
            auth_token = token.split(" ")[0]
        else:
            response_object = {
                'status': 'fail',
                'message': 'You must be logged in to update your profil'
            }
            return response_object, 401
        if auth_token:
            user_to_update = User.query.filter_by(public_id=user.public_id).first()
            resp = User.decode_auth_token(auth_token)
            to_authentify = User.query.filter_by(id=resp).first()
            if to_authentify.id == user_to_update.id:
                authentified_user = True
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'You can only update your profil'
                }
                return response_object, 401
        if authentified_user:
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'User profil successfully updated.',
            }
            return response_object, 201