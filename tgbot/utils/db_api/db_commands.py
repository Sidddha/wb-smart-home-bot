import sqlite3
from tgbot.utils.db_api.user import User


class Database:
    """
    Методы для взаимодействия с базой данных
    """

    def __init__(self, path_to_db="tgbot/data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False,
                fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connectoin = self.connection
        connectoin.set_trace_callback(logger)
        cursor = connectoin.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connectoin.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connectoin.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE if not exists Users (
        id int NOT NULL,
        chat int NOT NULL,
        name varchar(255) NOT NULL,
        status varchar(255),
        PRIMARY KEY (id)
        )
        """

        self.execute(sql, commit=True)

    def get_all_users(self):
        """
        Retrieve all users from the database.

        Returns:
        - List of users.
        """
        sql = "SELECT * FROM Users"
        return self.execute(sql, fetchall=True)

    def get_all_ids(self):
        """
        Retrieve all user IDs from the database.

        Returns:
        - List of user IDs.
        """
        sql = "SELECT id FROM Users"
        return self.execute(sql, fetchall=True)

    def is_user_exist(self, user_id: int):
        """
        Check if a user with the given ID exists in the database.

        Arguments:
        - user_id (int): The ID of the user.

        Returns:
        - True if the user exists, False otherwise.
        """
        ids = self.get_all_ids()
        for id in ids:
            if user_id == id[0]:
                return True
        else:
            return False

    def add_user(self, id: int, chat: int, name: str, status: str):
        """
        Add a user to the database.

        Keyword Arguments:
        - id (int): The ID of the user.
        - chat_id (int): The ID of the chat with bot.
        - name (str): The name of the user.
        - status (str): The status of the user.
        """
        if self.is_user_exist(id):
            print(f"User with ID: {id} already exists.")
            pass
        else:
            sql = "INSERT INTO Users(id, chat, name, status) VALUES(?, ?, ?, ?)"
            parameters = (id, chat, name, status)
            self.execute(sql, parameters=parameters, commit=True)
    
    @staticmethod
    def format_args(sql, parameters: dict):
        """
        Format SQL query and parameters.

        Arguments:
        - sql (str): SQL query string.
        - parameters (dict): Dictionary of parameters.

        Returns:
        - Formatted SQL query string.
        - Tuple of parameter values.
        """
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def get_user(self, **kwargs):
        """
        Retrieve a user from the database based on the given criteria.

        Keyword Arguments:
        - id (int): The ID of the user.

        Returns:
        - The user object.
        """
        if self.is_user_exist(kwargs.get('id')):
            sql = "SELECT * FROM Users WHERE "
            sql, parameters = self.format_args(sql, kwargs)
            user_data = self.execute(sql, parameters=parameters, fetchone=True)
            user = User(*user_data)
            return user
        else: 
            print(f"User with ID: {kwargs.get('id')} does not exist.")

    def get_status(self, **kwargs):
        """
        Retrieve the status of a user from the database based on the given criteria.

        Keyword Arguments:
        - id (int): The ID of the user.

        Returns:
        - The user object.
        """
        sql = "SELECT status FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        user_data = self.execute(sql, parameters, fetchone=True)
        user = User(*user_data)
        return user

    def get_admins(self):
        """
        Retrieve all administrators from the database.

        Returns:
        - List of administrator users.
        """
        sql = "SELECT * FROM Users WHERE status = 'ADMIN'"
        admins = list()
        data =  self.execute(sql, fetchall=True)
        if data:
            for admin in data:
                user = User(*admin)
                admins.append(user)
            return admins
        else: 
            print("No admins found")

    def count_users(self):
        """
        Count the number of users in the database.

        Returns:
        - The total number of users.
        """
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_status(self, id: int, status: str):
        """
        Update the status of a user in the database based on the given criteria.

        Keyword Arguments:
        - id (int): The ID of the user.
        - status (str): The new status of the user.
        """
        sql = "UPDATE Users SET status=? WHERE id=?"
        parameters = (status, id)
        self.execute(sql, parameters=parameters, commit=True)

    def delete_user(self, **kwargs):
        """
        Delete a user from the database based on the given criteria.

        Keyword Arguments:
        - id (int): The ID of the user.
        """
        sql = "DELETE FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        self.execute(sql, parameters=parameters, commit=True)


def logger(statement):
    print(f"""

    _____________________________________________
    
    Executing:
    {statement}
    _____________________________________________
    """)
