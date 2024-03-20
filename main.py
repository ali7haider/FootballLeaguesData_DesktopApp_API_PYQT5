# main.py

from utils.utils import get_championship_data, get_api_key, API_FOOTBALL_PLAYERS_ENDPOINT, \
    save_df_to_csv, clean_weight_height, CHAMPIONSHIPS

def main():
    # Retrieve API key
    key = get_api_key()
    
    # Iterate over championships
    for championship_name, championship_code in CHAMPIONSHIPS.items():
        print(f"Downloading data for {championship_name}...")
        
        # Get championship dataset
        championship_df = get_championship_data(API_FOOTBALL_PLAYERS_ENDPOINT, key, championship_code)
        
        # Clean dataset
        cleaned_df = clean_weight_height(championship_df)
        
        # Save dataset to CSV
        save_df_to_csv(cleaned_df, championship_name)
        
        print(f"Data for {championship_name} downloaded and saved successfully.")

if __name__ == "__main__":
    main()
