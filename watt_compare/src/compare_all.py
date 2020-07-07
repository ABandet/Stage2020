import matplotlib.pyplot as plt
from nvidia_power import get_data as nvidia_get_data
from likwid_power import get_likwid_data as cpu_get_data
from utils import get_total_power
from wattmeter_power import *

if __name__ == "__main__":
    n_time, n_power = nvidia_get_data()
    c_time, c_power = cpu_get_data()

    plt.xlabel("timestamp (s)")
    plt.ylabel("Power (W)")
    plt.plot(n_time, n_power, "C1", label="nvidia power", color="green")
    plt.plot(c_time, c_power, "C2", label="cpu power", color="orange")

    # get total
    total = get_total_power(c_power, n_power)
    plt.plot(n_time[:len(total)], total, "C3", label="software measure", color="red")

    try:
        watt = getwatt("gemini-2", n_time[0], n_time[-1])
        w_time, w_power = extract_data(watt)
        plt.plot(w_time, w_power, "C4", label="wattmeter measure", color="blue")
    except Exception as e:
        print("Could not get wattmeter data.")
    

    plt.legend()
    plt.savefig("img/nvidia_power.pdf")
