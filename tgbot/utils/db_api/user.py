
class User:
    """
    status may be\n
    UNKNOWN_USER;\n
    USER;\n
    ADMIN;\n
    REQUEST_SENT 
    """

    
    def __init__(self, id=None, name=None, status="UNKNOWN_USER"):
        self.id = id
        self.name = name
        self.status = status



