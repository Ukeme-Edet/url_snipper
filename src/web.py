from fastapi import Request, Response, status, APIRouter
from src.models import SnipperIn
import src.controller as controller

api = APIRouter()


@api.get("/")
def read_root():
    return {"Hello": "World"}


@api.post("/shorten")
def create_snipper(request: Request, snipper: SnipperIn):
    return controller.create_snipper(snipper.url, request.client.host)


@api.get("/expand/{snipper_id}")
def read_snipper(snipper_id: str):
    if not snipper_id or not snipper_id.isalnum():
        print(snipper_id, snipper_id.isalnum())
        return Response(
            "Invalid Request", status_code=status.HTTP_400_BAD_REQUEST
        )
    sanitized_snipper_id = snipper_id.strip()
    return controller.get_snipper(sanitized_snipper_id)


@api.delete("/delete/{snipper_id}")
def delete_snipper(snipper_id: str):
    if not snipper_id or not snipper_id.isalnum():
        return Response(
            "Invalid Request", status_code=status.HTTP_400_BAD_REQUEST
        )
    sanitized_snipper_id = snipper_id.strip()
    return controller.delete_snipper(sanitized_snipper_id)


@api.get("/all")
def get_all_snippers():
    return controller.get_all_snippers()
