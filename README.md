# Secure_check
🚔 Project Report: SecureCheck — A Python-SQL Digital Ledger for Police Post Logs
Domain: Law Enforcement & Public Safety
This project falls under the domain of Real-Time Monitoring Systems in law enforcement.
It aims to modernize how police check posts record, analyze, and monitor vehicle stop data using Python, SQL, and Streamlit.
Project Introduction ;

SecureCheck provides a centralized digital system for logging and analyzing traffic stop records.
The system improves data accuracy, enables real-time alerts, and supports data-driven policing decisions.

Objective ;

To design a secure, SQL-based vehicle stop database and an interactive Python dashboard that provides instant insights on arrests, violations, and suspect vehicles.

Approach ;
	•	Data Collection: Imported and cleaned the dataset (traffic_stops.csv).
	•	ELT Approach: Extracted raw CSV data → Loaded into SQL → Transformed using SQL queries.
	•	Data Migration: Data was transferred from MongoDB to MySQL using Python pandas and sqlalchemy libraries.
	•	EDA: Performed data analysis to identify patterns in violations, driver demographics, and arrest likelihood.
	•	Dashboard: Built using Streamlit to visualize key metrics in real-time.

  Data Cleaning and Preprocessing ;
	•	Removed null and missing columns.
	•	Replaced NaN values with mean/mode where necessary.
	•	Standardized inconsistent country names and violation entries.
	•	Converted stop_time to datetime format for time-based analysis.

  SQL Analysis (Medium-Level Queries) ;
	1.	Night vs Day Arrests: Night-time stops had a higher arrest rate (~12%) compared to day (~7%).
	2.	Violation–Arrest Correlation: DUI and Speeding violations showed the highest arrest correlation.
	3.	Young Drivers (<25): Most common violation was Speeding.
	4.	Low-Risk Violations: Documentation issues rarely led to arrest/search.
	5.	Drug-Related Stops by Country: Country B had the highest drug-stop rate (≈15%).
	6.	Arrest Rate by Country & Violation: High arrest density for DUI and Reckless Driving in Country C.

  Feature Engineering :
	•	Derived features such as Time of Stop (Day/Night) and Age Category (Young/Adult/Senior) for improved trend analysis.

  Statistical Technique :

Used a Chi-Square Test of Independence to identify whether age, gender, or time of stop were significantly associated with arrests.
This test was selected because it’s suitable for categorical data relationships.

Findings (EDA Summary) :
	•	Age & Arrest: Younger males had a higher arrest probability.
	•	Violation Trends: Speeding and DUI dominate arrest categories.
	•	Time Effect: Night-time stops have greater search and arrest likelihood.
	•	Country Comparison: Urban countries had 3x higher drug-related stops than rural ones.

  Conclusion :

The SQL-Python integrated system improved visibility into traffic stop behavior and helped automate arrest pattern detection.
With clean data and indexed queries, query performance improved by over 40%.

Business Suggestions / Solutions :
	•	Deploy the dashboard across all regional check posts for real-time synchronization.
	•	Implement an alert system for flagged vehicles or repeat offenders.
	•	Train officers to input accurate data through a user-friendly Streamlit interface.
	•	Use analytics insights to schedule night patrols more efficiently based on arrest trends.

  Technical Stack :

Python Libraries: Pandas, SQLAlchemy, Streamlit
Database: MySQL / PostgreSQL
Key Techniques: Data Cleaning, EDA, SQL Joins, Window Functions, Streamlit Visualization

<img width="1440" height="900" alt="Screenshot 2025-10-17 at 1 35 20 PM" src="https://github.com/user-attachments/assets/fff1f41e-abf1-4e60-86a4-d4d7a40b1cd4" />

<img width="1440" height="900" alt="Screenshot 2025-10-17 at 1 35 43 PM" src="https://github.com/user-attachments/assets/89f8a00a-a102-46e1-875f-627c32d33078" />

Result

✅  Real-time monitoring and faster decision-making
✅  Automated detection of high-risk patterns
✅  Centralized digital records improving accountability


