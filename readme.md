# The Phat Controller
The fully customizable metlink timetable

## What is The Phat Controller?
The Phat Controller is a flask web app that allows you to create a flexable dashboard/timetable screen. The idea is you add any bus/train stops you visit frequently maybe any bus or train timetables to the main page and boom! You don't have to spend ages trying to search for the one bus stop when you can open The Phat Controller and know exactly when that next bus arrives or when that train is about to leave

## Ok I wanna use this, How do I set it up?
First off you need to download this git repo. Next up you need to get an api key from metlink opendata api. To do this first go to https://opendata.metlink.org.nz, and create an account. Next up go to My Dashboard in the top left corner. On this screen you should see 2 sections. The first is your api key. The other is your usage of this api key. For now we only want to worry about the api key so copy that. Then open up your terminal where the folder that contains this file in. Then create an environment variable called OPENDATA_API_KEY that has your api key as the contents. Install requirements from the txt file by doing `pip install -r requirements.txt`. Then run main.py and go to the IP address of whatever is running the server and boom!
