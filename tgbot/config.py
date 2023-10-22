from dataclasses import dataclass

from environs import Env
from os import environ
import dotenv




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
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            use_redis=env.bool("USE_REDIS"),
            admin_password=env.int("ADMIN_PASSWORD")
        ),
        misc=Miscellaneous()
    )





