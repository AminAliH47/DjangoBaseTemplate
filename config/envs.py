from typing import List, Literal
from pydantic_settings import BaseSettings


class EnvsConfig(BaseSettings):
    DEBUG: bool
    TZ: str
    ENVIRONMENT: Literal['dev', 'prod'] = 'dev'

    SECRET_KEY: str

    ALLOWED_HOSTS: List[str] = list()
    CSRF_TRUSTED_ORIGINS: List[str] = list()

    PROJECT_TITLE: str = ''

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str = '5432'
    DB_CONN_MAX_AGE: int = 60

    REDIS_HOST: str
    REDIS_PORT: str = '6379'
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = None

    CACHE_TIMEOUT_HOURS: int | None = None

    RABBITMQ_HOST: str | None = None
    RABBITMQ_PORT: str = '5672'
    RABBITMQ_DEFAULT_USER: str | None = None
    RABBITMQ_DEFAULT_PASS: str | None = None

    MESSAGE_BROKER_TYPE: Literal['redis', 'rabbitmq'] = 'rabbitmq'

    def REDIS_SERVER_URL(
        self,
        db: int | None = None,
    ) -> str:
        db = db or self.REDIS_DB
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{db}'

    @property
    def RABBITMQ_SERVER_URL(self) -> str:
        return (
            f'amqp://{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS}'
            f'@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}'
        )

    @property
    def MESSAGE_BROKER_URL(self):
        if self.MESSAGE_BROKER_TYPE == 'rabbitmq':
            return self.RABBITMQ_SERVER_URL
        elif self.MESSAGE_BROKER_TYPE == 'redis':
            return self.REDIS_SERVER_URL(1)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = 'ignore'


envs = EnvsConfig()
