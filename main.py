# This is the main file for my alternative metlink application

# import the required modules
import os
import requests
import json
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from dateutil import parser

# set some variables that will make it easier to query the api using requests as well as to keep track o stuff
BaseURL = 'https://api.opendata.metlink.org.nz/v1'
StopPredictions = BaseURL + '/stop-predictions'
stops = {}
Api_key = os.environ["OPENDATA_API_KEY"]
stop_n = 0
app = Flask(__name__)
app.secret_key = 'ASuperSecretKey'
stop_names_n = 0

class AddStopsForm(FlaskForm):
    stop = StringField('stop_name', validators=[DataRequired()])



# load in all the stops information
def load_json_data():
    global data
    with open('stops.json') as file:
        data = json.loads(file.read())
        file.close



def is_json_file_empty(file):
    return os.path.exists(file) and os.stat(file).st_size == 0



# ask the user for the name of the stop they wish to obtain the id of then add to the stops list
def get_stop_id(stop_name):
    global stop_n
    for dictionary in data:
        if stop_name in dictionary.values():
            print(dictionary.values())
            stop_id = dictionary["stop_id"]
            stop_n = int(stop_n)
            stop_n = stop_n + 1
            stops[stop_n] = stop_id

# Vice-versa of the function above. Take the stop id and find the name of the stop
def get_stop_name(stop_id):
    for dictionary in data:
        if stop_id in dictionary.values():
            stop_name = dictionary["stop_name"]
            return stop_name

# Write all of the stops to be monitored to a file
def write_list_to_file():
    with open('monitored_stops.json', 'w') as file:
        json.dump(stops, file)
        file.close()
    with open('stopn.txt', 'w') as file:
        file.write(str(stop_n))
        file.close()
    with open('stopnn.txt', 'w') as file:
        file.write(str(stop_names_n))
        file.close()
        


# This is a function to grap the stops that will be monitored from the json file
def pull_list_from_file():
    global stops
    global stop_n
    with open('monitored_stops.json', 'r') as file:
        stops = json.load(file)
        file.close()
    with open('stopn.txt') as file:
        stop_n = file.read()
        file.close


def get_stop_predictions(stop_id):
    payload = {'stop_id': stop_id}
    headers = {'accept': 'application/json', 'x-api-key': Api_key}
    url = StopPredictions
    r = requests.get(url, params=payload, headers=headers)
    datass = r.json()
    expected_time = datass['departures'][0]['arrival']
    return expected_time


@app.route("/")
def index():
    try:
        pull_list_from_file()
    except:
        return "Looks like there is no stops to look at, maybe add some? <a href='/add-stops'>Here</a>"
    times = {}
    for value in stops.items():
        stop_namee = value[1]
        stop_nn = get_stop_name(stop_namee)
        time = get_stop_predictions(value)
        time = time['aimed']
        parsed_time = parser.parse(time)
        time = parsed_time.strftime("%H:%M:%S")
        print(time)
        times[stop_nn] = time
        print(times)
    return render_template('index.html', times=times)



@app.route("/add-stops", methods=['GET', 'POST'])
def managing_stops():
    form = AddStopsForm()
    if form.validate_on_submit():
        data = form.stop.data
        stop_ids = get_stop_id(data)
        print(stop_ids)
        write_list_to_file()
        print(stops)
    return render_template('add_stops.html', form=form)

@app.route("/stops")
def listing_stops():
        stop_names = {}
        try:
            pull_list_from_file()
            print(stops)
            stop_names_n = 0
        except:
            return "Looks like you don't have any stops here. Want to add them? Go <a href='/add-stops'>here</a>"
        for item in stops.values():
            stop_name = get_stop_name(item)
            stop_names_n += 1
            stop_names[stop_names_n] = stop_name
            print(stop_names)
        return render_template('list_stops.html', stops=stop_names)



if __name__ == "__main__":
    load_json_data()
    app.run(port=8008, host='0.0.0.0', debug=True)
