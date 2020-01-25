"""
This file serves as the point of entry for of the webserver logic.
"""

from flask import Flask, Blueprint
from flask_restplus import Api

from .main.controller.paper_controller import api as paper_ns
from .main.controller.family_controller import api as family_ns
from .main.controller.reference_controller import api as reference_ns
from .main.controller.author_controller import api as author_ns
from .main.controller.write_controller import api as write_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Research Paper Graph',
          version='1.0',
          description='Research Paper Graph'
          )

api.add_namespace(paper_ns, path='/paper')
api.add_namespace(reference_ns, path='/reference')
api.add_namespace(author_ns, path='/author')
api.add_namespace(write_ns, path='/write')
api.add_namespace(family_ns, path='/family')

