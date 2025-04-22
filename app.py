from src import create_app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import api
import os

app = create_app()
origins = [
    "http://localhost:3000",
    "https://snipper.0xtech-wiz.me",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/ping")
async def ping():
    return {"ping": "pong"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",  # Use import string for production with workers > 1
        host="0.0.0.0",
        port=8000,
        workers=os.cpu_count() * 2 + 1,
        server_header=False,
        proxy_headers=True,
        forwarded_allow_ips="*",
        log_level="info",
        use_colors=True,
    )
