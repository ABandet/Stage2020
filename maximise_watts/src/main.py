from utils import *


LOGS_PATH = "./data/out.log"

NB_NAME = "NB"
NT_NAME = "NT"
TIME_NAME = "TIME"
POWER_NAMES = [ "POWER_CPU1", "POWER_CPU2", "POWER_RAM1", "POWER_RAM2", "POWER_GPU"]

def get_rows(path=LOGS_PATH):
    return get_cvs_rows(path)

def get_data(rows, col_name):
    col_index = get_col_index(rows, col_name)
    data = get_col_data(rows, col_index)
    return data

def get_size(rows):
    nb_list = get_data(rows, NB_NAME)
    nt_list = get_data(rows, NT_NAME)
    return (nb_list, nt_list)

def get_time(rows):
    time = get_data(rows, TIME_NAME)
    return time

def get_power(rows):
    powers = []
    for name in POWER_NAMES:
        powers.append(convert_to_float(get_data(rows, name)))
    for i in range (1, len(powers)):
        powers[0] = add_two_list(powers[0], powers[i])
    return powers[0]

def find_max_index(data_liste):
    max_index = 0
    max_value = data_liste[0]
    for i in range(len(data_liste)):
        if data_liste[i] > max_value:
            max_value = data_liste[i]
            max_index = i
    
    return max_index


if __name__=="__main__":
    rows = get_rows()
    nb_list, nt_list = get_size(rows)
    time = get_time(rows)
    time = convert_to_float(time)
    power = get_power(rows)
    max_time_idx = find_max_index(time)
    print("Maximise time with nb={}, nt={}. Total time : {} seconde".format(nb_list[max_time_idx], nt_list[max_time_idx], time[max_time_idx]))
    print("Total energy was {} joules (Average {} W)\n".format(power[max_time_idx], power[max_time_idx]/time[max_time_idx]))

    average_power = div_two_list(power, time)
    max_power_idx = find_max_index(average_power)
    print("Maximise power with nb={}, nt={}. Total time : {} seconde".format(nb_list[max_power_idx], nt_list[max_power_idx], time[max_power_idx]))
    print("Total energy was {} joules (Average {} W)".format(power[max_time_idx], power[max_power_idx]/time[max_power_idx]))

