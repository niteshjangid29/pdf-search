from pydantic import BaseModel

class TokenData(BaseModel):
    id: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str