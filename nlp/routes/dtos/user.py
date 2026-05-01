from pydantic import BaseModel, Field, EmailStr


class RegisterUserDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class ShowUserDTO(BaseModel):
    id: int
    email: EmailStr


class LoginUserDTO(RegisterUserDTO):
    pass
