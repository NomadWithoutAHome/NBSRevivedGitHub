import json
import uuid
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='/static')

def load_json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Load episode data from the JSON file
episode_data = load_json_data('static/Data/episode_data.json')

# Load season data from the JSON file
seasons_data = load_json_data('static/Data/season_data.json')

# Define a dictionary to store UUIDs associated with episodes
episode_uuids = {}

# Function to generate and store UUIDs for episodes
def generate_episode_uuids():
    for season_name, season_episodes in episode_data.items():
        for episode in season_episodes:
            episode_uuid = str(uuid.uuid4())
            episode_uuids[episode_uuid] = episode
            episode['uuid'] = episode_uuid

# Initialize UUIDs when the application starts
generate_episode_uuids()

# Function to get season data by season number
def get_season_data(season_number):
    season_name = f"Season {season_number}"
    return episode_data.get(season_name, None)

# Function to get season number by episode title
def get_season_number(episode_title):
    for season_name, season_episodes in episode_data.items():
        for episode in season_episodes:
            if episode['Episode Title'] == episode_title:
                return int(season_name.split()[1])
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

# Define the video page
@app.route('/video/<uuid:video_uuid>')
def video(video_uuid):
    video_uuid_str = str(video_uuid)
    episode = episode_uuids.get(video_uuid_str)
    if episode and 'Episode_vidsrc' in episode:
        return render_template('video.html', video_url=episode['Episode_vidsrc'])
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
        query_lower = query.lower()
        search_results = []

        for season_name, season_episodes in episode_data.items():
            for episode in season_episodes:
                if query_lower in episode['Episode Title'].lower():
                    episode_copy = episode.copy()
                    episode_copy['Season'] = int(season_name.split()[1])
                    search_results.append(episode_copy)

        return render_template('search_results.html', query=query, results=search_results)
    else:
        return redirect(url_for('index'))

@app.route('/seasons')
def seasons():
    return render_template('seasons.html', seasons_data=seasons_data)

if __name__ == '__main__':
    app.run(debug=True)
