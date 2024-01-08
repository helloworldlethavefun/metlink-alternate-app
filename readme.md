# Note if you find this it's a massive work in progress at this point in time!
# Alternative Metlink Application

This is a side project I am working because I hate the metlink ui for both the app and the site.
It uses the Metlink OpenData API to periodcally obtain predictions for which ever stops you add to monitor

## Setup instructions

For those who don't know what they are doing:
(If you know skip to the next section)
```
Firstly you will need to obtain an api key for the opendata api. To do this head over to https://opendata.metlink.org.nz/ 
and register an account. Then in the top right corner click on My Dashboard. On this screen there should be 2 sections: One called API Key and another called Usage for Metlink Open Data API. Under API Key should be a string of alphanumeric characters. Copy this then head back over to your terminal. Now that we have our API key we need to put it into an environment variable. For this type in export METLINK_API_KEY="<paste your api key here>". Then run the program. On your first run it should ask you if you would like to add any stops to monitor. Type in the name of the stop (copy and paste from the metlink site) and after setup is finished you should now have stop predictions.
```

For those who know:
```
Create an api key from the Metlink OpenData site and set an environment variable called METLINK_API_KEY then run the program.
```
