from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse

from helpers import get_season_data, send_to_discord, track_session
from main import get_episode_data, templates


def init_app(app: FastAPI):  # Define init_app function

    def session_middleware(request: Request, call_next):
        # Your session management logic goes here, including creating and tracking the session
        # You can use the track_session function here if needed
        response = call_next(request)
        return response

    # Apply the session management middleware
    app.middleware("http")(session_middleware)

    @app.get('/season/{season_number}', response_class=HTMLResponse)
    def season(request: Request, season_number: int, seasons_data: dict = Depends(get_episode_data)):
        embed_data = track_session(request)
        # Call the send_to_discord function to send data to Discord
        send_to_discord(embed_data)
        season_data = get_season_data(season_number, seasons_data)
        if season_data:
            return templates.TemplateResponse('season.html', {"request": request, "season_data": season_data,
                                                              "season_number": season_number})
        raise HTTPException(status_code=404, detail="Season not found")

    @app.get('/dshorts', response_class=HTMLResponse)
    def disney_shorts(request: Request, disney_data: dict = Depends(get_episode_data)):
        """
        Render the disneyshorts.html template with DisneyShorts data.

        Args:
            request (Request): The FastAPI request object.
            seasons_data (dict): The episodes data.

        Returns:
            HTMLResponse: The rendered HTML template with DisneyShorts data.
        """
        embed_data = track_session(request)
        # Call the send_to_discord function to send data to Discord
        send_to_discord(embed_data)
        disney_shorts_data = disney_data.get("DisneyShorts", [])

        return templates.TemplateResponse('dshorts.html',
                                          {"request": request, "disney_shorts_data": disney_shorts_data})

    @app.get('/shorts', response_class=HTMLResponse)
    def shorts(request: Request, short_data: dict = Depends(get_episode_data)):
        """
        Render the disneyshorts.html template with DisneyShorts data.

        Args:
            request (Request): The FastAPI request object.
            seasons_data (dict): The episodes data.

        Returns:
            HTMLResponse: The rendered HTML template with DisneyShorts data.
            :param request:
            :param short_data:
        """
        embed_data = track_session(request)
        # Call the send_to_discord function to send data to Discord
        send_to_discord(embed_data)
        data = short_data.get("Shorts", [])

        return templates.TemplateResponse('shorts.html',
                                          {"request": request, "data": data})
