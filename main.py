import json
import re
from typing import Optional
from uuid import UUID, uuid4

import requests
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fuzzywuzzy import fuzz


# Define the load_json_data function to load JSON data from a file
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


# Define the get_random_simpsons_quote function
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


# Define a function to extract the numeric season value from a season name
def extract_season_number(season_name):
    try:
        # Split the season name by space and get the last part, which is the season number
        season_number = season_name.split()[-1]
        # Convert it to an integer
        return int(season_number)
    except (IndexError, ValueError):
        return None

app = FastAPI()

# Configure Jinja2Templates to load templates from a directory named "templates"
templates = Jinja2Templates(directory="templates")

# Serve static files from a directory named "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load episode data from the JSON file
episode_data = load_json_data('static/Data/episode_data.json')

# Load season data from the JSON file
seasons_data = load_json_data('static/Data/season_data.json')

# Initialize a dictionary to store episode UUIDs
episode_uuids = {}


# Define a function to generate and store UUIDs for episodes
def generate_episode_uuids():
    for season_name, season_episodes in episode_data.items():
        for episode in season_episodes:
            episode_uuid = str(uuid4())  # Generate a new UUID for each episode
            episode_uuids[episode_uuid] = episode
            episode['uuid'] = episode_uuid


# Initialize UUIDs when the application starts
generate_episode_uuids()


# Define a function to get an episode by its UUID
def get_episode_by_uuid(uuid_str):
    for season_name, season_episodes in episode_data.items():
        for episode in season_episodes:
            if episode.get('uuid') == uuid_str:
                return episode
    return None


# Define a function to get season data by season number
def get_season_by_number(season_number):
    for season in seasons_data:
        if season.get('Season') == season_number:
            return season
    return None

def get_season_data(season_number):
    season_name = f"Season {season_number}"
    return episode_data.get(season_name, None)




# Route handler to render the video.html template based on the provided code
@app.get('/video/{video_uuid}', response_class=HTMLResponse)
def video(request: Request, video_uuid: UUID):
    video_uuid_str = str(video_uuid)
    episode = episode_uuids.get(video_uuid_str)
    if episode and 'Episode_vidsrc' in episode:
        return templates.TemplateResponse('video.html', {"request": request, "video_url": episode['Episode_vidsrc']})
    return "Video not found", 404


# Route handler to get an episode by UUID
@app.get('/episode/{uuid}', response_model=dict)
def get_episode(uuid: UUID):
    episode_uuid_str = str(uuid)
    episode = get_episode_by_uuid(episode_uuid_str)
    if episode:
        return episode
    raise HTTPException(status_code=404, detail="Episode not found")

# Route handler for the index (home) page
@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    # Get a random Simpsons quote
    quote, character, image = get_random_simpsons_quote()

    # Render the index.html template with the quote data
    return templates.TemplateResponse('index.html',
                                      {"request": request, "quote": quote, "character": character, "image": image})

# Route handler for the seasons page
@app.get('/seasons', response_class=HTMLResponse)
def seasons(request: Request):
    return templates.TemplateResponse('seasons.html', {"request": request, "seasons_data": seasons_data})

# Route handler for the season page
@app.get('/season/{season_number}', response_class=HTMLResponse)
def season(request: Request, season_number: int):
    season_data = get_season_data(season_number)
    if season_data:
        return templates.TemplateResponse('season.html', {"request": request, "season_data": season_data, "season_number": season_number})
    raise HTTPException(status_code=404, detail="Season not found")

@app.get('/search', response_class=HTMLResponse)
def search(
    request: Request,
    query: str = Query(..., title="Search Query", description="Enter the episode title to search for."),
    season: int = Query(None, title="Season Number", description="Filter by season number."),
    fuzzy: bool = Query(False, title="Fuzzy Search", description="Enable fuzzy searching."),
    partial: bool = Query(False, title="Partial Match", description="Enable partial matching."),
):
    # Ensure the query is not empty
    if not query:
        return "Please enter a search query."

    matched_episodes = []

    for season_name, episodes in episode_data.items():
        # Check if the season filter is provided and matches the current season_name
        if (season is None or season == extract_season_number(season_name)):
            for episode in episodes:
                episode_title = episode['Episode Title'].lower()

                if fuzzy:
                    # Use fuzzywuzzy to perform fuzzy searching
                    from fuzzywuzzy import fuzz
                    fuzz_ratio = fuzz.ratio(query.lower(), episode_title)
                    if fuzz_ratio >= 90:  # Adjust the threshold as needed
                        matched_episodes.append(episode)
                elif partial:
                    # Perform partial matching
                    if query.lower() in episode_title:
                        matched_episodes.append(episode)
                else:
                    # Use regular expressions to match whole words
                    pattern = r'\b{}\b'.format(re.escape(query.lower()))
                    if re.search(pattern, episode_title):
                        matched_episodes.append(episode)

    return templates.TemplateResponse(
        'search_results.html',
        {"request": request, "query": query, "results": matched_episodes},
    )

#function to get video url by episode title then return its uuid ex: d8cbe487-6e66-446b-a3db-8a6e1b05492c
def get_video_url_by_title(episode_title):
    for season_name, season_episodes in episode_data.items():
        for episode in season_episodes:
            if episode.get('Episode Title') == episode_title:
                return episode.get('uuid')
    return None

test = get_video_url_by_title("Simpsons Roasting on an Open Fire")
print(test)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
