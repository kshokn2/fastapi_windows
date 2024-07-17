from pydantic import BaseModel

class Data(BaseModel):
    user: str
    code: str