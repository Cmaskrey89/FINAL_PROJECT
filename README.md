# Surf Forecast for "La Reventazon de Makaha"
#### Video Demo: <https://www.youtube.com/watch?v=14ejeQOTPcY>
#### Description: 

# General description
For the final project I built a webapp using flask that uses a freely-available API (Stormglass) of sea and weather conditions to evaluate the surf conditions of my local break in Lima, Peru ("La Reventazon de Makaha") based on my experience of suring it. The inspiration came from the lacklustre rating performance of generalised surf forecast websites like surf-forecast.com and surfline.com, who provide accurate surf conditions but a largely inaccurate evaluation of conditions for a final surf rating. 

I just want to know that I would have not been able to do the course without the support of my employer www.aquaswitch.co.uk, the UK-based utilities comparison website who pay my wages !!

# Architechture

## Logic

There are three main components to the backend logic of my webapp.

### data_fetcher.py

Fetches weather and tide data by calling on the Stormglass API (freely available for non-commercial purposes). Data is processed and combined into a single csv where both tide and weather data are appended together. A csv was used because I can only call on the API x10 per day with the free version, so I thought I'd better save this data instead of having to call it all the time!

### rating_parameters.py

This script then reads the hourly_forecast.csv file and scores the different sea and tide data that was fetched and categorises them in order to make it easier for me to use my arbitrary knowledge later in the surf_rating. There is a single function read_hourly_forecast that outputs the scores (numerical) and states (string descriptors for each score) and saves it into variable dictionary 'data'.

### surf_rating.py

Finally, this script uses the {states['']} from the rating_parameters (states instead of scores because then I can judge them better as strings!) to combine my knowledge with the conditions. 

## Front-end

### app.py

Flask implementation that runs the backend **logic** and hosts/displays all results in a snigle page: index.html. Here the UTC ISO times that were used in the back-end scripts are changed to a more readable hh:mm format and filtered out to only display daylight times. If this was to be hosted and implemented as a functioning webapp, I'd also need to put a daily trigger to execute the back-end logic once a day (a single API call a day to make sure we have enough API Calls left for any debugging 9 out of 10 available per day).

### index.html

A simple static website without buttons or forms that simply displays the results for the day in a table. Continued development could include some CSS, javascript animations, etc. 

