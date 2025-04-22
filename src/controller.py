from fastapi import Response, status
from fastapi.responses import JSONResponse
from src.service import SnipperService

service = SnipperService()


async def get_snipper(snipper_id: str):
    query_result = await service.get_snipper_by_id(snipper_id)
    if query_result:
        return JSONResponse(
            content={"url": query_result.url},
            status_code=status.HTTP_200_OK,
        )
    return Response(content="Not found", status_code=status.HTTP_404_NOT_FOUND)


async def create_snipper(url: str, ip: str):
    try:
        query_result = await service.get_snipper_by_url(url)
        if query_result:
            return JSONResponse(
                content={"key": query_result.id},
                status_code=status.HTTP_200_OK,
            )
        snipper = await service.create_snipper(url, ip)
        return JSONResponse(
            {"key": snipper.id}, status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            "Server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def delete_snipper(snipper_id: str):
    try:
        snipper = await service.get_snipper_by_id(snipper_id)
        if snipper:
            await service.delete_snipper(snipper_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return Response(
            content="Not found", status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            "Server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


async def get_all_snippers():
    try:
        snippers = await service.get_all_snippers()
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
