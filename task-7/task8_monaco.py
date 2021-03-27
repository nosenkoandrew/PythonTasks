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



def get_data_from_file(filename):
    with open(filename) as file:
        file = sorted(file)
    return file


def get_time(f):
    buff_time = []
    for line in f:
        time = line[3:].split("_")
        time[-1] = time[-1].strip()
        buff_time.append(time[1])
    return buff_time


def build_report():
    # Working with start time
    file = get_data_from_file(DATA_FILES / 'start.log')
    start_time = get_time(file)

    # Working with end time
    file = get_data_from_file(DATA_FILES / 'end.log')
    end_time = get_time(file)

    zip_object = zip(start_time, end_time)

    # Getting  lap time
    for start_t, end_t in zip_object:
        format = '%H:%M:%S.%f'
        startDateTime = datetime.strptime(start_t, format)
        endDateTime = datetime.strptime(end_t, format)
        diff = endDateTime - startDateTime
        LAP_TIME.append(str(diff))

    # building report
    file = get_data_from_file(DATA_FILES / 'abbreviations.txt')
    for line in file:
        line = line.split('_')
        line[-1] = line[-1].strip()
        NAME.append(line[1])
        CAR.append(line[2])

    result = list(zip(NAME, CAR, LAP_TIME))
    result = sorted(result, key=lambda x: x[2])
    report = [(x, y, t) for x, y, t in result if len(t) < 18]
    return report


def drivers_info():
    f = get_data_from_file(DATA_FILES / 'abbreviations.txt')
    for line in f:
        line = line.split('_')
        line[-1] = line[-1].strip()
        code.append(line[0])
        NAME.append(line[1])
        CAR.append(line[2])

    result = list(zip(code, NAME, CAR))
    return result


def print_report(report):
    for n, c, t in report:
        print(' | '.join([n, c, t]))
        result = ' | '.join([n, c, t])
        REPORT.append(result)
    return REPORT


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/report')
def racing_report():
    data = print_report(build_report())
    return jsonify(data)


@app.route('/report/drivers', methods=['GET'])
def driver():
    result = drivers_info()
    return jsonify(result)


@app.route('/report/drivers/<string:driver_id>', methods=['GET', 'PUT'])
def single_driver_info(driver_id):
    all_drivers = drivers_info()
    item = next((exact_driver for exact_driver in all_drivers if driver_id == exact_driver[0]), None)
    if not item:
        return {'message': 'No driver with this code'}, 400
    return jsonify(item)


if __name__ == '__main__':
    app.run(debug=True)
