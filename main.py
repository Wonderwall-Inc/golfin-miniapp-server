""" Main entry point for this FastAPI Project """

import os
import uvicorn
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from app.user.api.v1 import user
from app.friend.api.v1 import friend
from app.point.api.v1 import point
from app.activity.api.v1 import activity
from app.social_media.api.v1 import social_media
from app.game_character.api.v1 import game_character
from app.record.api.v1 import record # FIXME

from core import config, database


app = FastAPI(
    title="Telegram Minapp server",
    description="Description of my app.",
    version="1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url=None,
)

origins = [
    "https://telegram.golfin.dev",
    "https://golfin-miniapp-dev-xi.vercel.app"
    # "https://golfin-miniapp-server-next-innovation.vercel.app",
    # "https://golfin-miniapp-server-dev-inky.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# * CORS // FIXME: handle the cors on prod
# if not config.cfg.prod:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )



# * Root for status check
@app.get("/")
def root():
    """
    Handle root route entry point to check server status
    """
    return "Golfin Miniapp Backend API Server Running"


# * Database Engines
if not os.getenv("TESTING"):
    database.Base.metadata.create_all(bind=database.engine)


# * FastAPI Routers
app.include_router(user.router)
app.include_router(point.router)
app.include_router(friend.router)
app.include_router(activity.router)
app.include_router(social_media.router)
app.include_router(game_character.router)
#app.include_router(record.router) # FIXME


if __name__ == "__main__":
    uvicorn.run(app, log_level=config.cfg.fastapi_log_level)
