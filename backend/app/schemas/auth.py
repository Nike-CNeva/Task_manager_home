from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    auth_token: str
    token_type: str