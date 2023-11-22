import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import pandas as pd
from descriptors import start_stations_to_zips, random_seed


def split_dataframes(input_csv, output_prefix = ''):
    """
    transform full dataframe at location input_csv into train_val and test dataframes
    output_prefix can optionally prepend to the generic csv names
    """
    # collect full dataframe
    full_dataframe = pd.read_csv(input_csv, dtype={'zip_code': str})

    # 0.8 into train_val, 0.2 into test
    train_validation, test = train_test_split(full_dataframe, test_size = 0.2, random_state = random_seed, stratify = full_dataframe['zip_code'])
    
    # 0.75 into train, 0.25 into val
    train, validation = train_test_split(train_validation, test_size = 0.25, random_state = random_seed, stratify = train_validation['zip_code'])

    # save into new csv for each
    test_csv = 'ml_normalize/' + output_prefix + 'test.csv'
    train_val_csv = 'ml_normalize/' + output_prefix + 'train_val.csv'
    train_csv = 'ml_normalize/' + output_prefix + 'train.csv'
    val_csv = 'ml_normalize/' + output_prefix + 'val.csv'



    test.to_csv(test_csv, index=False)
    train_validation.to_csv(train_val_csv, index=False)
    train.to_csv(train_csv, index=False)
    validation.to_csv(val_csv, index=False)


def fit_and_trans(fit_csv, trans_csv, new_fit_csv, new_trans_csv):
    """
    use fit_df to fit standardizers, transform both fit_df and trans_df

    input:
        fit_csv: file with dataframe to fit the standardizers and transform
        trans_csv: file with dataframe to be transformed only
        new_fit_csv: normalized train_val csv
        new_trans_csv: normalized test csv
    """

    fit_df = pd.read_csv(fit_csv, dtype={'zip_code': str})
    trans_df = pd.read_csv(trans_csv, dtype={'zip_code': str})
    columns_to_standardize = ['daylight', 'tempmax', 'tempmin', 'temp', 'feelslikemax', 'feelslikemin', 'feelslike', 'dew', 'windspeed', 'pressure', 'visibility']
    scaler_standardize = StandardScaler()

    # fit on train_val
    scaler_standardize = scaler_standardize.fit(fit_df[columns_to_standardize])

    # transform on both train_val and test
    fit_df[columns_to_standardize] = scaler_standardize.transform(fit_df[columns_to_standardize])
    trans_df[columns_to_standardize] = scaler_standardize.transform(trans_df[columns_to_standardize])

    columns_to_min_max_scale = ['precip', 'snow', 'snowdepth']
    scaler_min_max = MinMaxScaler()
    scaler_min_max = scaler_min_max.fit(fit_df[columns_to_min_max_scale])
    fit_df[columns_to_min_max_scale] = scaler_min_max.transform(fit_df[columns_to_min_max_scale])
    trans_df[columns_to_min_max_scale] = scaler_min_max.transform(trans_df[columns_to_min_max_scale])

    # target features need to be standardized each on their own zip code
    # to accommadate for some stations always having larger number of rides and minutes
    # possibly due to more bikes at that station, more foot traffic, etc
    columns_to_zip_standardize = ['total_length', 'number_of_rides']
    zip_codes = start_stations_to_zips.values()

    for zip_code in zip_codes:
        # get rows to standardize
        zip_code_rows_fit = fit_df[fit_df['zip_code'] == zip_code]
        zip_code_rows_trans = trans_df[trans_df['zip_code'] == zip_code]

        # scaler_zip = StandardScaler()
        # I tried using standardscaler but got back awful results, switched to robustscaler and performance significantly improved
        scaler_zip = RobustScaler()

        # fit and transform fit_df
        fit_df.loc[fit_df['zip_code'] == zip_code, columns_to_zip_standardize] = scaler_zip.fit_transform(zip_code_rows_fit[columns_to_zip_standardize])

        # transform trans_df
        trans_df.loc[trans_df['zip_code'] == zip_code, columns_to_zip_standardize] = scaler_zip.transform(zip_code_rows_trans[columns_to_zip_standardize])

    fit_df.to_csv(new_fit_csv, index=False)
    trans_df.to_csv(new_trans_csv, index=False)

def remove_anomalies(train_val_csv):
    """
    remove anomalies in-place for train_val_csv
    anomaly threshold can be changed, currently defined as anything with target feature >= 4 z-score
    saves back to same file that was passed in
    """
    # define threshold for a z-score abs. value for anomalies
    threshold = 4

    # read df
    train_val_df = pd.read_csv(train_val_csv, dtype={'zip_code': str})
    
    # create condition
    condition = (train_val_df['total_length'].abs() <= threshold) & (train_val_df['number_of_rides'].abs() <= threshold)

    # display removed values
    temp = train_val_df[(train_val_df['total_length'].abs() >= threshold)]
    print(temp)
    temp = train_val_df[(train_val_df['number_of_rides'].abs() >= threshold)]
    print(temp)

    # filter and save
    filtered_train_val_df = train_val_df[condition]
    filtered_train_val_df.to_csv(train_val_csv, index=False)


if __name__ == '__main__':
    split_dataframes('ml_normalize/dataframe.csv')
    
    train_val_csv = 'ml_normalize/train_val.csv'
    test_csv = 'ml_normalize/test.csv'
    train_csv = 'ml_normalize/train.csv'
    val_csv = 'ml_normalize/val.csv'
    
    new_train_val_csv = 'ml_learning/n_train_val.csv'
    new_test_csv = 'ml_learning/n_test.csv'
    new_train_csv = 'ml_learning/n_train.csv'
    new_val_csv = 'ml_learning/n_val.csv'

    # fit on train/val, transform on testing for when final testing is performed
    fit_and_trans(train_val_csv, test_csv, new_train_val_csv, new_test_csv)
    remove_anomalies(new_train_val_csv)

    # fit on train, transform on val to prevent data leakage during training and tuning based on val performance
    fit_and_trans(train_csv, val_csv, new_train_csv, new_val_csv)
    remove_anomalies(new_train_csv)