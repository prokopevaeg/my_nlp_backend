from fastapi import APIRouter
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import (
    FromDishka,
    DishkaRoute
)

from nlp.repositories import UserRepository
from .dtos.user import (
    RegisterUserDTO,
    LoginUserDTO,
    ShowUserDTO
)
from nlp.errors import (
    UserAlreadyExists,
    UndefinedUserError,
    InvalidPasswordError
)
from nlp.entities import User
from nlp.services import (
    PasswordService,
    AuthService
)

user_router = APIRouter(prefix="/user", tags=["Users router"], route_class=DishkaRoute)


@user_router.post("/register")
async def register_user(
    dto: RegisterUserDTO,
    user_repo: FromDishka[UserRepository],
    password_service: FromDishka[PasswordService]
) -> ShowUserDTO:
    if await user_repo.get_by_email(dto.email):
        raise UserAlreadyExists("Already registered")
    user = User(dto.email, password_service.hash_password(dto.password))
    user_repo.session.add(user)
    await user_repo.session.flush([user])
    return user


@user_router.post("/login")
async def login_user(
    dto: LoginUserDTO,
    user_repo: FromDishka[UserRepository],
    password_services: FromDishka[PasswordService],
    auth_service: FromDishka[AuthService]
):
    user = await user_repo.get_by_email(dto.email)
    if not user:
        raise UndefinedUserError("User does not exist")
    if not password_services.check_password(user.password, dto.password):
        raise InvalidPasswordError("Invalid password")
    token = auth_service.generate_user_token(user.id)
    resp = JSONResponse({"detail": "Logged in"})
    resp.set_cookie("token", token)
    return resp
