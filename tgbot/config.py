from dataclasses import dataclass

from environs import Env
from os import environ
import dotenv




@dataclass
class TgBot:
    token: str
    # admin_ids: list[int]
    use_redis: bool
    default_password: str
    admin_password_hash: str
    dashboards: str


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
            default_password=env.str("DEFAULT_PASSWORD"),
            admin_password_hash=env.str("ADMIN_PASSWORD_HASH"),
            dashboards='wb-webui.conf'
        ),
        misc=Miscellaneous()
    )





