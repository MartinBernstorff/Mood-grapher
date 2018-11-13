import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import json
from pprint import pprint
from numbers import Number
import datetime as dt

DIR = "/Users/martin/Dropbox/Apps/Reporter-App"

dates = []
values = []

def combine_json(dir):
    """
    Input: Directory with .json Reporter files
    Output: List of contents of .json files
    """
    json_list = []

    for file in sorted(os.listdir(DIR)):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            with open(dir + "/" + file) as train_file:
                json_list.append(json.load(train_file))

    return json_list

def get_mood_snaps(list):
    """
    Input: List of Reporter jsons elements
    Output: List of date, val tuples
    """
    mood_snaps = []

    for json_element in list:
        for snapshot in json_element["snapshots"]:
            #pprint(item, width=3)
            try:
                if snapshot["responses"][0]["questionPrompt"] == "How are you feeling? (Affect)":
                    date = snapshot["date"]
                    mood_val = snapshot["responses"][0]["answeredOptions"][0][1]
                    print(mood_val)
                    if is_number(mood_val):
                        dates.append(date)
                        values.append(mood_val)

            except KeyError:
                print("Element doesn't have selected prompt, skipping")


    return mood_snaps

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def moving_avg(l, N):
    """
    Inputs:
        l: List of floats
        N: Width of window
    Outputs:
        List of running averages with window-width N
    """
    cumsum, moving_aves = [0], []

    for i, x in enumerate(l, 1):
        i = int(i)
        x = int(x)
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)
    return moving_aves

def conv_to_datetime(l):
    new_l = []
    for d in l:
        new_l.append(dt.datetime.strptime(d, '%Y-%m-%dT%H:%M:%S%z'))

    return new_l

json_list = combine_json(DIR)

get_mood_snaps(json_list)

window_width = 3

values_running_avg = moving_avg(values, window_width)
dates_running_avg = dates[window_width-1:]

dates_datetime = conv_to_datetime(dates_running_avg)

def plot_datetime(x, y):
    """
    Inputs:
        x: List of datetime objects
        y: values

    Outputs:
        graph
    """
    window_width = 3

    #plt.plot(dates, values)
    plt.plot_date(mdates.date2num(x), y, linestyle = "-", markersize = "0.1")

    plt.ylabel("Mood")
    plt.ylim(0, 10)

    plt.xticks(fontsize="x-small", rotation=30)
    plt.xlabel("Time")
    plt.subplots_adjust(bottom=0.2)

plot_datetime(dates_datetime, values_running_avg)

plt.show()

#pprint(dates_running_avg)
