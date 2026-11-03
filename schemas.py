from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class LoginIn(BaseModel):
    username: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12)
    expires_at: datetime | None = None
    quota_bytes: int = Field(default=0, ge=0)

class UserPatch(BaseModel):
    is_active: bool | None = None
    expires_at: datetime | None = None
    quota_bytes: int | None = Field(default=None, ge=0)

class ServerCreate(BaseModel):
    name: str
    country: str
    region: str = ""
    hostname: str
    port: int = Field(default=443, ge=1, le=65535)
    protocol: str = "VLESS"

class UserOut(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool
    expires_at: datetime | None = None
    quota_bytes: int = 0
    used_bytes: int = 0
