"""
This file serves as the point of entry for of the webserver logic.
"""

from flask import Flask, Blueprint
from flask_cors import CORS, cross_origin
from flask_restplus import Api

from .main.controller.paper_controller import api as paper_ns
from .main.controller.family_controller import api as family_ns
from .main.controller.reference_controller import api as reference_ns
from .main.controller.author_controller import api as author_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Research Paper Graph',
          version='1.0',
          description='Research Paper Graph'
          )

api.add_namespace(paper_ns, path='/paper')
api.add_namespace(reference_ns, path='/reference')
api.add_namespace(author_ns, path='/author')
api.add_namespace(family_ns, path='/family')

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
