from datetime import datetime
from flask import Flask, render_template, json

LAP_TIME = []
NAME = []
CAR = []
REPORT = []
CODE = []

app = Flask(__name__)

def get_data_from_file(filename):
    with open(filename) as f:
        f = sorted(f)
    return f


def get_time(f):
    buff_time = []
    for line in f:
        time = line[3:].split("_")
        time[-1] = time[-1].strip()
        buff_time.append(time[1])
    return buff_time


def build_report():
    # Working with start time
    f = get_data_from_file(r'..\datafiles\start.log')
    start_time = get_time(f)

    # Working with end time
    f = get_data_from_file(r'..\datafiles\end.log')
    end_time = get_time(f)

    zip_object = zip(start_time, end_time)

    # Getting  lap time
    for start_t, end_t in zip_object:
        format = '%H:%M:%S.%f'
        startDateTime = datetime.strptime(start_t, format)
        endDateTime = datetime.strptime(end_t, format)
        diff = endDateTime - startDateTime
        LAP_TIME.append(str(diff))

    # building report
    f = get_data_from_file(r'..\datafiles\abbreviations.txt')
    for line in f:
        line = line.split('_')
        line[-1] = line[-1].strip()
        NAME.append(line[1])
        CAR.append(line[2])

    result = list(zip(NAME, CAR, LAP_TIME))
    res = sorted(result, key=lambda x: x[2])
    report = [(x, y, t) for x, y, t in res if len(t) < 18]
    return report

def drivers_info():
    f = get_data_from_file(r'..\datafiles\abbreviations.txt')
    for line in f:
        line = line.split('_')
        line[-1] = line[-1].strip()
        CODE.append(line[0])
        NAME.append(line[1])
        CAR.append(line[2])

    result = list(zip(CODE, NAME, CAR))
    return result



def print_report(report):
    for n, c, t in report:
        print(' | '.join([n, c, t]))
        result = ' | '.join([n, c, t])
        REPORT.append(result)
    return REPORT



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/report')
def racing_report():
    data = print_report(build_report())
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/report/drivers')
def driver():
    result = drivers_info()
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/report/drivers/<string:driver_id>')
def single_driver_info(driver_id):
    all_drivers = drivers_info()
    for test_driver in all_drivers:
        if driver_id == test_driver[0]:
            res = test_driver
            break
        pass

    response = app.response_class(
        response=json.dumps(res),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=True)
