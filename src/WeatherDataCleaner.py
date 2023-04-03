import pandas as pd

# Load the weather data from the CSV file
data = pd.read_csv('weather_data.csv')

# Fill missing values with zeros
data = data.fillna(0)

# Save the cleaned data to a new CSV file
data.to_csv('weather_data_cleaned.csv', index=False)
