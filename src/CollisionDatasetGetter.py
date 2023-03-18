import requests
import json

# Define the API endpoint with a $limit parameter
url = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?$limit=2000000"

# Send a GET request to the API
response = requests.get(url)

# Parse the JSON data
data = json.loads(response.text)

# Write the JSON data to a text file
with open("analysis/collision_data.json", "w") as f:
    counter = 0  # Initialize a counter variable
    for item in data:
        f.write(json.dumps(item) + "\n")
        counter += 1  # Increment the counter variable
    print(f"collision: Downloaded {counter} data items.")  # Print the total number of data items downloaded
