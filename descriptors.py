# store dictionary to be imported which maps pandas dataframe column names to English explanation
descriptions_for_column_keys = {
    'start_date': 'Starting date of data',
    'end_date': 'Ending date of data',
    'zip_code': 'Zip code location',
    'datetime': 'Date and time of data',
    'daylight': 'Seconds of daylight',
    'tempmax': 'Maximum temperature',
    'tempmin': 'Minimum temperature',
    'temp': 'Average temperature',
    'feelslikemax': 'Maximum "feels like" temperature',
    'feelslikemin': 'Minimum "feels like" temperature',
    'feelslike': 'Average "feels like" temperature',
    'dew': 'Dew point',
    'humidity': 'Humidity level',
    'precip': 'Precipitation amount',
    'precipcover': 'Extent of precipitation coverage',
    'snow': 'Snowfall amount',
    'snowdepth': 'Depth of snowfall',
    'windgust': 'Maximum wind gust',
    'windspeed': 'Wind speed',
    'winddir': 'Wind direction',
    'pressure': 'Atmospheric pressure',
    'cloudcover': 'Cloud cover percentage',
    'visibility': 'Visibility distance',
    'solarradiation': 'Solar radiation amount',
    'solarenergy': 'Solar energy level',
    'uvindex': 'UV index',
    'severerisk': 'Risk of severe weather',
    'sunrise': 'Time of sunrise',
    'sunset': 'Time of sunset',
    'moonphase': 'Phase of the moon',
    'number_of_rides': 'Predicted number of citiBike rides',
    'zscore_percentile': 'Percentile score for expected activity'
}

# columns that can be graphed by matplotlib
graphable_columns = [
    'daylight',
    'tempmax',
    'tempmin',
    'temp',
    'feelslikemax',
    'feelslikemin',
    'feelslike',
    'dew',
    'humidity',
    'precip',
    'precipcover',
    'snow',
    'snowdepth',
    'windgust',
    'windspeed',
    'pressure',
    'cloudcover',
    'visibility',
    'solarradiation',
    'solarenergy',
    'uvindex',
    'moonphase']

# map start station names to zip codes
start_stations_to_zips = {
    'Newport PATH' : '07310',
    'South Waterfront Walkway - Sinatra Dr & 1 St' : '07030',
    'Marin Light Rail' : '07302'
}

# predictor list for machine learning
all_predictors = ['tempmax','tempmin','temp','feelslikemax','feelslikemin','feelslike','dew','humidity','precip','precipcover','snow','snowdepth','windgust','windspeed','pressure','cloudcover','visibility','solarradiation','solarenergy','uvindex','daylight','is_work_day']
domain_predictors = ['temp','humidity','precip','snow','snowdepth','windspeed','pressure','cloudcover','visibility','daylight', 'is_work_day']
baseline_predictors = ['daylight','is_work_day']
selection_predictors = ['temp','precip','precipcover','windspeed','cloudcover','visibility','uvindex','daylight']

targets = ['number_of_rides', 'total_length']
target = 'number_of_rides'

# random seed for training
random_seed = 23907251

# scoring system, can be 'r2' or 'neg_mean_squared_error', among others. To see full list, put in a random string and allowed values will be printed to terminal
scoring = 'r2'