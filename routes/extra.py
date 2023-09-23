from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json

from main import templates


def init_app(app: FastAPI):
    @app.get('/extra', response_class=HTMLResponse)
    def extra(request: Request):
        with open("static/data/games_data.json", "r") as json_file:
            games_data = json.load(json_file)
        return templates.TemplateResponse('extra.html',  {"request": request, "games_data": games_data })
