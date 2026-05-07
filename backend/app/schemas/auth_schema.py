from pydantic import BaseModel, Field, field_validator


def normalize_email(value: str) -> str:
    email = str(value or "").strip().lower()
    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        raise ValueError("A valid email address is required.")
    return email


class AuthUser(BaseModel):
    id: str
    email: str
    name: str


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)
    name: str = Field(min_length=1, max_length=120)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return normalize_email(value)


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return normalize_email(value)


class AuthResponse(BaseModel):
    user: AuthUser
    access_token: str
    token_type: str = "bearer"


class AuthConfigResponse(BaseModel):
    auth_enabled: bool
    local_dev_mode: bool
