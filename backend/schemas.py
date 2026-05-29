from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserCreateSchema(BaseModel):
    username: str
    mail: EmailStr
    password: str = Field(max_length=72)

class UserLoginSchema(BaseModel):
    mail: EmailStr
    password: str = Field(max_length=72)

class UserResponseSchema(BaseModel):
    id: int
    username: str
    mail: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)

class TokenSchema(BaseModel):
    access_token: str
    token_type: str