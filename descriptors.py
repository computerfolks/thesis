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

# columns that can always be graphed by matplotlib
# NOTE: if the weather dataframe is missing some of this data due to collection being unavailable, the graph may appear strange
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

# predictor lists used for machine learning

# use all available metrics as predictors
all_predictors = ['tempmax','tempmin','temp','feelslikemax','feelslikemin','feelslike','dew','humidity','precip','precipcover','snow','snowdepth','windgust','windspeed','pressure','cloudcover','visibility','solarradiation','solarenergy','uvindex','daylight','is_work_day']

# the 'domain expert' metrics chosen that are thought to be most predictive without using the data for feature selection
domain_predictors = ['temp','humidity','precip','snow','snowdepth','windspeed','pressure','cloudcover','visibility','daylight', 'is_work_day']

# predictors for a baseline model which does not account for weather, used for comparison purposes
baseline_predictors = ['daylight','is_work_day']

# predictors as determined by performing feature selection
selection_predictors = ['temp','precip','precipcover','windspeed','cloudcover','visibility','uvindex','daylight']

# random seed for scikitlearn functions that have the option
random_seed = 23907251

# max query cost allowed for a user. 1000 credits available per day.
max_query_cost = 100