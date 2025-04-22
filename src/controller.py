from fastapi import Response, status
from fastapi.responses import JSONResponse
from src.service import SnipperService

service = SnipperService()


def get_snipper(snipper_id: str):
    query_result = service.get_snipper(snipper_id)
    if query_result:
        return Response(
            content=query_result.url, status_code=status.HTTP_200_OK
        )
    return Response(content="Not found", status_code=status.HTTP_404_NOT_FOUND)


def create_snipper(url: str, ip: str):
    try:
        query_result = service.get_snipper(url)
        if query_result:
            return Response(
                content=query_result.id, status_code=status.HTTP_200_OK
            )
        snipper = service.create_snipper(url, ip)
        return Response(
            content=snipper.id, status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            "Server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def delete_snipper(snipper_id: str):
    try:
        snipper = service.get_snipper(snipper_id)
        if snipper:
            service.delete_snipper(snipper_id)
            return Response(content="Deleted", status_code=status.HTTP_200_OK)
        return Response(
            content="Not found", status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            "Server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def get_all_snippers():
    try:
        snippers = service.get_all_snippers()
        snippers_list = [
            {"id": snipper.id, "url": snipper.url} for snipper in snippers
        ]
        return JSONResponse(
            content=snippers_list, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            "Server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
