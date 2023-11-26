import sys
sys.path.append(".")
import pandas as pd
from descriptors import start_stations_to_zips
from dataframe import aggregate_all_files


def preaggregation(input_csv, output_csv):
  """
  function which performs pre-processing on the raw csv with bike data

  input:
    input_csv: raw bike data
  
  output:
    output_csv: new csv with the same number of rows, but columns ride_id, zip_code, started_at_date, and total_length
  """

  dataframe = pd.read_csv(input_csv)

  # convert started_at to started_at_date, which deletes the time and contains only the date
  dataframe['started_at'] = pd.to_datetime(dataframe['started_at'])
  dataframe['started_at_date'] = dataframe['started_at'].dt.date

  # convert start time and end time to ride_length, make it an integer
  dataframe['ended_at'] = pd.to_datetime(dataframe['ended_at'])
  dataframe['ride_length'] = ((dataframe['ended_at'] - dataframe['started_at']).dt.total_seconds()) / 60
  dataframe['ride_length'] = dataframe['ride_length'].astype(int)

  # map start station name to zip code
  dataframe['zip_code'] = dataframe['start_station_name'].map(start_stations_to_zips)

  # keep only the necessary columns
  result_df = dataframe[['zip_code', 'ride_id', 'started_at_date', 'ride_length']]
  result_df.to_csv(output_csv, index=False)


def feature_extraction(input_csv, output_csv):
  """
  extract features from a pre-processed csv

  input:
    input_csv: the preprocessed csv with a row for each ride

  output:
    output_csv: the feature csv, with a row for each date and the following columns: 
      date
      total_length: minutes summed up for all rides started on that date
      number_of_rides
      zip_code: the start station zip code
  """
  df = pd.read_csv(input_csv, dtype={'zip_code': str})
  
  # calculate cumulative stats based on grouping by start date, all zip codes are same so just keep first
  cumulative_stats = df.groupby('started_at_date').agg({'ride_length': 'sum', 'ride_id': 'count', 'zip_code': 'first'}).reset_index()
  
  # rename columns and save csv
  cumulative_stats.columns = ['date', 'total_length', 'number_of_rides', 'zip_code']
  cumulative_stats.to_csv(output_csv, index=False)

if __name__ == '__main__':
  # perform the following steps for all bike raws
  input_csv = 'ml_preprocessing/bike_raw_07302.csv'
  preaggregation_csv = 'ml_preprocessing/bike_preaggregation_07302.csv'
  aggregation_csv = 'ml_preprocessing/bike_aggregation_07302.csv'

  preaggregation(input_csv, preaggregation_csv)
  feature_extraction(preaggregation_csv, aggregation_csv)

  file_list = ['ml_preprocessing/bike_aggregation_07302.csv', 'ml_preprocessing/bike_aggregation_07030.csv', 'ml_preprocessing/bike_aggregation_07310.csv']
  new_file = 'ml_preprocessing/bike_total_aggregation.csv'
  aggregate_all_files(file_list, new_file)