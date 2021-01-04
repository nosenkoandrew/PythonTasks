from datetime import datetime
from flask import Flask, render_template, jsonify
from pathlib import Path
from flask_restful import Resource, Api
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_restful_swagger import swagger

LAP_TIME = []
NAME = []
CAR = []
REPORT = []
code = []
ROOT_PATH = Path.cwd()
DATA_FILES = ROOT_PATH / '../datafiles'

app = Flask(__name__)
api = Api(app)
api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url="/v1")


class Monaco_Racing(Resource):
    def get_data_from_time(self, filename):
        with open(filename) as file:
            file = sorted(file)
        return file

    def get_time(self, f):
        buff_time = []
        for line in f:
            time = line[3:].split("_")
            time[-1] = time[-1].strip()
            buff_time.append(time[1])
        return buff_time

    def build_report(self):
        file = self.get_data_from_file(DATA_FILES / 'start.log')
        start_time = self.get_time(file)
        file = self.get_data_from_file(DATA_FILES / 'end.log')
        end_time = self.get_time(file)
        zip_object = zip(start_time, end_time)
        for start_t, end_t in zip_object:
            format = '%H:%M:%S.%f'
            startDateTime = datetime.strptime(start_t, format)
            endDateTime = datetime.strptime(end_t, format)
            diff = endDateTime - startDateTime
            LAP_TIME.append(str(diff))
        file = self.get_data_from_file(DATA_FILES / 'abbreviations.txt')
        for line in file:
            line = line.split('_')
            line[-1] = line[-1].strip()
            NAME.append(line[1])
            CAR.append(line[2])
        result = list(zip(NAME, CAR, LAP_TIME))
        result = sorted(result, key=lambda x: x[2])
        report = [(x, y, t) for x, y, t in result if len(t) < 18]
        return report

    def drivers_info(self):
        f = self.get_data_from_file(DATA_FILES / 'abbreviations.txt')
        for line in f:
            line = line.split('_')
            line[-1] = line[-1].strip()
            code.append(line[0])
            NAME.append(line[1])
            CAR.append(line[2])

        result = list(zip(code, NAME, CAR))
        return result

    def print_report(self, report):
        for n, c, t in report:
            print(' | '.join([n, c, t]))
            result = ' | '.join([n, c, t])
            REPORT.append(result)
        return REPORT

    @app.route('/', methods=['GET'])
    @app.route('/home', methods=['GET'])
    def home(self):
        return render_template('home.html')

    @app.route('/report')
    def racing_report(self):
        data = self.print_report(self.build_report())
        return jsonify(data)

    @app.route('/report/drivers', methods=['GET'])
    def driver(self):
        result = self.drivers_info()
        return jsonify(result)

    @app.route('/report/drivers/<string:driver_id>', methods=['GET', 'PUT'])
    def get_single_driver_info(self, driver_id):
        all_drivers = self.drivers_info()
        item = next((exact_driver for exact_driver in all_drivers if driver_id == exact_driver[0]), None)
        if not item:
            return {'message': 'No driver with this code'}, 400
        return jsonify(item)


api.add_resource(Monaco_Racing, '/api')
if __name__ == '__main__':
    app.run(debug=True)
