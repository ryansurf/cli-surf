"""
FastAPI Server!
"""

import io
import logging
from contextlib import redirect_stdout
from pathlib import Path

import debugpy
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

from src import cli
from src.settings import ServerSettings

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "src" / "templates"
CLI_PATH = BASE_DIR / "src" / "cli.py"

surf = cli.SurfReport()

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def create_app(env):
    """
    Application factory function
    """
    app = FastAPI()

    # define which "origins" (frontend urls) can talk to this api
    origins = ["http://localhost:8501", "http://127.0.0.1:8501"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    @app.get("/help")
    async def serve_help():
        """Serves the help.txt file."""
        HELP_FILE_PATH = BASE_DIR / "help.txt"
        return FileResponse(path=HELP_FILE_PATH, media_type="text/plain")

    @app.get("/", response_class=PlainTextResponse)
    async def default_route(request: Request):
        """Serves the surf report."""
        parsed_parameters = [
            f"{key}={value}" if value else key
            for key, value in request.query_params.items()
        ]
        passed_args = ",".join(parsed_parameters)

        # get stdout from print function (probably not ideal but whatever)
        f = io.StringIO()
        with redirect_stdout(f):
            surf.run(args=passed_args)
        return f.getvalue()

    return app


env = ServerSettings()
app = create_app(env)

if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    uvicorn.run(app, host=str(env.IP_ADDRESS), port=env.PORT)
