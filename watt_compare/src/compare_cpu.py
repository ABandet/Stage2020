import matplotlib.pyplot as plt
from nvidia_power import get_data as nvidia_get_data
from likwid_power import get_likwid_data as cpu_get_data
from utils import get_total_power
from wattmeter_power import *


if __name__=="__main__":
    c_time, c_power = cpu_get_data()

    try:
        watt = getwatt("gemini-2", c_time[0], c_time[-1])
        w_time, w_power = extract_data(watt)
        plt.plot(w_time, w_power, "C2", label="wattmeter measure", color="red")
    except Exception as e:
        print("Could not get wattmeter data: {}".format(e))

    plt.xlabel("timestamp (s)")
    plt.ylabel("Power (W)")
    plt.plot(c_time, c_power, "C1", label="likwid measure", color="blue")
    plt.legend()
    plt.savefig("img/power.pdf")
