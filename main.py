import json
import re
from typing import Dict, Union, List
from uuid import UUID, uuid4

import requests
from fastapi import FastAPI, Request, HTTPException, Query, Cookie
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fuzzywuzzy import fuzz

from deta import Deta
from pydantic import BaseModel

# Initialize Deta
deta = Deta("b0zC9ym1tt1d_cE68J9dW9L6xwaf9GQRgxoHjW4kF3iBX")
# Initialize Deta Base
db = deta.Base("comments")

def load_json_data(filename):
    """
    Load JSON data from a file.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data as a Python dictionary or None if there was an error.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None



def get_random_simpsons_quote():
    """
    Get a random Simpsons quote from an external API.

    Returns:
        tuple: A tuple containing the quote, character, and image URL.
    """
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


def extract_season_number(season_name):
    """
    Extract the numeric season value from a season name.

    Args:
        season_name (str): The name of the season.

    Returns:
        int or None: The extracted season number as an integer, or None if it couldn't be extracted.
    """
    try:
        season_number = season_name.split()[-1]
        return int(season_number)
    except (IndexError, ValueError):
        return None


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

episode_data = load_json_data('static/Data/episode_data.json')

seasons_data = load_json_data('static/Data/season_data.json')

episode_uuids = {}

class Comment(BaseModel):
    episode_uuid: str
    username: str
    comment: str

@app.post('/comment', response_model=Comment)
def create_comment(comment: Comment):
    new_comment = db.put(comment.dict())
    return new_comment

@app.get('/comments/{episode_uuid}', response_model=List[Comment])
def get_comments(episode_uuid: str):
    comments = db.fetch({"episode_uuid": episode_uuid})
    return list(comments)


def generate_episode_uuids():
    """
    Generate and store UUIDs for episodes.
    """
    for season_name, season_episodes in episode_data.items():
        for episode in season_episodes:
            episode_uuid = str(uuid4())
            episode_uuids[episode_uuid] = episode
            episode['uuid'] = episode_uuid


generate_episode_uuids()


def get_episode_by_uuid(uuid_str):
    """
    Get an episode by its UUID.

    Args:
        uuid_str (str): The UUID of the episode.

    Returns:
        dict or None: The episode data as a dictionary or None if not found.
    """
    for season_name, season_episodes in episode_data.items():
        for episode in season_episodes:
            if episode.get('uuid') == uuid_str:
                return episode
    return None


def get_season_by_number(season_number):
    """
    Get season data by season number.

    Args:
        season_number (int): The season number.

    Returns:
        dict or None: The season data as a dictionary or None if not found.
    """
    for season in seasons_data:
        if season.get('Season') == season_number:
            return season
    return None


def get_season_data(season_number):
    """
    Get episode data for a specific season number.

    Args:
        season_number (int): The season number.

    Returns:
        dict or None: The episode data for the specified season or None if not found.
    """
    season_name = f"Season {season_number}"
    return episode_data.get(season_name, None)


from fastapi import Response

@app.get('/video/{video_uuid}', response_class=HTMLResponse)
def video(request: Request, response: Response, video_uuid: UUID):
    """
    Render the video.html template based on the provided UUID and set the last-watched episode cookie.

    Args:
        request (Request): The FastAPI request object.
        response (Response): The FastAPI response object.
        video_uuid (UUID): The UUID of the video.

    Returns:
        HTMLResponse or str: The rendered HTML template or an error message.
    """
    video_uuid_str = str(video_uuid)
    episode = episode_uuids.get(video_uuid_str)
    if episode and 'Episode_vidsrc' in episode:
        # Set the "last_watched_episode" cookie with the UUID of the current episode.
        response.set_cookie(key="last_watched_episode", value=video_uuid_str)
        return templates.TemplateResponse('video.html', {"request": request, "video_url": episode['Episode_vidsrc']})
    return "Video not found", 404



@app.get('/episode/{uuid}', response_model=dict)
def get_episode(uuid: UUID):
    """
    Get an episode by its UUID.

    Args:
        uuid (UUID): The UUID of the episode.

    Returns:
        dict: The episode data as a dictionary.

    Raises:
        HTTPException: If the episode is not found, returns a 404 error.
    """
    episode_uuid_str = str(uuid)
    episode = get_episode_by_uuid(episode_uuid_str)
    if episode:
        return episode
    raise HTTPException(status_code=404, detail="Episode not found")


@app.get('/', response_class=HTMLResponse)
def index(request: Request, last_watched_episode: str = Cookie(default=None)):
    """
    Render the index.html template with a random Simpsons quote and last watched episode.

    Args:
        request (Request): The FastAPI request object.
        last_watched_episode (str, optional): The last watched episode stored in a cookie.

    Returns:
        HTMLResponse: The rendered HTML template.
    """
    # Retrieve the last watched episode data based on the stored cookie value (e.g., episode UUID).
    last_watched_episode_data = get_episode_by_uuid(last_watched_episode)

    # Get a random Simpsons quote.
    quote, character, image = get_random_simpsons_quote()

    return templates.TemplateResponse('index.html',
                                      {"request": request,
                                       "quote": quote,
                                       "character": character,
                                       "image": image,
                                       "last_watched_episode": last_watched_episode_data})


@app.get('/seasons', response_class=HTMLResponse)
def seasons(request: Request):
    """
    Render the seasons.html template with season data.

    Args:
        request (Request): The FastAPI request object.

    Returns:
        HTMLResponse: The rendered HTML template.
    """
    return templates.TemplateResponse('seasons.html', {"request": request, "seasons_data": seasons_data})


@app.get('/season/{season_number}', response_class=HTMLResponse)
def season(request: Request, season_number: int):
    """
    Render the season.html template with season data for a specific season number.

    Args:
        request (Request): The FastAPI request object.
        season_number (int): The season number.

    Returns:
        HTMLResponse or HTTPException: The rendered HTML template or a 404 error.
    """
    season_data = get_season_data(season_number)
    if season_data:
        return templates.TemplateResponse('season.html', {"request": request, "season_data": season_data,
                                                          "season_number": season_number})
    raise HTTPException(status_code=404, detail="Season not found")


@app.get('/search', response_class=HTMLResponse)
def search(
        request: Request,
        query: str = Query(..., title="Search Query", description="Enter the episode title to search for."),
        season: int = Query(None, title="Season Number", description="Filter by season number."),
        fuzzy: bool = Query(False, title="Fuzzy Search", description="Enable fuzzy searching."),
        partial: bool = Query(False, title="Partial Match", description="Enable partial matching."),
):
    """
    Handle episode searches based on query parameters.

    Args:
        request (Request): The FastAPI request object.
        query (str): The search query (episode title).
        season (int, optional): The season number to filter by.
        fuzzy (bool): Enable fuzzy searching.
        partial (bool): Enable partial matching.

    Returns:
        HTMLResponse: The rendered HTML template with search results.
    """
    if not query:
        return "Please enter a search query."

    matched_episodes = []

    for season_name, episodes in episode_data.items():
        if (season is None or season == extract_season_number(season_name)):
            for episode in episodes:
                episode_title = episode['Episode Title'].lower()

                if fuzzy:
                    fuzz_ratio = fuzz.ratio(query.lower(), episode_title)
                    if fuzz_ratio >= 90:
                        matched_episodes.append(episode)
                elif partial:
                    if query.lower() in episode_title:
                        matched_episodes.append(episode)
                else:
                    pattern = r'\b{}\b'.format(re.escape(query.lower()))
                    if re.search(pattern, episode_title):
                        matched_episodes.append(episode)

    return templates.TemplateResponse(
        'search_results.html',
        {"request": request, "query": query, "results": matched_episodes},
    )

#route that returns the video url for a given episode title and return json
@app.get('/video_url/{episode_title}', response_model=Dict[str, Union[str, int]])
def video_url(episode_title: str):
    """
    Return the video URL based on the provided episode title.

    Args:
        episode_title (str): The title of the episode.

    Returns:
        dict: A dictionary containing the video URL or an error message.
    """
    episode_uuid = get_video_url_by_title(episode_title)
    if episode_uuid:
        return {"uuid": episode_uuid}
    raise HTTPException(status_code=404, detail="Video not found")

def get_video_url_by_title(episode_title):
    """
    Get the UUID of a video by providing its title.

    Args:
        episode_title (str): The title of the episode.

    Returns:
        str or None: The UUID of the video or None if not found.
    """
    for season_name, season_episodes in episode_data.items():
        for episode in season_episodes:
            if episode.get('Episode Title') == episode_title:
                return episode.get('uuid')
    return None


#test = get_video_url_by_title("Simpsons Roasting on an Open Fire")
#print(test)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
