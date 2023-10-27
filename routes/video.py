from uuid import UUID

from fastapi import FastAPI, Request, Response, HTTPException, Depends  # Import Depends
from fastapi.responses import HTMLResponse

from helpers import get_episode_by_uuid, send_to_discord, track_session , get_session_id
from main import get_episode_data, templates  # Import get_episode_data and templates from main.py


def init_app(app: FastAPI):  # Define init_app function

    def session_middleware(request: Request, call_next):
        # Your session management logic goes here, including creating and tracking the session
        # You can use the track_session function here if needed
        response = call_next(request)
        return response

    # Apply the session management middleware
    app.middleware("http")(session_middleware)
    @app.get('/video/{video_uuid}', response_class=HTMLResponse)
    def video(request: Request, response: Response, video_uuid: UUID, session_id: str = Depends(get_session_id), episode_data: dict = Depends(get_episode_data)):  # Add this line
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
        embed_data = track_session(request)
        # Call the send_to_discord function to send data to Discord
        send_to_discord(embed_data)
        video_uuid_str = str(video_uuid)
        episode = get_episode_by_uuid(video_uuid_str, episode_data)  # Use get_episode_by_uuid
        if episode and 'Episode_vidsrc' in episode:
            # Set the "last_watched_episode" cookie with the UUID of the current episode.
            request.session['last_episode'] = episode['Episode Title']
            request.session['last_episode_uuid'] = video_uuid_str
            response.set_cookie(key="last_watched_episode", value=video_uuid_str)
            return templates.TemplateResponse('video.html', {"request": request, "video_url": episode['Episode_vidsrc']})
        raise HTTPException(status_code=404, detail="Video not found")
