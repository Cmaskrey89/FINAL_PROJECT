from rating_parameters import read_hourly_forecast, parameter_scores

############# DEFINE THE SURF RATING SCORES ##########################

def calculate_surf_rating(states):
    
# 5 Star Rating Criteria

    if (states['windWave'] in ['Glass', 'Light'] and
        states['swell_period'] == 'Epic' and
        states['swell_disruption'] in ['Minimal Disruption', 'Mild Disruption'] and
        states['swell_height'] in ['MS', 'M', 'L'] and
        states['swell_x_tide'] == 'Ideal' and
        states['swell_direction'] == 'Optimal Direction'):
        return 5

# 4 Star Rating Criteria

    elif (states['windWave'] in ['Glass', 'Light'] and
          states['swell_period'] in ['Good', 'Epic'] and
          states['swell_disruption'] in ['Minimal Disruption', 'Mild Disruption', 'Moderate Disruption'] and
          states['swell_x_tide'] in ['Ideal', 'Working'] and
          states['swell_height'] in ['MS', 'M', 'L'] and
          states['swell_direction'] in ['Optimal Direction', 'Working Direction']):
        return 4

# 3 Star Rating Criteria

    elif (states['windWave'] != 'Blown' and
          states['windWave'] != 'Choppy!' and
          states['swell_period'] in ['Epic', 'Good', 'Medium'] and
          states['swell_disruption'] in ['Minimal Disruption', 'Mild Disruption', 'Moderate Disruption'] and
          states['swell_x_tide'] in ['Ideal', 'Working'] and
          states['swell_height'] in ['S', 'MS', 'M', 'L'] and
          states['swell_direction'] in ['Optimal Direction', 'Working Direction']):
        return 3

# 2 Star Rating Criteria

    elif (states['swell_x_tide'] in ['Ideal', 'Working']):
        return 2

# 1 Star Rating Criteria (basically anything left)

    else:
        return 1

########################## DEFINE MAIN FUNCTION ##########################
def main():
    data = read_hourly_forecast()
    
    for hour in data:
        scores, states = parameter_scores(hour)
        surf_rating = calculate_surf_rating(states)
        
        formatted_time = hour.get("time", "Unknown Time") #format time to test in printing.
        print(f"{formatted_time}: Surf Rating = {surf_rating} Star(s)") #debug
        print("States:", states) # debug
        print("-" * 80)  # Separator for clarity

if __name__ == "__main__":
    main()
