from pydantic import BaseModel


class SnipperIn(BaseModel):
    url: str
