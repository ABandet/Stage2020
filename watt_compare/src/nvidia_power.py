import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from utils import *


CSV_FILE = "data/nvidia.csv"
PLOT_FILE = "img/power.pdf"

TIME_COL = "timestamp"
POWER_COL = " power.draw [W]"

power_list = []
time_list = []


def clean_power(power):
    for i in range(len(power)):
        str_power = power[i]
        str_power = str_power.split(' ')
        power[i] = float(str_power[1])
    return power

def clean_time(time):
    for i in range(len(time)):
        str_time = time[i]
        time_obj = datetime.strptime(str_time, "%Y/%m/%d %H:%M:%S.%f")
        time[i] = time_obj.timestamp()
    return time

def get_power_index(rows):
    try :
        return get_col_index(rows, POWER_COL)
    except Exception as e:
        print("Error occured in nvidia's get_power_index : {}".format(e))
        exit(-1)

def get_time_index(rows):
    try :
        return get_col_index(rows, TIME_COL)
    except Exception as e:
        print("Error occured in nvidia's get_time_index : {}".format(e))
        exit(-1)

def get_power(rows):
    power_index = get_power_index(rows)
    power = get_col_data(rows, power_index)
    power = clean_power(power)
    return power

def get_time(rows):
    time_index = get_time_index(rows)
    time = get_col_data(rows, time_index)
    time = clean_time(time)
    return time

def get_data():
    try :
        rows = get_cvs_rows(CSV_FILE)
        power = get_power(rows)
        time = get_time(rows)
        if (True): # for gemini, to adapt
            clean_time = []
            clean_power = []
            for i in range(0, len(power), 8):
                clean_time.append(time[i])
                sum = 0
                for j in range(i, i+8):
                    try:
                        sum += power[j]
                    except Exception as e:
                        sum+=0
                clean_power.append(sum)
            return clean_time, clean_power
        return time, power

    except Exception as e:
        print("Error occured in nvidia's get_data : {}".format(e))
        exit(-1)

def plot_data(x, y):
    plt.xlabel("timestamp (s)")
    plt.ylabel("Power (W)")
    plt.plot(time_list, power_list)
    plt.savefig(PLOT_FILE)


if __name__=="__main__":
    time, power = get_data()
    plt.xlabel("timestamp (s)")
    plt.ylabel("Power (W)")
    plt.plot(time, power)
    plt.savefig(PLOT_FILE)
