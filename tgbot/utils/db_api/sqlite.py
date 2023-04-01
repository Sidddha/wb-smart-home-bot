

import sqlite3


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
        CREATE TABLE Users (
        id int NOT NULL,
        name varchar(255) NOT NULL,
        status varchar(255),
        PRIMARY KEY (id)
        )
        """

        self.execute(sql, commit=True)



    def select_all_users(self):
        sql = "SELECT * FROM Users"
        return self.execute(sql, fetchall=True)
    
    def select_all_ids(self):
        sql = "SELECT id FROM Users"
        return self.execute(sql, fetchall=True)
   
    def is_user_exist(self, id: int):
        ids = self.select_all_ids()
        if id in ids:
            return True
        else:
            return False

    def add_user(self, id: int, name: str, status: str):
        if self.is_user_exist(id):
            print(f"User with ID: {id} already exist.")
            pass
        else:
            sql = "INSERT INTO Users(id, name, status) VALUES(?, ?, ?)"
            parameters = (id, name, status)
            self.execute(sql, parameters=parameters, commit=True)
            
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
 
    def select_status(self, **kwargs):
        sql = "SELECT status FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)
    
    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_status(self, status, id):
        sql = "UPDATE Users SET status=? WHERE id=?"
        return self.execute(sql, parameters=(status, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE True")

def logger(statement):
    print(f"""

    _____________________________________________
    
    Executing:
    {statement}
    _____________________________________________
    """)
