# login input

# token response

# register inpu


from pydantic import BaseModel


class UserRegisterInput(BaseModel):
    username: str
    # phone_number: str | None = None
    password: str

    # email: EmailStr
    # first_name: str | None = None
    # last_name: str | None = None


class LoginInput(BaseModel):
    username: str
    password: str
    email: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    # refresh_token: str | None = None
    token_type: str = "bearer"
    expires_in: int | None = None


class TokenPayload(BaseModel):
    sub: str
    exp: int
    iss: str | None = None
    aud: str | None = None
    iat: str | None = None
