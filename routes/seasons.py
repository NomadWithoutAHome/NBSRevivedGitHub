from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse

from main import get_seasons_data, templates  # Assuming get_seasons_data is defined in main.py


def init_app(app: FastAPI):  # Define init_app function
    @app.get('/seasons', response_class=HTMLResponse)
    def seasons(request: Request,  seasons_data: dict = Depends(get_seasons_data)):  # Add this line

        """
        Render the seasons.html template with season data.

        Args:
            request (Request): The FastAPI request object.
            seasons_data (dict): The seasons data.  # Add this line

        Returns:
            HTMLResponse: The rendered HTML template.
        """
        return templates.TemplateResponse('seasons.html', {"request": request, "seasons_data": seasons_data})