from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse

from main import get_seasons_data, templates

from helpers import send_to_discord, track_session , generate_custom_user_id

def init_app(app: FastAPI):
    # Define a middleware function to handle session management
    def session_middleware(request: Request, call_next):
        # Your session management logic goes here, including creating and tracking the session
        # You can use the track_session function here if needed
        response = call_next(request)
        return response

    # Apply the session management middleware
    app.middleware("http")(session_middleware)

    @app.get('/seasons', response_class=HTMLResponse)
    def seasons(request: Request, seasons_data: dict = Depends(get_seasons_data)):
        # request.session['session_id'] = generate_custom_user_id()

        # Call the track_session function to handle session tracking
        embed_data = track_session(request)
        # Call the send_to_discord function to send data to Discord
        send_to_discord(embed_data)

        return templates.TemplateResponse('seasons.html', {"request": request, "seasons_data": seasons_data})
