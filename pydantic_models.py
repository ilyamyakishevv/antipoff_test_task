from pydantic import BaseModel

class QueryRequest(BaseModel):
    cadastre_number: str
    latitude: str
    longitude: str


class ResultResponse(BaseModel):
    id: int
    result: bool

    