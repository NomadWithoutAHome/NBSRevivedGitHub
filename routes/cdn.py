from fastapi import FastAPI
from deta import Deta
from fastapi.responses import StreamingResponse

from helpers import get_content_type

# Initialize
deta = Deta('b0zC9ym1tt1d_LBi3rgiGXDyHpGeyX1k1qetPSsSd6Joj')

# This how to connect to or create a drive.
cdn_drive = deta.Drive("nobss_cdn")

def init_app(app: FastAPI):
    @app.get("/cdn/{file_path:path}")
    async def serve_static(file_path: str):
        # Determine the content type based on the file extension
        content_type = get_content_type(file_path)
        print(content_type)

        if content_type:
            headers = {"Content-Type": content_type}
        else:
            headers = {}

        try:
            # Retrieve and serve the file from Deta Drive
            file_data = cdn_drive.get(file_path)
            return StreamingResponse(file_data.iter_chunks(4096), media_type=headers["Content-Type"])
        except Exception as e:
            return {"error": str(e)}
