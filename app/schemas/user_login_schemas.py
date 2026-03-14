from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    mobile_number: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =====================================================
# USERS
# =====================================================


class AdminCreateUser(BaseModel):
    name: str
    mobile_number: str
    password: str = Field(min_length=8)
    role: str  # ADMIN / COORDINATOR / DRIVER
