from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from main import templates
def init_app(app: FastAPI):
    @app.get('/emulator', response_class=HTMLResponse)
    def emulator(request: Request):
        """
        Render the about.html template.

        Args:
            request (Request): The FastAPI request object.

        Returns:
            HTMLResponse: The rendered HTML template.
        """
        return templates.TemplateResponse('emulator.html', {"request": request})
