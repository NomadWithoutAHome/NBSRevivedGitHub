import re

from fastapi import FastAPI, Request, Query, Depends
from fastapi.responses import HTMLResponse
from fuzzywuzzy import fuzz  # Assuming you have installed the fuzzywuzzy library

from helpers import extract_season_number, track_session, send_to_discord  # Assuming you have defined the extract_season_number, track_session, and send_to_discord functions
from main import get_episode_data, templates  # Assuming get_episode_data is defined in main.py


def init_app(app: FastAPI):  # Define init_app function

    def session_middleware(request: Request, call_next):
        # Your session management logic goes here, including creating and tracking the session
        # You can use the track_session function here if needed
        response = call_next(request)
        return response

    # Apply the session management middleware
    app.middleware("http")(session_middleware)
    @app.get('/search', response_class=HTMLResponse)
    def search(
            request: Request,
            episode_data: dict = Depends(get_episode_data),  # Add this line
            query: str = Query(..., title="Search Query", description="Enter the episode title to search for."),
            season: int = Query(None, title="Season Number", description="Filter by season number."),
            fuzzy: bool = Query(False, title="Fuzzy Search", description="Enable fuzzy searching."),
            partial: bool = Query(False, title="Partial Match", description="Enable partial matching."),
    ):

        embed_data = track_session(request)
        # Call the send_to_discord function to send data to Discord
        send_to_discord(embed_data)
        """
        Handle episode searches based on query parameters.

        Args:
            request (Request): The FastAPI request object.
            episode_data (dict): The episode data.  # Add this line
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
            {"request": request, "query": query, "results": matched_episodes, "season": season},
        )
