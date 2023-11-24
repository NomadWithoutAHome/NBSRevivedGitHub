from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.responses import HTMLResponse
from helpers import get_episode_by_uuid, send_to_discord, track_session, get_session_id, get_next_episode, get_current_season
from main import get_episode_data, templates
from uuid import UUID

def init_app(app: FastAPI):
    def session_middleware(request: Request, call_next):
        response = call_next(request)
        return response

    app.middleware("http")(session_middleware)

    @app.get('/video/{video_uuid}', response_class=HTMLResponse)
    def video(
            request: Request,
            response: Response,
            video_uuid: UUID,
            session_id: str = Depends(get_session_id),
            episode_data: dict = Depends(get_episode_data)
    ):
        embed_data = track_session(request)
        send_to_discord(embed_data)

        video_uuid_str = str(video_uuid)
        episode = get_episode_by_uuid(video_uuid_str, episode_data)

        if episode and 'Episode_vidsrc' in episode:
            current_season = get_current_season(episode, episode_data)

            if current_season:
                current_episode_number = int(episode['Episode Number'])
                next_episode = get_next_episode(current_season, current_episode_number, episode_data)

                return templates.TemplateResponse(
                    'video.html',
                    {"request": request, "video_url": episode['Episode_vidsrc'], "next_episode": next_episode}
                )

            # Handle the case when the current season is not found
            raise HTTPException(status_code=500, detail="Current season not found")

        # Handle the case when the video is not found
        raise HTTPException(status_code=404, detail="Video not found")
