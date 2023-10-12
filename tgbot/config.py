from dataclasses import dataclass

import asyncio
from environs import Env
from os import environ
import dotenv


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    url: str


@dataclass
class TgBot:
    token: str
    # admin_ids: list[int]
    use_redis: bool
    admin_password: int


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            # admin_ids=list(map(int, get_admins_ids())),
            use_redis=env.bool("USE_REDIS"),
            admin_password=env.int("ADMIN_PASSWORD")
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASSWORD'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            url=env.str('POSTGRES_URI')
        ),
        misc=Miscellaneous()
    )





