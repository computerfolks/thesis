import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from query import get_query_result_for_date_range_zip_code
import json
from convert_to_dataframe import clean_convert_dictionary_to_dataframe
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd

def get_weather_bike_data(start_date, end_date, zip_code, output_file):
  """
  query for weather data, save into json

  input:
    start_date, end_date, zip_code, output_file
  
  output:
    json with weather query result tuples modified to list to be compatible
  """
  user_query_result = get_query_result_for_date_range_zip_code(start_date, end_date, str(zip_code))
  with open(output_file, 'w') as outfile:
    json.dump(user_query_result, outfile, indent=2)


def normalize_weather_dataframe(input_json, output_csv):
  """
  given a json filepath with raw query results, create and normalize a dataframe and save to output_csv
  """
  with open(input_json, 'r') as file:
    loaded_data = json.load(file)

  # reconstruct object as it was when returned by query function
  raw_key = tuple(loaded_data[0])
  raw_value = loaded_data[1]
  query_raw_result = {raw_key:raw_value}

  weather_dataframe = clean_convert_dictionary_to_dataframe(query_raw_result)
  # print(weather_dataframe.columns)
  # print(weather_dataframe)

  # clean dataframe
  # remove columns
  weather_dataframe = weather_dataframe.drop(['start_date', 'end_date', 'winddir', 'severerisk', 'sunrise', 'sunset'], axis=1)
  # rename datetime to date to match bike dataframe
  weather_dataframe = weather_dataframe.rename(columns={'datetime': 'date'})

  # define normalization instructions
  columns_to_standardize = ['daylight', 'tempmax', 'tempmin', 'temp', 'feelslikemax', 'feelslikemin', 'feelslike', 'dew', 'windspeed', 'pressure', 'visibility']
  columns_to_divide_by_100 = ['humidity', 'precipcover', 'cloudcover']
  columns_to_divide_by_10 = ['uvindex']
  columns_to_min_max_scale = ['precip', 'snow', 'snowdepth']

  # normalize
  scaler_standardize = StandardScaler()
  scaler_min_max = MinMaxScaler()
  weather_dataframe[columns_to_standardize] = scaler_standardize.fit_transform(weather_dataframe[columns_to_standardize])
  weather_dataframe[columns_to_divide_by_100] /= 100
  weather_dataframe[columns_to_divide_by_10] /= 10
  weather_dataframe[columns_to_min_max_scale] = scaler_min_max.fit_transform(weather_dataframe[columns_to_min_max_scale])

  # create new feature 'is_work_day'
  weather_dataframe['date'] = pd.to_datetime(weather_dataframe['date'])
  weather_dataframe['is_work_day'] = (weather_dataframe['date'].dt.weekday < 5).astype(int)

  # check if it is a national holiday, in which case change to not work day
  weekdays_that_were_federal_holidays = ['2022-11-11', '2022-11-24', '2022-11-25', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04', '2023-10-09']
  weather_dataframe.loc[weather_dataframe['date'].isin(weekdays_that_were_federal_holidays), 'is_work_day'] = 0

  weather_dataframe.to_csv(output_csv, index=False)


if __name__ == '__main__':
  weather_query_output_file = 'ml_processing/weather_raw.json'
  # get_weather_bike_data('2022-11-01', '2023-10-31', '07310', 'weather_raw.json')
  weather_normalize_output_file = 'ml_processing/weather_normalized.csv'
  normalize_weather_dataframe(weather_query_output_file, weather_normalize_output_file)
