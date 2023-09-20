from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from helpers import get_season_data
from main import get_episode_data, templates


def init_app(app: FastAPI):  # Define init_app function
    @app.get('/season/{season_number}', response_class=HTMLResponse)
    def season(request: Request, season_number: int, seasons_data: dict = Depends(get_episode_data)):
        """
        Render the season.html template with season data for a specific season number.

        Args:
            request (Request): The FastAPI request object.
            season_number (int): The season number.

        Returns:
            HTMLResponse or HTTPException: The rendered HTML template or a 404 error.
            :param seasons_data:
        """
        season_data = get_season_data(season_number, seasons_data)
        if season_data:
            return templates.TemplateResponse('season.html', {"request": request, "season_data": season_data,
                                                              "season_number": season_number})
        raise HTTPException(status_code=404, detail="Season not found")
