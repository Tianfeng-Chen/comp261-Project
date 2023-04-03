from datetime import datetime
from meteostat import Point, Daily

# Set time period
start = datetime(2014, 5, 1)
end = datetime(2023, 3, 31)

# Create Point for New York City
nyc = Point(40.7128, -74.0060)

# Get daily data for New York City
data = Daily(nyc, start, end)
data = data.fetch()

data['date'] = data.index.strftime('%Y-%m-%d')

# Save data to a CSV file
data.to_csv('weather_data.csv', index=False)


