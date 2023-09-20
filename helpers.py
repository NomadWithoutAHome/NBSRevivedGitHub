# helpers.py
import json
from uuid import uuid4

import requests


# Load JSON data from a file.
def load_json_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

# Generate and store UUIDs for episodes.
def generate_episode_uuids(episode_data, episode_uuids):
    for season_name, season_episodes in episode_data.items():
        for episode in season_episodes:
            episode_uuid = str(uuid4())
            episode_uuids[episode_uuid] = episode
            episode['uuid'] = episode_uuid

    # Save the updated episode_data back to the JSON file
    with open('static/Data/episode_data.json', 'w') as file:
        json.dump(episode_data, file, indent=4)

# Get an episode title by its UUID.
def get_episode_title_by_uuid(uuid_str, episode_data):
    for season_name, season_episodes in episode_data.items():
        for episode in season_episodes:
            if episode.get('uuid') == uuid_str:
                return episode.get('title')
    return None

# Get the UUID of a video by providing its title.
def get_video_url_by_title(episode_title, episode_data):
    for season_name, season_episodes in episode_data.items():
        for episode in season_episodes:
            if episode.get('Episode Title') == episode_title:
                return episode.get('uuid')
    return None

# Get an episode by its UUID.
def get_episode_by_uuid(uuid_str, episode_data):
    for season_name, season_episodes in episode_data.items():
        for episode in season_episodes:
            if episode.get('uuid') == uuid_str:
                return episode
    return None

# Get season data by season number.
def get_season_by_number(season_number, seasons_data):
    for season in seasons_data:
        if season.get('Season') == season_number:
            return season
    return None

# Get episode data for a specific season number.
def get_season_data(season_number, episode_data):
    season_name = f"Season {season_number}"
    return episode_data.get(season_name, None)


def extract_season_number(season_name):
    try:
        season_number = season_name.split()[-1]
        return int(season_number)
    except (IndexError, ValueError):
        return None

# Get a random Simpsons quote from an external API.
def get_random_simpsons_quote():
    try:
        response = requests.get('https://thesimpsonsquoteapi.glitch.me/quotes')
        if response.status_code == 200:
            quote_data = response.json()[0]
            return quote_data['quote'], quote_data['character'], quote_data['image']
        else:
            return "Failed to fetch quote", "Unknown", None
    except Exception as e:
        print(f"Error fetching Simpsons quote: {e}")
        return "Failed to fetch quote", "Unknown", None