from flask import request
from flask_restplus import Resource, reqparse

from ..util.dto import PropertyDto
from ..service.property_service import save_new_property, \
    get_all_properties, \
    get_a_property, \
    save_updated_property, \
    check_user_permission

from app.main.util.decorator import token_required

api = PropertyDto.api
_property = PropertyDto.property
_property_update = PropertyDto.property_update

@api.route('/')
class PropertyList(Resource):
    @api.doc('list_of_registered_properties')
    # @token_required
    @api.marshal_list_with(_property, envelope='data')
    def get(self):
        """List all registered properties"""
        return get_all_properties()

    @api.response(201, 'Property successfully created.')
    @api.doc('create a new property')
    # @token_required
    @api.expect(_property_update, validate=True)
    def post(self):
        """Creates a new Property """
        data = request.json
        auth_header = request.headers.get('Authorization')
        return save_new_property(data=data, token=auth_header)


@api.route('/<public_id>')
@api.param('public_id', 'The Property identifier')
@api.response(404, 'Property not found.')
class Property(Resource):
    @api.doc('get a property')
    # @token_required
    @api.marshal_with(_property)
    def get(self, public_id):
        """get a property given its identifier"""
        property = get_a_property(public_id)
        if not property:
            api.abort(404)
        else:
            return property
    # PUT/PATCH
    @api.response(201, 'Property successfully updated.')
    @api.doc('update a property')
    # @token_required
    @api.expect(_property_update, validate=True)
    def patch(self, public_id):
        """update a property given its identifier"""
        data = request.json
        auth_header = request.headers.get('Authorization')
        return save_updated_property(public_id=public_id, data=data, token=auth_header)
    # @api.doc('delete a user')
    # @token_required
    def delete(self, public_id):
        """delete a user given its identifier"""
        auth_header = request.headers.get('Authorization')
        return check_user_permission(public_id=public_id, token=auth_header)