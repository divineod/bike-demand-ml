import yaml
import warnings
import configparser
import pandas as pd
from flask import Flask, request, jsonify
from datetime import datetime
from catboost import CatBoostRegressor
from urllib3.exceptions import InsecureRequestWarning
import logging

# Suppress specific warnings to improve log readability
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

# Configure pandas to avoid chained assignment warnings
pd.set_option('mode.chained_assignment', None)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load configuration items
config = configparser.RawConfigParser()
config.optionxform = lambda option: option
config.read('app/config.ini')
data_path = dict(config.items('paths'))['data']
model_path = dict(config.items('paths'))['model']
features_path = dict(config.items('paths'))['features']

app = Flask(__name__)

# Initialize CatBoostRegressor and load the pre-trained model
loaded_cat_model = CatBoostRegressor()
cat_model = loaded_cat_model.load_model(model_path)

# Load the master training dataset with specified dtypes for efficiency
master_df = pd.read_csv(f"{data_path}/training_data.csv", dtype={'hr': int, 'yr': int, 'cnt': float})
model_features = []

# Load model features from configuration
with open(features_path, 'r') as stream:
    try:
        configs = yaml.safe_load(stream)
        model_features = configs.get('model_features', [])
    except yaml.YAMLError as exc:
        logging.error(f"Error loading feature configuration: {exc}")


def process_data_for_prediction(date_str: str, df: pd.DataFrame, features: list) -> pd.DataFrame:
    """
    Processes the master dataset to prepare it for prediction based on the input date.

    Parameters:
        date_str (str): The date in 'YYYY-MM-DD' format.
        df (pd.DataFrame): The master dataset DataFrame.
        features (list): List of model features used for prediction.

    Returns:
        pd.DataFrame: The processed DataFrame ready for prediction.
    """
    forecast_date = datetime.strptime(date_str, '%Y-%m-%d')
    df['dteday'] = pd.to_datetime(df['dteday'])
    df.sort_values(by='dteday', inplace=True)

    filtered_df = master_df[(df['dteday'].dt.month == forecast_date.month) &
                            (df['dteday'].dt.day == forecast_date.day)]
    filtered_df = filtered_df[features]

    filtered_df.drop(columns=['dteday'], inplace=True)
    grouped_by_hour = filtered_df.groupby('hr').mean().reset_index()
    grouped_by_hour['yr'] = forecast_date.year - 2011

    return grouped_by_hour

@app.route('/prediction', methods=['POST'])
def predict() -> jsonify:
    """
    Endpoint for predicting bike rental demand based on input date.
    Expects a JSON payload with a 'date' key in 'YYYY-MM-DD' format.

    Returns:
        JSON response with hourly predictions or an error message.
    """
    data = request.get_json(force=True)
    date_str = data.get('date', '')

    try:
        forecast_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError as e:
        logging.error(f"Incorrect date format for {date_str}. Error: {e}")
        return jsonify({'error': f"Incorrect date format: {date_str}. Please use YYYY-MM-DD format."}), 400

    # Process the dataset to match the required input format for the prediction model
    grouped_by_hour = process_data_for_prediction(date_str, master_df, model_features)

    predictions = cat_model.predict(grouped_by_hour)
    result_dict = {hour: prediction for hour, prediction in zip(grouped_by_hour['hr'], predictions)}

    return jsonify(result_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
