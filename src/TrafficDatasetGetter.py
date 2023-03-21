import requests
import json

# Define the API endpoint with a $limit parameter
url = "https://data.cityofnewyork.us/resource/7ym2-wayt.json?$limit=28000000"

# Send a GET request to the API
response = requests.get(url, stream=True)

# Write the JSON data to a text file
with open("traffic_data.txt", "w") as f:
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line)
                f.write(json.dumps(data) + "\n")
            except json.decoder.JSONDecodeError:
                pass

print("traffic: Download complete.")  # Print a message indicating that the download is complete
