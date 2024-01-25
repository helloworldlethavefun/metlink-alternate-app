import json
import sqlite3

con = sqlite3.connect('stops.db')
cur = con.cursor()
selected_data = []

def create_table():
    cur.execute("CREATE TABLE stops(id, stop_id, stop_name, stop_desc)")

def add_stop(stops):
    for stop in stops:
        cur.execute("INSERT INTO stops VALUES(?, ?, ?, ?)", (stop['id'], stop['stop_id'], stop['stop_name'], stop['stop_desc']))
    con.commit()

with open('stops.json', 'r') as file:
    data = json.loads(file.read())
    file.close()

for index, item in enumerate(data):
    stop = {}
    for key, value in item.items():
        if key in ["id", "stop_id", "stop_name", "stop_desc"]:
            stop[key] = value
    selected_data.append(stop)


add_stop(selected_data)
