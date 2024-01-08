# This is the main file for my alternative metlink application

# import the required modules
import os
import requests
import json
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

# set some variables that will make it easier to query the api using requests as well as to keep track o stuff
BaseURL = 'https://api.opendata.metlink.org.nz/v1'
StopPredictions = BaseURL + '/stop-predictions'
stops = {}
Api_key = os.environ["OPENDATA_API_KEY"]
stop_n = 0
app = Flask(__name__)
app.secret_key = 'ASuperSecretKey'


class AddStopsForm(FlaskForm):
    stop = StringField('stop', validators=[DataRequired()])



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



# Write all of the stops to be monitored to a file
def write_list_to_file():
    with open('monitored_stops.json', 'w') as file:
        print(stops)
        json.dump(stops, file)
        file.close()
    with open('stopn.txt', 'w') as file:
        file.write(str(stop_n))
        print(stop_n)
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



@app.route("/")
def index():
    return render_template('index.html')



@app.route("/add_stops", methods=['GET', 'POST'])
def managing_stops():
    if is_json_file_empty('monitored_stops.json'):
        form = AddStopsForm()
        print('test')
        if form.validate_on_submit():
            data = form.stop.data
            get_stop_id(data)
            print(stops)
        return render_template('list_stops.html', form=form)
    else:
        pull_list_from_file()
        return render_template('list_stops.html')



if __name__ == "__main__":
    load_json_data()
    app.run(port=8008, host='0.0.0.0', debug=True)
