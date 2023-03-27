from .start_unknown import register_unknown
from .user.start_user import register_user
from .admin.start_admin import register_admin
from .echo import register_echo
from .errors import register_errors
from .testing import register_test


from aiogram import Dispatcher


def register_handlers(dp: Dispatcher):
    register_admin(dp)
    register_user(dp)
    register_unknown(dp)
    register_test(dp)
    # register_echo(dp)
    register_errors(dp)
