from .user.start import register_user
from .admin.admin import register_admin
from .echo import register_echo
from .errors import register_errors
from .testing import register_test


from aiogram import Dispatcher


def register_handlers(dp: Dispatcher):
    register_test(dp)
    register_admin(dp)
    register_user(dp)
    register_echo(dp)
    register_errors(dp)