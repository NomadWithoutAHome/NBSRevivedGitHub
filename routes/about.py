from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from main import templates
def init_app(app: FastAPI):
    @app.get('/about', response_class=HTMLResponse)
    def extra(request: Request):
        """
        Render the about.html template.

        Args:
            request (Request): The FastAPI request object.

        Returns:
            HTMLResponse: The rendered HTML template.
        """
        return templates.TemplateResponse('about.html', {"request": request})
