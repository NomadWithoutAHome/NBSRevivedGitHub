from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from main import templates

class Game(BaseModel):
    game: str
    emucode: str
    rom: str

def init_app(app: FastAPI):
    @app.post('/emulator', response_class=HTMLResponse)
    def emulator(request: Request, game: Game):
        """
        Render the emulator.html template with the game data.

        Args:
            request (Request): The FastAPI request object.
            game (Game): The game data.

        Returns:
            HTMLResponse: The rendered HTML template.
        """
        return templates.TemplateResponse('emulator.html', {"request": request, "game": game})
