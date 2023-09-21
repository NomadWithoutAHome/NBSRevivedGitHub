from fastapi import FastAPI, Request, Response, HTTPException, Cookie, Depends  # Import Depends
from fastapi.responses import HTMLResponse
from uuid import UUID
from helpers import get_episode_by_uuid  # Import get_episode_by_uuid
from main import get_episode_data, templates  # Import get_episode_data and templates from main.py

def init_app(app: FastAPI):  # Define init_app function
    @app.get('/video/{video_uuid}', response_class=HTMLResponse)
    def video(request: Request, response: Response, video_uuid: UUID, episode_data: dict = Depends(get_episode_data)):  # Add this line
        """
        Render the video.html template based on the provided UUID and set the last-watched episode cookie.

        Args:
            request (Request): The FastAPI request object.
            response (Response): The FastAPI response object.
            video_uuid (UUID): The UUID of the video.
            episode_data (dict): The episode data.  # Add this line

        Returns:
            HTMLResponse or str: The rendered HTML template or an error message.
        """
        video_uuid_str = str(video_uuid)
        print(video_uuid_str)
        episode = get_episode_by_uuid(video_uuid_str, episode_data)  # Use get_episode_by_uuid
        if episode and 'Episode_vidsrc' in episode:
            # Set the "last_watched_episode" cookie with the UUID of the current episode.
            response.set_cookie(key="last_watched_episode", value=video_uuid_str)
            return templates.TemplateResponse('video.html', {"request": request, "video_url": episode['Episode_vidsrc']})
        raise HTTPException(status_code=404, detail="Video not found")
