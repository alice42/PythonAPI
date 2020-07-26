from flask_restplus import Namespace, fields

class PropertyDto:
    api = Namespace('property', description='properties related operations')
    property = api.model('property', {
        'public_id': fields.String(description='property Identifier'),
        'name' : fields.String(required=True, description='property name'),
        'description' : fields.String(required=True, description='property description'),
        'property_type' : fields.String(required=True, description='Type of property'),
        'city' : fields.String(required=True, description='property city'),
        'rooms_count' : fields.Integer(required=True, description='property number of rooms'),
        'owner' : fields.String(required=True, description='property owner'),
    })
    property_update = api.model('property_update', {
        'name' : fields.String(description='property name', attribute='private_name', null_allow=True),
        'description' : fields.String( description='property description', null_allow=True),
        'property_type' : fields.String( description='Type of property', null_allow=True),
        'city' : fields.String( description='property city'),
        'rooms_count' : fields.Integer( description='property number of rooms'),
    })

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier'),
        'properties': fields.List(fields.Nested(PropertyDto.property), description='list of created properties', null_allow=True)
    })
    user_update = api.model('user_update', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })