from flask import Flask, render_template
import data_fetcher
import rating_parameters
import surf_rating
from datetime import datetime

############# FLASK IMPLEMENTATION #############

app = Flask(__name__)

@app.route('/')
def index():

############# FETCHES THE DATA USING data_fetcher ###############

    data_fetcher.main()

############# READS CSV AND CALCULATES RATING PARAMETERS #############

# Process the data and calculate ratings

    hourly_data = rating_parameters.read_hourly_forecast()
    surf_ratings = []
    for hour in hourly_data:

# Parse the time string and convert to a datetime object, we are trying to make the time nice for display on index.html

        time_obj = datetime.fromisoformat(hour['time'])

# Filter times between 05:00 AM and 07:00 PM since these are the surfable times of a 24 hour day.

############# USES RATING STATES TO CALCULATE SURF_RATING #############

        if 5 <= time_obj.hour <= 19:
            scores, states = rating_parameters.parameter_scores(hour)
            surf_rating_result = surf_rating.calculate_surf_rating(states)

# Format the time as HH:MM from the time object defined earlier from the string.

            formatted_time = time_obj.strftime("%H:%M")

# Appends the results from running surf_rating.py and appends it to the variable surf_ratings we use here.

            surf_ratings.append({'time': formatted_time, 'rating': surf_rating_result, 'states': states})

# Extract the date from the first time entry for the header, we dont want to repeat in the table.

    surf_date = datetime.fromisoformat(hourly_data[0]['time']).strftime("%Y-%m-%d")

# Render the templateeeeeee

    return render_template('index.html', surf_ratings=surf_ratings, surf_date=surf_date)

if __name__ == '__main__':
    app.run(debug=True)
