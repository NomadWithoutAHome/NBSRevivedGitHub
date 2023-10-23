from fastapi import Request
from starlette.middleware.sessions import SessionMiddleware


def create_session_middleware(app):
    return SessionMiddleware(app, secret_key="your_secret_key")

def get_session(request: Request):
    return request.session

def track_session(request: Request):
    user_ip = request.client.host
    session = get_session(request)
    session_id = session.get("session_id")
    visited_page = request.url.path

    discord_embed_data = {
        "title": "User Session Tracking",
        "description": f"User IP: {user_ip}\nSession ID: {session_id}\nVisited Page: {visited_page}",
    }

    return discord_embed_data