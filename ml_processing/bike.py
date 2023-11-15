import pandas as pd
from descriptors import start_stations_to_zips


def preaggregation(input_csv, output_csv):

  # Read the original CSV
  df = pd.read_csv(input_csv)

  # Convert 'started_at' and 'ended_at' columns to datetime objects
  df['started_at'] = pd.to_datetime(df['started_at'])
  df['ended_at'] = pd.to_datetime(df['ended_at'])

  # Create a new column 'started_at_date' with only the date portion
  df['started_at_date'] = df['started_at'].dt.date

  # Create a new column 'ride_length' with the duration of the ride
  df['ride_length'] = ((df['ended_at'] - df['started_at']).dt.total_seconds()) / 60

  # Convert 'ride_length' to integers
  df['ride_length'] = df['ride_length'].astype(int)

  # Create zip code
  df['zip_code'] = df['start_station_name'].map(start_stations_to_zips)

  # Keep only the required columns
  result_df = df[['zip_code', 'ride_id', 'started_at_date', 'ride_length']]

  # Save the result to a new CSV file
  result_df.to_csv(output_csv, index=False)


def feature_extraction(input_csv, output_csv):
  # Read the original CSV
  df = pd.read_csv(input_csv, dtype={'zip_code': str})

  # Convert 'start_date' to datetime objects
  df['started_at_date'] = pd.to_datetime(df['started_at_date']).dt.date

  # Group by 'start_date' and calculate the sum of 'ride_length' and count the number of rides
  cumulative_stats = df.groupby('started_at_date').agg({'ride_length': 'sum', 'ride_id': 'count', 'zip_code': 'first'}).reset_index()

  # Rename columns for clarity
  cumulative_stats.columns = ['date', 'total_length', 'number_of_rides', 'zip_code']

  # Save the result to a new CSV file
  cumulative_stats.to_csv(output_csv, index=False)


if __name__ == '__main__':
  input_csv = 'ml_processing/bike_raw.csv'
  preaggregation_csv = 'ml_processing/bike_preaggregation.csv'
  aggregation_csv = 'ml_processing/bike_aggregation.csv'

  preaggregation(input_csv, preaggregation_csv)
  feature_extraction(preaggregation_csv, aggregation_csv)