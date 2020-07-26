import uuid
import datetime

from app.main import db
from app.main.model.property import Property
from app.main.model.user import User
from app.main.util.decorator import token_required

def save_new_property(data, token):
    property = Property.query.filter_by(name=data['name']).first()
    if token:
        auth_token = token.split(" ")[0]
    else:
        auth_token = ''
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        user = User.query.filter_by(id=resp).first()
    else:
        user= ''
    if not user:
        response_object = {
            'status': 'fail',
            'message': 'You must be register to create a property.',
            }
        return response_object, 409
    if not property:
        if not data["name"] \
            or not data["city"] or not data["description"] \
            or not data["rooms_count"] \
            or not data["property_type"]:
            response_object = {
                'status': 'fail',
                'message': 'All fields excepts public_id are required',
            }
            return response_object, 409
        else:
            new_property = Property(
                public_id=str(uuid.uuid4()),
                name=data['name'],
                owner=user.public_id,
                city=data['city'],
                description=data['description'],
                rooms_count=data['rooms_count'],
                property_type=data['property_type'],
                user_id=user.id
            )
            save_changes(new_property)
            response_object = {
                'status': 'success',
                'message': 'Successfully created.',
            }
            return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Property with this name already exists.',
        }
        return response_object, 409

def get_all_properties():
    return Property.query.all()


def get_a_property(public_id):
    return Property.query.filter_by(public_id=public_id).first()

def save_updated_property(public_id, data, token):
    property = Property.query.filter_by(public_id=public_id).update(data)
    if not property:
        response_object = {
            'status': 'fail',
            'message': 'Property doesn\'t exists. Please check given ID.',
        }
        return response_object, 409
    else:
        if token:
            auth_token = token.split(" ")[0]
        else:
            response_object = {
                'status': 'fail',
                'message': 'You must be logged in to update your property'
            }
            return response_object, 401
        if auth_token:
            property_to_update = Property.query.filter_by(public_id=public_id).first()
            resp = User.decode_auth_token(auth_token)
            to_authentify = User.query.filter_by(id=resp).first()
            if to_authentify.id == property_to_update.user_id:
                authentified_user = True
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'You can only update your properties'
                }
                return response_object, 401
        if authentified_user:
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Property successfully updated.',
            }
            return response_object, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()

def check_user_permission(public_id, token):
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
            property_to_update = Property.query.filter_by(public_id=public_id).first()
            resp = User.decode_auth_token(auth_token)
            to_authentify = User.query.filter_by(id=resp).first()
            if to_authentify.id == property_to_update.id:
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
