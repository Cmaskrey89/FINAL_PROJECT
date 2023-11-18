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

Fetches weather and tide data by calling on the Stormglass API (freely available for non-commercial purposes). Weather and tide data are sourced from two different URLs requiring 2 API calls everytime the script is run.

Data is processed and combined into a single csv where both tide and weather data are appended together. A csv was used because I can only call on the API x5 per day with the free version, so I thought I'd better save this data instead of having to call on the API everytime I needed the data. 

**Challenges:** Well, a lot. I feel Ive dealt very weirdly with timezone conversions and I wanted to implement more fixes but it would just keep breaking the implementation. I used timedata but perhaps I should have used the arrow library as suggested by the StormGlass documentation. Also joining the data gathered from two function (tide and weather) wasn't straight forward.

### rating_parameters.py

This script then reads the hourly_forecast.csv file and scores the different sea and tide data that was fetched and categorises them in order to make it easier for me to use my arbitrary knowledge later in the surf_rating. There is a single function read_hourly_forecast that outputs the scores (numerical) and states (string descriptors for each score) and saves it into variable dictionary 'data'.

**Challenges:** The implementation of the scoring system was very very very time consuming. At the end I used both scores and states to try to give me options later but its certainly redundant. I also feel like I could have perhaps abstracted to reduce significantly the length of the code! Also, I didn't implement a main() function here, which is perhaps the correct way of doing so for later use of the script in other apps.

### surf_rating.py

Finally, this script uses the {states['']} from the rating_parameters (states instead of scores because then I can judge them better as strings!) to combine my knowledge with the conditions. 

**Challenges:** This was the easiest bit, I just had to implement my scoring system. I ultimately usedthe states and not the code as it made it so much easier to visualise and basically shows the numerical scored were ultimately not important. You live and learn! Also I couldnt decide if this module should have been simply included with rating_parameters.py as its not hugely different. I just thought another layer of abstraction would be good.

## Front-end

### app.py

Flask implementation that runs the backend **logic** and hosts/displays all results in a snigle page: index.html. Here the UTC ISO times that were used in the back-end scripts are changed to a more readable hh:mm format and filtered out to only display daylight times. If this was to be hosted and implemented as a functioning webapp, I'd also need to put a daily trigger to execute the back-end logic once a day (a single API call a day to make sure we have enough API Calls left for any debugging 4 out of 5 available per day).

### index.html

A simple static website without buttons or forms that simply displays the results for the day in a table. Continued development could include some CSS, javascript animations, etc. 

