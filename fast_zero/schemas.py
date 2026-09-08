from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    password_hash: str


class UserList(BaseModel):
    users: list[UserPublic]



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password_hash: str