import pandas as pd

# Read CSV file into a pandas DataFrame
df = pd.read_csv('weather_data_cleaned.csv')

# Convert DataFrame to JSON format and save to a file
df.to_json('weather_data.json', orient='records')