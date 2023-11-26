import sys
sys.path.append(".")
from query import get_query_result_for_date_range_zip_code
import json
from convert_to_dataframe import clean_convert_dictionary_to_dataframe
import pandas as pd
from dataframe import aggregate_all_files

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

  # remove columns
  weather_dataframe = weather_dataframe.drop(['start_date', 'end_date', 'winddir', 'severerisk', 'sunrise', 'sunset', 'moonphase'], axis=1)
  # rename datetime to date to match bike dataframe
  weather_dataframe = weather_dataframe.rename(columns={'datetime': 'date'})

  # define normalization instructions
  columns_to_divide_by_100 = ['humidity', 'precipcover', 'cloudcover']
  columns_to_divide_by_10 = ['uvindex']

  # normalize
  weather_dataframe[columns_to_divide_by_100] /= 100
  weather_dataframe[columns_to_divide_by_10] /= 10

  # create new feature 'is_work_day'
  weather_dataframe['date'] = pd.to_datetime(weather_dataframe['date'])
  weather_dataframe['is_work_day'] = (weather_dataframe['date'].dt.weekday < 5).astype(int)

  # check if it is a national holiday, in which case change to not work day
  weekdays_that_were_federal_holidays = ['2022-11-11', '2022-11-24', '2022-11-25', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04', '2023-10-09']
  weather_dataframe.loc[weather_dataframe['date'].isin(weekdays_that_were_federal_holidays), 'is_work_day'] = 0

  weather_dataframe.to_csv(output_csv, index=False)


if __name__ == '__main__':
  # weather_query_output_file = 'ml_preprocessing/weather_raw_07302.json'
  # get_weather_bike_data('2023-10-30', '2023-10-31', '07302', 'weather_raw_07302.json')
  # weather_normalize_output_file = 'ml_preprocessing/weather_normalized_07302.csv'
  # normalize_weather_dataframe(weather_query_output_file, weather_normalize_output_file)
  file_list = ['ml_preprocessing/weather_normalized_07302.csv', 'ml_preprocessing/weather_normalized_07030.csv', 'ml_preprocessing/weather_normalized_07310.csv']
  new_file = 'ml_preprocessing/weather_total_normalized.csv'
  aggregate_all_files(file_list, new_file)
