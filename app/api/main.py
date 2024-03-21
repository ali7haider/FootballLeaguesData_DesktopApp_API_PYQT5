# main.py
import datetime
import os
import pandas as pd
from utils.utils import get_championship_data, get_api_key, API_FOOTBALL_PLAYERS_ENDPOINT, save_df_to_csv, clean_weight_height

# Data Path
DATA_PATH = "data"

def main(country, league, championship_code):
    # Retrieve API key
    key = get_api_key()

    # Get today's date
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    country_league = f"{country}_{league}"

    # Check if the data for the specified country_league and today's date already exists
    csv_file_path = os.path.join(DATA_PATH, f"{country_league}_{today_date}.csv")
    if os.path.exists(csv_file_path):
        print(f"Data for {country} - {league} already exists for today's date.")
        return pd.read_csv(csv_file_path)

    print(f"Downloading data for {country} - {league}...")
    
    # Get championship dataset from API
    championship_df = get_championship_data(API_FOOTBALL_PLAYERS_ENDPOINT, key, championship_code)    
    # Clean dataset
    cleaned_df = clean_weight_height(championship_df)
    
    # Save dataset to CSV
    save_df_to_csv(cleaned_df, country_league)

    print(f"Data for {country} - {league} downloaded and saved successfully.")
    return cleaned_df

if __name__ == "__main__":
    # Pass the country_league and key of specific
    country_league = "MAJOR_LEAGUE"  # Example: "MAJOR_LEAGUE" or "INDIA_LEAGUE"
    key = '253'  # Retrieve your API key
    data = main(country_league, key)
