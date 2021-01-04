import json
from flask import Flask, Response, abort
from flask_restful import Resource, Api, request
from task.static import utilities
from json2xml import json2xml
from flasgger import Swagger, swag_from

app = Flask(__name__)


swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/swagger.yaml',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/swagger/"
}

swagger = Swagger(app, config=swagger_config)
api = Api(app, prefix='/api/v1')


class Drivers(Resource):
    def response(self, data, response_format):
        if response_format == 'xml':
            data = json2xml.Json2xml(data).to_xml()
            return Response(data, status=200, mimetype='application/xml')
        data = json.dumps(data, indent=4)
        return Response(data, status=200, mimetype='application/json')

    @swag_from('/static/swagger.yaml')
    def get(self, driver_id=None):
        response_format = request.args.get('format', 'json')
        if driver_id:
            result = utilities.one_driver_info(driver_id)
            if not result:
                print('No driver with such id')
                return abort(404)
        else:
            result = utilities.all_drivers()
        return self.response(result, response_format)


api.add_resource(Drivers, '/drivers', endpoint='drivers')
api.add_resource(Drivers, '/drivers/<driver_id>', endpoint='driver')

if __name__ == '__main__':
    app.run(debug=True)
