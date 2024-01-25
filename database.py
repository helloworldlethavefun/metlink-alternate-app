# This is the file the will handle all the sqlite commands
import sqlite3

def search_for_stop_id(stop):

    stop_ids = []

    con = sqlite3.connect('stops.db')
    cur = con.cursor()

    query = f"SELECT stop_id FROM stops WHERE stop_name LIKE ?;"

    cur.execute(query, ('%' + stop + '%',))

    results = cur.fetchall()

    cur.close()
    con.close()

    if len(results) > 1:
        multiple_results = {}
        for item in results:
            stop_name = search_for_stop_name(item[0])
            multiple_results[item[0]] = stop_name
        return multiple_results  # Return multiple results
    elif len(results) == 1:
        stop_id = results[0][0]
        return int(stop_id)
    else:
        return None


def search_for_stop_name(stop_id):

    con = sqlite3.connect('stops.db')
    cur = con.cursor()

    query = f"SELECT stop_name FROM stops WHERE stop_id LIKE ?;"

    stop_id = str(stop_id)
    
    cur.execute(query, ('%' + stop_id + '%',))

    results = cur.fetchall()

    print(results)

    cur.close()
    con.close()

    if len(results) == 1:
        stop_name = results[0][0]
        print(stop_name)
        return str(stop_name)
    else:
        return "Sorry there were no results found"
