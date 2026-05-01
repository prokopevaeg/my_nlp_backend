from typing import AsyncGenerator

from dishka import (
    Provider,
    provide,
    make_async_container,
    Scope
)
from fastapi import Request
from dishka.integrations.fastapi import FastapiProvider
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from nlp.config import (
    DBConfig,
    AppConfig
)
from nlp.services import (
    PasswordService,
    AuthService
)
from nlp.repositories import (
    UserRepository,
    ProjectRepository,
    TaskRepository
)
from nlp.types import AuthenticatedUserId
from nlp.errors import AuthError


class ConfigsProvider(Provider):
    scope = Scope.APP

    @provide
    def df_config(self) -> DBConfig:
        return DBConfig()

    @provide
    def app_config(self) -> AppConfig:
        return AppConfig()


class DBProvider(Provider):
    scope = Scope.APP

    @provide
    def engine(self, config: DBConfig) -> AsyncEngine:
        return create_async_engine(config.conn_url)

    @provide
    def sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            expire_on_commit=False,
            autoflush=False,
            autobegin=True
        )

    @provide(scope=Scope.REQUEST)
    async def session(
            self,
            sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except:
                await session.rollback()
            finally:
                await session.close()


class AuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def auth(
        self,
        r: Request,
        auth_service: AuthService,
        user_repo: UserRepository,
    ) -> AuthenticatedUserId:
        token = r.cookies.get("token")
        if not token:
            raise AuthError("Unauthorized", status=401)
        user_id = auth_service.get_user_id(token)
        if not user_id:
            raise AuthError("Invalid credentials", status=401)
        if not await user_repo.get_by_id(user_id):
            raise AuthError("Unauthorized", status=401)
        return AuthenticatedUserId(user_id)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    password = provide(PasswordService)

    @provide
    def auth(self, conf: AppConfig) -> AuthService:
        return AuthService(conf.secret, conf.token_expire_time)


repo_provider = Provider(scope=Scope.REQUEST)
repo_provider.provide_all(
    UserRepository,
    ProjectRepository,
    TaskRepository
)
container = make_async_container(
    AuthProvider(),
    ConfigsProvider(),
    DBProvider(),
    ServiceProvider(),
    repo_provider,
    FastapiProvider()
)
