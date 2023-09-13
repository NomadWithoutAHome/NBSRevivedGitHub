import json
import uuid

import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Load episode data from the JSON file
with open('episode_data.json', 'r') as file:
    episode_data = json.load(file)

# Define a dictionary to store UUIDs associated with episodes
episode_uuids = {}


def get_season_data(season_number):
    season_name = f"Season {season_number}"
    if season_name in episode_data:
        # Generate a UUID for each video and add it to the data
        for episode in episode_data[season_name]:
            episode_uuid = str(uuid.uuid4())
            episode_uuids[episode_uuid] = episode  # Store the episode data with the UUID as the key
            episode['uuid'] = episode_uuid  # Add the UUID to the episode data
        return episode_data[season_name]
    else:
        return None  # Season not found


def get_season_number(episode_title):
    for season_name, season_data in episode_data.items():
        for episode in season_data:
            if episode['Episode Title'] == episode_title:
                return season_name.split()[1]
    return None



# Function to fetch a random quote from The Simpsons API
def get_random_simpsons_quote():
    response = requests.get('https://thesimpsonsquoteapi.glitch.me/quotes')
    if response.status_code == 200:
        quote_data = response.json()[0]
        return quote_data['quote'], quote_data['character'], quote_data['image']
    else:
        return "Failed to fetch quote", "Unknown"


# Define the index page
@app.route('/')
def index():
    quote, character, image = get_random_simpsons_quote()
    return render_template('index.html', quote=quote, character=character, image=image)


@app.route('/video/<uuid:video_uuid>')
def video(video_uuid):
    print(episode_uuids)
    # Convert the UUID to a string
    video_uuid_str = str(video_uuid)

    # Check if the UUID exists in the episode_uuids mapping
    if video_uuid_str in episode_uuids:
        episode = episode_uuids[video_uuid_str]
        video_url = episode.get('Episode_vidsrc')
        if video_url:
            return render_template('video.html', video_url=video_url)

    return "Video not found", 404



# Define the season page
@app.route('/season/<int:season_number>')
def season(season_number):
    season_data = get_season_data(season_number)
    if season_data is not None:
        return render_template('season.html', season_data=season_data, season_number=season_number)
    else:
        return "Season not found", 404


# Define the search route
@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        # Filter the episode data by title
        search_results = [episode for season in episode_data.values() for episode in season if query.lower() in episode['Episode Title'].lower()]

        # Add the season number to each search result
        for episode in search_results:
            episode['Season'] = get_season_number(episode['Episode Title'])
            episode['Episode Number'] = f"{episode['Season']}x{episode['Episode Number']}"

        return render_template('search_results.html', query=query, results=search_results)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=5000)
