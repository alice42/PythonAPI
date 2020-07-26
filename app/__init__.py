# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.property_controller import api as property_ns

blueprint = Blueprint('api', __name__)

authorizations = { 'Basic Auth': { 'type': 'apiKey', 'in': 'header', 'name': 'Authorization' }, }

api = Api(blueprint,
          title='API ARCANE',
          version='1.0',
          description='a RestFul API using Flask',
          security='Basic Auth',
          authorizations=authorizations 
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(property_ns, path='/property')