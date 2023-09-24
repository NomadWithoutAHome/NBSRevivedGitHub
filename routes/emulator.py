from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

from main import templates

def init_app(app: FastAPI):
    @app.post('/emulator', response_class=HTMLResponse)
    def emulator(request: Request, game: str = Form(...), emucode: str = Form(...), rom: str = Form(...)):
        """
        Render the emulator.html template with the game data.

        Args:
            request (Request): The FastAPI request object.
            game (str): The game name.
            emucode (str): The emulator code.
            rom (str): The ROM file location.

        Returns:
            HTMLResponse: The rendered HTML template.
        """
        return templates.TemplateResponse('emulator.html',
                                          {"request": request, "game": game, "emucode": emucode, "rom": rom})
