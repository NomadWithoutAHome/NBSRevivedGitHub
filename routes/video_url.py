from fastapi import HTTPException, FastAPI, Depends
from typing import Dict, Union
from helpers import get_video_url_by_title
from main import get_episode_data

def init_app(app: FastAPI):  # Add this line
    @app.get('/video_url/{episode_title}', response_model=Dict[str, Union[str, int]])
    def video_url(episode_title: str, episode_data: dict = Depends(get_episode_data)):
        """
        Return the video URL based on the provided episode title.

        Args:
            episode_title (str): The title of the episode.

        Returns:
            dict: A dictionary containing the video URL or an error message.
        """
        episode_uuid = get_video_url_by_title(episode_title, episode_data)
        if episode_uuid:
            return {"uuid": episode_uuid}
        raise HTTPException(status_code=404, detail="Video not found")