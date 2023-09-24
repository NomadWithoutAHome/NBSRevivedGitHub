from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json
import re

from main import templates


def format_game_id(game_name):
    """Custom filter"""
    return re.sub('[^A-Za-z0-9_]+', '', game_name.replace(" ", "_"))


# Add the custom filter to the Jinja2 environment
templates.env.filters['format_game_id'] = format_game_id


def init_app(app: FastAPI):
    @app.get('/extra', response_class=HTMLResponse)
    def extra(request: Request):
        with open("static/data/games_data.json", "r") as json_file:
            games_data = json.load(json_file)
        return templates.TemplateResponse('extra.html', {"request": request, "games_data": games_data})
