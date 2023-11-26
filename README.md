## General Overview
This project has two main aims:
1. Graphing weather data in an easy-to-read fashion
2. Using machine learning to predict CitiBike ride patterns

## User Interaction Pipeline
The user runs the project by running the 'complete_testing.py' file in 'complete_testing/'. 

The user is first prompted for their date ranges and US Zip Codes using the files in 'user/', specifically making a call to the function 'get_date_range_keys_zip_codes_values_dictionary'. The files in 'user/' perform significant filtering, ensuring that no invalid zip codes or dates are used, re-prompting the user as needed. Additional filtering includes gracefully handling the user exceeded the maximum allowed date and the user exceeding the maximum query cost.

The user's chosen date ranges and zip codes are used to extract information for plotting purposes, such as the number of date intervals and the number of zip codes. The program then builds the API query, and the results are transformed into a dataframe. Additional preprocessing takes place, including creating new columns based on already present weather data, as well as dropping extraneous columns. 

The user is then repeatedly asked for metrics to plot. One of these includes 'bikerides' as long as all zip codes they selected were in the available list. The available list consists only of zip codes that have been trained on. The correct plotting function is called based on how many intervals there are. If the user chooses to plot 'bikerides', the program performs preprocessing and then runs the model on the weather data. The user is then able to view both the total number of expected rides from that zip code, as well as the percentile score for that number of rides. Additionally, the median, average, and standard deviation for the location are all printed to the user. The user can repeatedly graph metrics until they choose to exit.

## Machine Learning Pipeline
I randomly selected three start stations that had ~ >30 rides per day from the Jersey City CitiBike dataset and downloaded all data between 2022-11-01 and 2023-10-31. I performed preprocessing by aggregating the individual rides into daily totals and total ride lengths (in 'ml_preprocessing/bike.py'), and put all the bike data into one file. I performed a weather data query for each day in the interval and performed preprocessing on the weather data (in 'ml_preprocessing/weather.py'). This included adding scaling certain features, dropping columns, renaming columns, and creating a new 'workday' feature, which tracks whether the day is a work day or not. The 'bike' and 'weather' dataframes were then merged on date and zip code in 'ml_preprocessing/dataframe.py'.

In 'ml_normalize/split.py', the one large dataframe was split into smaller dataframes:
* train_validation: the training data and the validation data in one large dataframe, for hyperparameter optimization
* train: the training data, for training models to be tested on the validation data
* validation: used as the test data when testing performance on all models to determine best model
* test: the test data, which was only used to test the performance of the best performing model at the final step
* fs_train_validation: for the purposes hyperparameter optimization in feature selection, the training data and validation data
* fs_train: in feature selection, the training data only for training models to be tested on validation data
* fs_validation: the feature selection validation data
* fs_tune: the data used to pick features using feature selection

These dataframes were then fit and transformed appropriately, ensuring no data leakage occurred between training/validation, training_validation/test, or tune/training_validation. Anomalies were removed from training and train_validation, but not validation, tune, or test. This is to ensure training is optimized while avoiding providing an artificial boost to testing by removing anomalies.

Next, I performed feature selection. I wanted to compare performance across different sets of features. I started with the following sets of predictors:
* all_predictors: set containing all of the available weather features
* baseline_predictors: set containing basic features that do not involve weather. contains only is_work_day and daylight (time between sunrise and sunset)
* domain_predictors: set containing features that I hypothesized would be most predictive

I then ran 'ml_learning/feature_selection' and viewed the correlation matrix. I chose the most correlated features with the target, while also using domain knowledge and avoiding selecting features that were highly correlated with each other. The result was the fourth set of predictors: selection_predictors.

Finally, I ran 'ml_learning/runmodels.py'. This file leverages all models built in 'ml_learning/' by performing hyperparameter search for each on the train_validation, then training on train, and then testing on validation. The result for each model on each predictor is saved to a .txt file to be read by the user. 

I then tested the best performing model from validation testing on the test data as well as the best performing baseline model from validation on the test data. Results are reported below.
* Optimal Baseline Model
	* Model Type: Random Forest
	* Performance on Test Data: r^2 = 0.491
* Optimal Model
	* Model Type: Random Forest
	* Predictors: selection_predictors
	* Performance on Test Data: r^2 = 0.741

I saved the results of the best performing model into a pickle file. This pickle file is opened and used when future test cases are encountered. Importantly, when real life test cases are encountered, they are also transformed based on the fit of the training_validation dataset, which was also saved into a pickle during training. 

## Folders
Each file has a docstring which explains its purpose. I will explain briefly what each folder represents.
* 
