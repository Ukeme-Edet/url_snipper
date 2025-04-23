from fastapi import Request, Response, status, APIRouter
from src.models import SnipperIn
import src.controller as controller

api = APIRouter()


@api.get("/")
async def read_root():
    return {"Hello": "World"}


@api.post("/shorten")
async def create_snipper(request: Request, snipper: SnipperIn):
    return await controller.create_snipper(
        snipper.url, request.headers.get("X-Forwarded-For")
    )


@api.get("/expand/{snipper_id}")
async def read_snipper(snipper_id: str):
    if not snipper_id or not snipper_id.isalnum():
        return Response(
            "Invalid Request", status_code=status.HTTP_400_BAD_REQUEST
        )
    sanitized_snipper_id = snipper_id.strip()
    return await controller.get_snipper(sanitized_snipper_id)


@api.delete("/delete/{snipper_id}")
async def delete_snipper(snipper_id: str):
    if not snipper_id or not snipper_id.isalnum():
        return Response(
            "Invalid Request", status_code=status.HTTP_400_BAD_REQUEST
        )
    sanitized_snipper_id = snipper_id.strip()
    return await controller.delete_snipper(sanitized_snipper_id)


@api.get("/all")
async def get_all_snippers():
    return await controller.get_all_snippers()
