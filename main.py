from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from helpers import load_json_data, generate_episode_uuids

app = FastAPI(docs_url=None, redoc_url=None)

# Mount a static directory for serving CSS, JS, and other static files.
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

episode_uuids = {}

def get_episode_data():
    return load_json_data('static/data/episode_data.json')

def get_seasons_data():
    return load_json_data('static/data/season_data.json')

def get_episode_uuids():
    return episode_uuids

#generate_episode_uuids(get_episode_data(), episode_uuids)

# Import your route files and initialize them.
import routes.index
import routes.seasons
import routes.season
import routes.search
import routes.video_url
import routes.video

routes.index.init_app(app)
routes.seasons.init_app(app)
routes.season.init_app(app)
routes.search.init_app(app)
routes.video_url.init_app(app)
routes.video.init_app(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
