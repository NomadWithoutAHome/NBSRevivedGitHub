from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from helpers import load_json_data
#app = FastAPI(docs_url=None, redoc_url=None)
app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

episode_uuids = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=False,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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
import routes.extra
import routes.about
import routes.games
import routes.emulator

routes.index.init_app(app)
routes.seasons.init_app(app)
routes.season.init_app(app)
routes.search.init_app(app)
routes.video_url.init_app(app)
routes.video.init_app(app)
routes.extra.init_app(app)
routes.about.init_app(app)
routes.games.init_app(app)
routes.emulator.init_app(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
