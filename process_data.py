import pandas as pd
from sqlalchemy import create_engine, text
import os

# --- Configuration ---
DATABASE_FILE = "police_logs.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}" 
TABLE_NAME = 'traffic_stops'
DATASET_PATH = "traffic_stops.csv" 

def create_and_load_database(df: pd.DataFrame, engine):
    """
    Creates the SQL table schema and loads the processed data.
    Corresponds to Step 2: Database Design (SQL)[cite: 24].
    """
    
    # 1. Define the SQL CREATE TABLE command
    # NOTE: The schema is adapted from the document's dataset explanation [cite: 89-103].
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        stop_id INTEGER PRIMARY KEY,
        stop_date DATE NOT NULL,
        stop_time TIME NOT NULL,
        country_name VARCHAR(50) NOT NULL,
        driver_gender CHAR(1),
        driver_age INT,
        driver_race VARCHAR(50),
        violation_raw VARCHAR(100),
        violation VARCHAR(100) NOT NULL,
        search_conducted BOOLEAN NOT NULL,
        search_type VARCHAR(100),
        stop_outcome VARCHAR(50),
        is_arrested BOOLEAN NOT NULL,
        stop_duration VARCHAR(20),
        drugs_related_stop BOOLEAN NOT NULL,
        vehicle_number VARCHAR(20)
    );
    """
    
    with engine.connect() as connection:
        # Execute the CREATE TABLE statement
        connection.execute(text(create_table_sql))
        connection.commit()
        print(f"Table '{TABLE_NAME}' created successfully.")

        # 2. Insert data into the SQL table
        # We use 'append' since we create the schema explicitly above
        df.to_sql(TABLE_NAME, engine, if_exists='append', index=True, index_label='stop_id')
        print(f"Data successfully loaded into '{TABLE_NAME}'. Total rows: {len(df)}")


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles data cleaning and preprocessing (Step 1)[cite: 21].
    - Removes the column 'driver_age_raw' (since 'driver_age' is available)
    - Converts boolean columns to appropriate format (True/False)
    - Handles NaN values[cite: 23].
    """
    print("Starting data preprocessing...")

    # Drop columns that only contain missing value (not strictly needed for this clean dataset) [cite: 22]
    df_cleaned = df.dropna(axis=1, how='all')

    # Drop raw columns as suggested by the schema
    df_cleaned = df_cleaned.drop(columns=['driver_age_raw'], errors='ignore')

    # Handle NaN values for categorical columns (e.g., search_type)
    df_cleaned['search_type'].fillna('None Conducted', inplace=True)
    df_cleaned['vehicle_number'].fillna('Unknown', inplace=True)

    # Convert boolean columns to ensure correct storage in SQLite
    for col in ['search_conducted', 'is_arrested', 'drugs_related_stop']:
        df_cleaned[col] = df_cleaned[col].astype(bool)

    # Convert date and time columns
    df_cleaned['stop_date'] = pd.to_datetime(df_cleaned['stop_date']).dt.date
    df_cleaned['stop_time'] = pd.to_datetime(df_cleaned['stop_time']).dt.time
    
    print("Data preprocessing complete.")
    return df_cleaned

if __name__ == "__main__":
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)
        print(f"Existing database file '{DATABASE_FILE}' removed.")

    # 1. Load and preprocess
    try:
        data = pd.read_csv(DATASET_PATH)
        processed_data = preprocess_data(data)
    except FileNotFoundError:
        print(f"Error: Dataset file '{DATASET_PATH}' not found. Cannot proceed.")
        exit()

    # 2. Initialize database and load data
    engine = create_engine(DATABASE_URL)
    create_and_load_database(processed_data, engine)
    
    print("\nDatabase initialization complete. Run 'streamlit run app.py' next.")