import pandas as pd
import os

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs data cleaning and preprocessing as required by the project (Step 1).
    1. Removes columns with all missing values.
    2. Handles NaN values.
    """
    print("Starting data preprocessing...")

    # 1. Remove columns that only contains missing value [cite: 22]
    # (The traffic_stops.csv is very clean, but this code handles that requirement)
    df_cleaned = df.dropna(axis=1, how='all')

    # Remove the 'driver_age_raw' column since the cleaned 'driver_age' is available.
    df_cleaned = df_cleaned.drop(columns=['driver_age_raw'], errors='ignore')

    # 2. Handle the NAN values [cite: 23]
    
    # Fill missing categorical columns with a sensible default:
    # 'search_type' is often NaN if 'search_conducted' is False.
    df_cleaned['search_type'].fillna('None Conducted', inplace=True)
    # Fill vehicle_number if missing
    df_cleaned['vehicle_number'].fillna('Unknown', inplace=True)

    # Ensure boolean columns are correctly represented
    for col in ['search_conducted', 'is_arrested', 'drugs_related_stop']:
        df_cleaned[col] = df_cleaned[col].astype(bool)

    # Convert date and time columns to appropriate types for database insertion
    df_cleaned['stop_date'] = pd.to_datetime(df_cleaned['stop_date']).dt.date
    df_cleaned['stop_time'] = pd.to_datetime(df_cleaned['stop_time'], format='%H:%M:%S').dt.time
    
    print("Data preprocessing complete.")
    return df_cleaned

# --- Example Execution ---
if __name__ == "__main__":
    DATASET_PATH = "traffic_stops.csv" 
    
    try:
        # Load the raw data
        raw_data = pd.read_csv(DATASET_PATH)
        print(f"Raw Data Shape: {raw_data.shape}")

        # Process the data
        processed_data = preprocess_data(raw_data)

        # Display results of cleaning
        print("\n--- Processed Data Head ---")
        print(processed_data.head().to_markdown(index=False, numalign="left", stralign="left"))
        print(f"\nProcessed Data Shape: {processed_data.shape}")

        # The processed_data DataFrame is now ready to be loaded into SQL.

    except FileNotFoundError:
        print(f"Error: Dataset file '{DATASET_PATH}' not found. Please ensure the file is in the current directory.")