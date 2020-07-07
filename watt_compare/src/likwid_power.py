from utils import *

CSV_PATH = "data/out"
START_TIME_PATH = "data/start.log"
POWER_COL = [4, 5]
RAM_COL = [6, 7]
TIME_COL = 3


def clean_row(rows):
    rows.pop(0)
    return rows

def convert_to_float(liste):
    for i in range(len(liste)):
        liste[i] = float(liste[i])
    return liste

def shift_time_col(liste):
    f = open(START_TIME_PATH, "r")
    start = float(f.readline())
    for i in range(len(liste)):
        liste[i] = liste[i] + start
    return liste

def get_watt_data():
    # get csv data
    rows = get_cvs_rows(CSV_PATH)
    rows = clean_row(rows)
    # get cpu watt data
    cpu_data = []
    for i in POWER_COL:
        data = get_col_data(rows, i)
        data = convert_to_float(data)
        cpu_data.append(data)
    # get ram watt data
    ram_data = []
    for i in RAM_COL:
        data = get_col_data(rows, i)
        data = convert_to_float(data)
        ram_data.append(data)

    power = []
    for i in range(len(cpu_data[0])):
        power.append(0)
        for j in range(len(cpu_data)):
            power[i] += cpu_data[j][i]
            power[i] += ram_data[j][i]

    return power

def get_time_data():
    # get csv data
    rows = get_cvs_rows(CSV_PATH)
    rows = clean_row(rows)
    # get time data
    time = get_col_data(rows, TIME_COL)
    # shift data with start time
    time = convert_to_float(time)
    time = shift_time_col(time)
    return time

def get_likwid_data():
    time = get_time_data()
    power = get_watt_data()
    return time, power

if __name__=="__main__":
    pass
