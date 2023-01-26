import os
import requests
import json

tmdb_key = os.getenv("TMDB_KEY")
min_id = 0
max_id = 1000000

# Exit if the environment variables are not set
if "TMDB_KEY" not in os.environ:
    raise Exception("Please set TMDB_KEY with your v3 API key")

# Create output file
print("Creating output file")
with open("output.json", "w+") as f:

    # Call TMDB API
    for id in range(min_id, max_id):
        url = f"https://api.themoviedb.org/3/movie/{id}?api_key={tmdb_key}&language=cs"
        response = requests.get(url)
        if response.status_code == 200:
           if json.loads(response.text)["overview"] != "":
               print(f"ID: {id} - Status: {response.status_code} - Title: {json.loads(response.text)['title']}")
               f.write(response.text + "\n")
        else:
            print(f"ID: {id} - Status: {response.status_code}")