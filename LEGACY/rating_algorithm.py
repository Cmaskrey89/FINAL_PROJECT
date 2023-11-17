import csv


############ Reads the hourly forecast CSV and returns a list of dictionaries containing the table for the algorithm :)

def read_hourly_forecast(filename='Hourly_Forecast.csv'):
    
    data = []
    
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

############# Computes scores for each loaded parameter in the list of dictionaries and returns a new dictionary of scores.

def parameter_scores(hour):
    # Initialize the dictionaries
    scores = {}
    states = {}

    try:
        ########## PRIMARY SWELL HEIGHT SCORES
        
        # Extract the swell height from the hour data
        swell_height = float(hour.get("swellHeight", 0))  # Defaults to 0 if "swellHeight" isn't found
        
        # Determine the score and state based on swell height
        if 0 <= swell_height <= 0.6:
            scores['swell_height'] = 1
            states['swell_height'] = "XS"
        elif 0.6 < swell_height <= 1:
            scores['swell_height'] = 2
            states['swell_height'] = "S"
        elif 1 < swell_height <= 2:
            scores['swell_height'] = 3
            states['swell_height'] = "MS"
        elif swell_height == 2:
            scores['swell_height'] = 4
            states['swell_height'] = "M"
        elif 2 < swell_height <= 3:
            scores['swell_height'] = 5
            states['swell_height'] = "L"
        elif 3 < swell_height:
            scores['swell_height'] = 1
            states['swell_height'] = "XL"
        else:
            scores['swell_height'] = 0
            states['swell_height'] = "Unknown"

        ########## PRIMARY SWELL DIRECTION SCORES
        
        swell_direction = float(hour.get("swellDirection", 0))
        if 220 <= swell_direction <= 320:
            scores['swell_direction'] = 5
            states['swell_direction'] = "Optimal Direction"
        else:
            scores['swell_direction'] = 2
            states['swell_direction'] = "Working Direction"
            
        ########## PRIMARY SWELL PERIOD SCORES
        
        swell_period = float(hour.get("swellPeriod", 0))
        if swell_period < 10:
            scores['swell_period'] = 1
            states['swell_period'] = "Worst"
        elif swell_period < 12:
            scores['swell_period'] = 2
            states['swell_period'] = "Bad"
        elif 12 <= swell_period <= 14:
            scores['swell_period'] = 3
            states['swell_period'] = "Medium"
        elif 14 <= swell_period <= 16:
            scores['swell_period'] = 4
            states['swell_period'] = "Good"
        elif 16 <= swell_period <= 20:
            scores['swell_period'] = 5
            states['swell_period'] = "Epic"
        else:
            scores['swell_period'] = 0
            states['swell_period'] = "Unknown"

        ########## SWELL DISRUPTION SCORES
        
        # Extracting the necessary data from the 'hour' dictionary
        swell_direction = float(hour.get("swellDirection", 0))
        secondary_swell_direction = float(hour.get("secondarySwellDirection", 0))
        swell_period = float(hour.get("swellPeriod", 0))
        secondary_swell_period = float(hour.get("secondarySwellPeriod", 0))
        swell_height = float(hour.get("swellHeight", 0))
        secondary_swell_height = float(hour.get("secondarySwellHeight", 0))

        # Calculating Directional Difference score
        directional_difference = abs(swell_direction - secondary_swell_direction)
        if 0 <= directional_difference <= 20:
            directional_score = 4
        elif 20 < directional_difference <= 40:
            directional_score = 3
        elif 40 < directional_difference <= 90:
            directional_score = 2
        else:
            directional_score = 1

        # Calculating Period Difference score
        period_difference = abs(swell_period - secondary_swell_period)
        if 0 <= period_difference <= 2:
            period_score = 4
        elif 2 < period_difference <= 5:
            period_score = 3
        elif 5 < period_difference <= 10:
            period_score = 2
        else:
            period_score = 1

        # Calculating Size Difference score
        size_difference_percentage = abs((swell_height - secondary_swell_height) / swell_height) * 100
        if 0 <= size_difference_percentage <= 25:
            size_score = 4
        elif 25 < size_difference_percentage <= 50:
            size_score = 3
        elif 50 < size_difference_percentage <= 75:
            size_score = 2
        else:
            size_score = 1

        # Summing up the scores
        total_disruption_score_raw = directional_score + period_score + size_score

        # Normalizing the overall score to be between 1 and 5
        normalized_score = round(1 + (total_disruption_score_raw - 3) * (4/9))

        # Assigning the corresponding state to the score
        if normalized_score == 1:
            disruption_state = "Total Disruption"
        elif normalized_score == 2:
            disruption_state = "Strong Disruption"
        elif normalized_score == 3:
            disruption_state = "Moderate Disruption"
        elif normalized_score == 4:
            disruption_state = "Mild Disruption"
        else:  # normalized_score == 5
            disruption_state = "Minimal Disruption"


        scores['swell_disruption'] = normalized_score
        states['swell_disruption'] = disruption_state

        # Extracting wind speed from the hour data
        wind_speed = float(hour.get("windSpeed", 0))

        ########### WIND SPEED SCORE 

        # Assigning scores and states based on wind speed
        if wind_speed < 7:
            scores["windSpeed"] = 5
            states["windSpeed"] = "Glass"
        elif 7 <= wind_speed < 10:
            scores["windSpeed"] = 4
            states["windSpeed"] = "Light"
        elif 10 <= wind_speed < 12:
            scores["windSpeed"] = 3
            states["windSpeed"] = "Windy"
        else:  # wind_speed >= 12
            scores["windSpeed"] = 1
            states["windSpeed"] = "Blown"

        ########### WIND DIRECTION SCORE

        # Extracting wind direction from the hour data
        wind_direction = float(hour.get("windDirection", 0))

        # Assigning scores and states based on wind direction
        if 170 <= wind_direction <= 280:
            scores["windDirection"] = 1
            states["windDirection"] = "Terrible"
        elif 90 <= wind_direction < 170 or 280 <= wind_direction < 350:
            scores["windDirection"] = 4
            states["windDirection"] = "Cross"
        else:  # 350 <= wind_direction or wind_direction < 90
            scores["windDirection"] = 5
            states["windDirection"] = "Off"
            
        ########### WIND WAVE CHOP SCORE

        # Extracting wind wave height from the hour data
        wind_wave_height = float(hour.get("windWave", 0))

        # Assigning scores and states based on wind wave height
        if wind_wave_height < 0.1:
            scores["windWave"] = 5
            states["windWave"] = "No Chop"
        elif 0.1 <= wind_wave_height < 0.2:
            scores["windWave"] = 4
            states["windWave"] = "Minimal Chop"
        elif 0.2 <= wind_wave_height < 0.3:
            scores["windWave"] = 3
            states["windWave"] = "Noticeable"
        else:  # wind_wave_height >= 0.3
            scores["windWave"] = 1
            states["windWave"] = "Choppy!"

    except ValueError:
        # Handle potential value errors from string to float conversions
        print("Error converting a value to float")

    return scores, states


# Read the hourly forecast data
data = read_hourly_forecast()

# If there's data, process and print each hour's scores and states
if data:
    for idx, hour in enumerate(data):
        scores, states = parameter_scores(hour)
        print(f"Hour {idx + 1}:")
        print("Scores:", scores)
        print("States:", states)
        print("-" * 40)  # Separator for clarity
