from datetime import datetime
from flask import render_template
from pathlib import Path

LAP_TIME = []
NAME = []
CAR = []
REPORT = []
code = []
ROOT_PATH = Path.cwd()
DATA_FILES = ROOT_PATH / '../datafiles'


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


def home():
    return render_template('home.html')


def racing_report():
    data = print_report(build_report())
    return data


def all_drivers():
    result = drivers_info()
    return result


def one_driver_info(driver_id):
    all_drivers = drivers_info()
    res = None
    for test_driver in all_drivers:
        if driver_id == test_driver[0]:
            res = test_driver
            break
        pass
    return res

