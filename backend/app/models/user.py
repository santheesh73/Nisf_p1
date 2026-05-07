from pydantic import BaseModel


class UserDocument(BaseModel):
    id: str
    email: str
    password_hash: str
    name: str
    created_at: str
    updated_at: str
    is_active: bool = True


class PublicUser(BaseModel):
    id: str
    email: str
    name: str
