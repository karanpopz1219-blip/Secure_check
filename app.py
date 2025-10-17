import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# Streamlit page configuration must be set before any other Streamlit API calls
# (including decorators like @st.cache_resource). Place it immediately after imports.
st.set_page_config(page_title="SecureCheck: Police Post Digital Ledger 🚓", layout="wide")

# --- Configuration ---
DATABASE_URL = "sqlite:///police_logs.db" 
TABLE_NAME = 'traffic_stops'

# Connect to the database
@st.cache_resource
def get_database_engine():
    """Initializes and returns the database engine (for PostgreSQL/MySQL/SQLite)[cite: 19]."""
    try:
        engine = create_engine(DATABASE_URL)
        # Verify connection
        with engine.connect() as conn:
            conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}"))
        return engine
    except Exception as e:
        st.error(f"Database connection error: {e}. Please ensure 'process_data.py' was run first.")
        st.stop()

engine = get_database_engine()

# --- Functions for Database Interaction ---

def fetch_data(query_text):
    """Executes a SQL query and returns the results as a Pandas DataFrame[cite: 28]."""
    try:
        with engine.connect() as connection:
            df = pd.read_sql(text(query_text), connection)
            return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame()

def log_new_stop(log_data):
    """
    Inserts a new police log entry into the traffic_stops table (Real-time logging)[cite: 9].
    """
    try:
        log_df = pd.DataFrame([log_data])
        # Use if_exists='append' for real-time logging
        log_df.to_sql(TABLE_NAME, engine, if_exists='append', index=False)
        st.success("✅ New Stop Logged Successfully!")
    except Exception as e:
        st.error(f"Error logging stop: {e}")


# --- Streamlit Application Layout ---
st.title("SecureCheck: Digital Police Post Logs")

# --- 1. Real-time Logging Section ---
st.header("1. Add New Police Log")

with st.form("new_log_form"):
    st.markdown("Enter details for a new vehicle stop (Real-time logging)[cite: 9].")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stop_date = st.date_input("Stop Date", datetime.now().date())
        stop_time = st.time_input("Stop Time", datetime.now().time())
        country_name = st.text_input("Country Name", "India")
        vehicle_number = st.text_input("Vehicle Number (e.g., RJ83PZ4441)")
        
    with col2:
        driver_gender = st.selectbox("Driver Gender", ['M', 'F', 'Other'])
        driver_age = st.number_input("Driver Age", min_value=16, max_value=100, value=30)
        violation = st.selectbox("Violation Type", ['Speeding', 'DUI', 'Seatbelt', 'Signal', 'Other'])
        stop_duration = st.selectbox("Stop Duration [cite: 102]", ['<5 min', '6-15 min', '16-30 min', '30+ min'])
    
    with col3:
        search_conducted = st.checkbox("Search Conducted? [cite: 98]")
        drugs_related_stop = st.checkbox("Drug-Related Stop? [cite: 103]")
        is_arrested = st.checkbox("Resulted in Arrest? [cite: 101]")
        stop_outcome = st.selectbox("Stop Outcome [cite: 100]", ['Citation', 'Warning', 'Arrest', 'None'])

    submitted = st.form_submit_button("Submit Log (Real-time Update)")
    
    if submitted:
        # Prepare data for insertion (using default/placeholder values for fields not in the form)
        new_log = {
            'stop_date': stop_date,
            'stop_time': stop_time,
            'country_name': country_name,
            'vehicle_number': vehicle_number,
            'driver_gender': driver_gender[0], # Use first letter
            'driver_age': driver_age,
            'violation': violation,
            'violation_raw': violation, # Use violation for raw as well
            'search_conducted': search_conducted,
            'drugs_related_stop': drugs_related_stop,
            'is_arrested': is_arrested,
            'stop_outcome': stop_outcome,
            'stop_duration': stop_duration,
            'driver_race': 'Unknown', 
            'search_type': 'None Conducted' if not search_conducted else 'Vehicle Search'
        }
        log_new_stop(new_log)

st.markdown("---")

# --- 2. Advanced Insights and Analytics Section ---
st.header("2. Advanced Insights (Data-backed Decision Making) [cite: 39]")

# Dictionary of complex and medium SQL queries from the document [cite: 53, 76]
ANALYTICS_QUERIES = {
    "Top 10 Vehicles in Drug-Related Stops [cite: 56]": """
        SELECT vehicle_number, COUNT(*) AS drug_stop_count
        FROM traffic_stops
        WHERE drugs_related_stop = TRUE AND vehicle_number IS NOT NULL
        GROUP BY vehicle_number
        ORDER BY drug_stop_count DESC
        LIMIT 10;
    """,
    "Arrest Rate by Driver Age Group [cite: 59]": """
        SELECT
            CASE
                WHEN driver_age BETWEEN 16 AND 25 THEN '16-25'
                WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
                WHEN driver_age BETWEEN 36 AND 45 THEN '36-45'
                ELSE '46+'
            END AS age_group,
            CAST(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS arrest_rate_percentage
        FROM traffic_stops
        GROUP BY age_group
        ORDER BY arrest_rate_percentage DESC;
    """,
    "Violations with High Search/Arrest Rates [cite: 80]": """
        SELECT 
            violation,
            CAST(SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS search_rate,
            CAST(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) AS arrest_rate,
            (CAST(SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*) + 
             CAST(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS REAL) * 100 / COUNT(*)) / 2 AS combined_rate
        FROM traffic_stops
        GROUP BY violation
        ORDER BY combined_rate DESC;
    """
}

# Dropdown to select a query
query_selection = st.selectbox("Select an Analytics Query to Run:", list(ANALYTICS_QUERIES.keys()))

if st.button("Run Analytics Query"):
    selected_query = ANALYTICS_QUERIES[query_selection]
    results_df = fetch_data(selected_query)
    
    if not results_df.empty:
        st.subheader(f"Results for: {query_selection}")
        st.dataframe(results_df, use_container_width=True)

        # Basic visualization for rate analysis
        if 'arrest_rate_percentage' in results_df.columns:
            st.bar_chart(results_df, x='age_group', y='arrest_rate_percentage')
        elif 'combined_rate' in results_df.columns:
            st.bar_chart(results_df, x='violation', y='combined_rate')


st.markdown("---")

# --- 3. Latest Logs Display and Search Filter ---
st.header("3. Real-time Logs and Quick Search [cite: 27, 28]")

# Implement SQL-based search filters for quick lookups [cite: 28]
search_term = st.text_input("Search Logs by Country Name or Vehicle Number:")

# Construct the query based on the search filter
base_query = f"""
    SELECT 
        stop_id, stop_date, stop_time, country_name, vehicle_number, 
        violation, stop_outcome, is_arrested, drugs_related_stop 
    FROM {TABLE_NAME}
"""
where_clause = ""
if search_term:
    where_clause = f"WHERE country_name LIKE '%{search_term}%' OR vehicle_number LIKE '%{search_term}%'"

final_query = f"{base_query} {where_clause} ORDER BY stop_date DESC, stop_time DESC LIMIT 50"

latest_logs_df = fetch_data(final_query)
st.dataframe(latest_logs_df, use_container_width=True)

# Footer/Technical tags [cite: 46]
st.sidebar.markdown("### Technical Tags")
st.sidebar.write("- Python [cite: 47]")
st.sidebar.write("- Data preprocessing [cite: 48]")
st.sidebar.write("- PostgreSQL/MySQL/SQLite [cite: 49]")
st.sidebar.write("- Streamlit for dashboard creation [cite: 50]")