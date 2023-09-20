from fastapi import FastAPI, Request, Cookie, Depends
from fastapi.responses import HTMLResponse
from helpers import get_episode_by_uuid, get_random_simpsons_quote
from main import get_episode_data, templates


def init_app(app: FastAPI):  # Define init_app function
    @app.get('/', response_class=HTMLResponse)
    def index(
        request: Request,
        last_watched_episode: str = Cookie(default=None),
        episode_data: dict = Depends(get_episode_data)  # Add this line
    ):
        """
        Render the index.html template with a random Simpsons quote and last watched episode.

        Args:
            request (Request): The FastAPI request object.
            last_watched_episode (str, optional): The last watched episode stored in a cookie.
            episode_data (dict): The episode data.  # Add this line

        Returns:
            HTMLResponse: The rendered HTML template.
        """
        # Retrieve the last watched episode data based on the stored cookie value (e.g., episode UUID).
        last_watched_episode_data = get_episode_by_uuid(last_watched_episode, episode_data)  # Modify this line

        # Get a random Simpsons quote.
        quote, character, image = get_random_simpsons_quote()

        return templates.TemplateResponse('index.html',
                                          {"request": request,
                                           "quote": quote,
                                           "character": character,
                                           "image": image,
                                           "last_watched_episode": last_watched_episode_data})

