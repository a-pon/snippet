from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
