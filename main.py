import mimetypes
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.datastructures import Secret

from starlette.exceptions import HTTPException as StarletteHTTPException

from helpers import load_json_data

app = FastAPI(docs_url=None, redoc_url=None)

secret_key = Secret("aE6Nf2U1ldkwIjNzeCs6rBL4KPy7sGHS")

# Add the session middleware to the app
app.add_middleware(SessionMiddleware, secret_key=secret_key, session_cookie="fastapi-session")


def get_content_type(file_path: str) -> str:
    # Check for custom MIME type for .data files
    if file_path.endswith(".data"):
        return "application/x-7z-compressed"

    # Get the content type based on the file extension
    mime_type, _ = mimetypes.guess_type(file_path)
    print(mime_type)
    if mime_type:
        return mime_type
    else:
        return "application/octet-stream"  # Default MIME type




app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

episode_uuids = {}


template_mapping = {
    400: "400.html",  # Bad Request
    401: "401.html",  # Unauthorized
    403: "403.html",  # Forbidden
    404: "404.html",  # Not Found
    500: "500.html",  # Internal Server Error
}

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    # Get the appropriate template name for the given status code, or use '500.html' as a default
    template_name = template_mapping.get(exc.status_code, "500.html")

    # Create a TemplateResponse to render the HTML template
    response = templates.TemplateResponse(template_name, {"request": request}, status_code=exc.status_code)

    # Return the HTML response
    return response




@app.get("/robots.txt")
async def get_robots_txt():
    # Path to your robots.txt file
    robots_txt_path = "static/robots.txt"
    return FileResponse(robots_txt_path, media_type="text/plain")

@app.get("/sitemap.xml")
async def get_sitemap_xml():
    sitemap_patch = "static/sitemap.xml"
    return FileResponse(sitemap_patch, media_type="text/xml")

def get_episode_data():
    return load_json_data('static/data/episode_data.json')

def get_seasons_data():
    return load_json_data('static/data/season_data.json')

def get_episode_uuids():
    return episode_uuids

#generate_episode_uuids(get_episode_data(), episode_uuids)

import routes.index
import routes.seasons
import routes.season
import routes.search
import routes.video_url
import routes.video
import routes.music
import routes.about
import routes.games
import routes.emulator

routes.index.init_app(app)
routes.seasons.init_app(app)
routes.season.init_app(app)
routes.search.init_app(app)
routes.video_url.init_app(app)
routes.video.init_app(app)
routes.music.init_app(app)
routes.about.init_app(app)
routes.games.init_app(app)
routes.emulator.init_app(app)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
