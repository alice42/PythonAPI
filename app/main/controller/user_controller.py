from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, \
    get_all_users, \
    get_a_user, \
    check_user_permission, \
    save_updated_user

from app.main.util.decorator import token_required

api = UserDto.api
_user = UserDto.user
_user_update = UserDto.user_update
_user_editable = UserDto.user_editable

@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @token_required
    @api.marshal_list_with(_user)
    def get(self):
        """List all registered users"""
        return get_all_users()
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user_update, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)

@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @token_required
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
    @api.response(201, 'User successfully updated.')
    @api.doc('update a user')
    @token_required
    @api.expect(_user_editable, validate=True)
    def patch(self, public_id):
        """update a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            data = request.json
            auth_header = request.headers.get('Authorization')
            return save_updated_user(user=user, data=data, token=auth_header)
    @api.doc('delete a user')
    @token_required
    def delete(self, public_id):
        """delete a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            auth_header = request.headers.get('Authorization')
            return check_user_permission(user=user, token=auth_header)
