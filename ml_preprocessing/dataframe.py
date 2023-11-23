import sys
sys.path.append(".")
import pandas as pd

def aggregate_all_files(file_list, new_file):
  """
  a generic dataframe aggregator which takes a list of csvs that have all the same columns,
  and combines all the rows into one dataframe / csv in new_file
  """
  combined_dataframe = pd.DataFrame()

  for file in file_list:
    current_dataframe = pd.read_csv(file, dtype={'zip_code': str})
    combined_dataframe = pd.concat([combined_dataframe, current_dataframe], ignore_index=True)

  combined_dataframe.to_csv(new_file, index=False)

if __name__ == '__main__':

    # load bike and weather dataframes
    bike_file = 'ml_preprocessing/bike_total_aggregation.csv'
    weather_file = 'ml_preprocessing/weather_total_normalized.csv'
    dataframe_bike = pd.read_csv(bike_file, dtype={'zip_code': str})
    dataframe_weather = pd.read_csv(weather_file, dtype={'zip_code': str})

    # merge dataframe on date and zip code
    merged_dataframe = pd.merge(dataframe_bike, dataframe_weather, on=['date', 'zip_code'], how='outer')
    merged_dataframe = merged_dataframe.dropna()

    # save to csv
    merged_dataframe.to_csv('ml_normalize/dataframe.csv', index=False)
    print(merged_dataframe)