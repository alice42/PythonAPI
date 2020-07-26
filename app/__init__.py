# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='API ARCANE',
          version='1.0',
          description='a RestFul API using Flask'
          )

api.add_namespace(user_ns, path='/user')