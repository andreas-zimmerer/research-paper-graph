"""
This file serves as the point of entry for of the webserver logic.
"""

from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restplus import Api
from flask import Blueprint # pylint: disable=ungrouped-imports

from .main.controller.paper_controller import api as paper_ns
from .main.controller.reference_controller import api as reference_ns
from .main.controller.relative_controller import api as relative_ns

blueprint = Blueprint('api', __name__) # pylint: disable=invalid-name

api = Api(blueprint, # pylint: disable=invalid-name
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(paper_ns, path='/paper')
api.add_namespace(reference_ns, path='/reference')
api.add_namespace(relative_ns, path='/relative')

# pylint: disable=invalid-name
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Import at bottom to prevent circular imports
# pylint: disable=wrong-import-position
