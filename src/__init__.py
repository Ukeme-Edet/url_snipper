from .web import api
from fastapi import FastAPI


def create_app():
    app = FastAPI()
    app.include_router(api, prefix="/api")
    return app
