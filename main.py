# main.py file for the Phat Controller

# import the required modules
import os
import requests
import json
from flask import Flask, render_template, redirect, url_for, request
from dateutil import parser
import sqlite3
from database import *

# set some variables that will make it easier to query the api using requests as well as to keep track o stuff
BaseURL = 'https://api.opendata.metlink.org.nz/v1'
StopPredictions = BaseURL + '/stop-predictions'
stops = {}
Api_key = os.environ["OPENDATA_API_KEY"]
app = Flask(__name__)
app.secret_key = 'ASuperSecretKey'
colour = "white"
data = {}
num_of_stops = 0

# Just checks if the json file is empty or exists. 
def is_json_file_empty(file):
    return os.path.exists(file) and os.stat(file).st_size == 0

# Write all of the stops to be monitored to a file
def write_list_to_file():
    with open('monitored_stops.json', 'w') as file:
        json.dump(stops, file)
        file.close()

# This is a function to grap the stops that will be monitored from the json file
def pull_list_from_file():
    global stops
    global stop_n
    with open('monitored_stops.json', 'r') as file:
        stops = json.load(file)
        file.close()

# Query the opendata api and pulls down the predictions of the arrival of the bus
def get_stop_predictions(stop_id):
    payload = {'stop_id': stop_id}
    headers = {'accept': 'application/json', 'x-api-key': Api_key}
    url = StopPredictions
    r = requests.get(url, params=payload, headers=headers)
    datass = r.json()
    if type(stop_id) == 'string':
        try:
            expected_time = datass['departures'][0]['arrival']
        except:
            expected_time = 'Sorry there was an error fetching the time'
        destination = datass['departures'][0]['destination']['name']
        return expected_time, destination
    else:
        try:
            expected_time = datass['departures'][0]['departure']['aimed']
        except:
            expected_time = 'Sorry there was an error fetching the time'
        destination = datass['departures'][0]['destination']['name']
    return expected_time, destination

# This is the main page. It takes the stops you wish to monitor and then find the times 
# and display them
@app.route("/")
def index():
    try:
        pull_list_from_file()
    except:
        print(stops)
        return "Looks like there is no stops to look at, maybe add some? <a href='/manage-stops'>Here</a>"
    times = {}
    print(stops)
    for value in stops.items():
        stop_id = value[1]
        stop_name = search_for_stop_name(stop_id)
        time, target = get_stop_predictions(value)
        parsed_time = parser.parse(time)
        time = parsed_time.strftime("%H:%M:%S")
        times[stop_name + " Service to " + target] = time
    return render_template('index.html', times=times, colour=colour)

# This is the page where users can add/remove stops from the list
@app.route("/manage-stops", methods=['GET', 'POST'])
def managing_stops():
    global colour
    global num_of_stops
    global stops

    if request.method == 'POST':
        chosen_stop = request.form.get('chosen_stop')
        stop = request.form.get('stops')
        colour = request.form.get('colour')

        if chosen_stop:
            # If a stop is chosen from the selection screen
            num_of_stops += 1
            stops[num_of_stops] = chosen_stop
            write_list_to_file()
            return redirect(url_for('index'))
      
        elif stop:
            # If a stop is directly entered without choosing from the selection screen
            stop_results = search_for_stop_id(stop)
            print(stop_results)
            if stop_results:
                if isinstance(stop_results, int):
                    # Only one result (integer), proceed with it
                    stop_id = stop_results
                    num_of_stops += 1
                    stops[num_of_stops] = stop_id
                    write_list_to_file()
                    return redirect(url_for('index'))
                elif len(stop_results) == 1:
                    # Only one result (list with a 4-letter string code), proceed with it
                    stop_id = stop_results[0][0]
                    num_of_stops += 1
                    stops[num_of_stops] = stop_id
                    write_list_to_file()
                    return redirect(url_for('index'))
                else:
                    return render_template('choose_stop.html', stop_results=stop_results)
            else:
                return "Sorry, there were no results found"
    return render_template('add_stops.html')


# When the program is ran, import all of the information of the stops and start flask
if __name__ == "__main__":
    app.run(port=8008, host='0.0.0.0')
