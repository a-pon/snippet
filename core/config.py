import multiprocessing

from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    app_port: int = 8000
    app_host: str = 'localhost'
    reload: bool = True
    cpu_count: int | None = None
    postgres_dsn: PostgresDsn = MultiHostUrl(
        'postgresql+asyncpg://postgres:postgres@localhost:5432/snippetdb')
    jwt_secret: str = 'your_super_secret'
    algorithm: str = 'HS256'

    class Config:
        _env_file = '.env'
        _extra = 'allow'


app_settings = AppSettings()

uvicorn_options = {
    'host': app_settings.app_host,
    'port': app_settings.app_port,
    'workers': app_settings.cpu_count or multiprocessing.cpu_count(),
    'reload': app_settings.reload
}
