from tgbot.filters.admin import AdminFilter


#### User status constants ####

(
    UNKNOWN_USER,
    USER,
    ADMIN,
    REQUEST_SENT
) = map(int, range(4))
    
class User:
    def __init__(self, id=None, name=None, status=None):
        self.id = id
        self.name = name
        self.status = status
