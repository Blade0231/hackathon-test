import sqlite3
import pandas as pd
from abc import ABC, abstractmethod


class Database(ABC):
    def __init__(self, database_name="data\\database.db"):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    @abstractmethod
    def create_table():
        pass

    @abstractmethod
    def add_record():
        pass

    def run_query(self, sql_query, params=None):
        if params is not None:
            self.cursor.execute(sql_query, params)
        else:
            self.cursor.execute(sql_query)
        self.conn.commit()

        result = self.cursor.fetchall()
        df = pd.DataFrame(result, columns=[desc[0] for desc in self.cursor.description])

        return df

    def close(self):
        self.conn.close()


class UserDatabase(Database):
    def __init__(self):
        super().__init__()

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            USER_ID TEXT PRIMARY KEY NOT NULL,
            NAME TEXT NOT NULL,
            ROLE TEXT,
            PHONE TEXT,
            EMAIL TEXT NOT NULL,
            PASSWORD TEXT NOT NULL
        );
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def add_record(self, user_id, name, role, phone, email, password):
        insert_user_sql = "INSERT INTO users (USER_ID, NAME, ROLE, PHONE, EMAIL, PASSWORD) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(
            insert_user_sql, (user_id, name, role, phone, email, password)
        )
        self.conn.commit()

    def get_user(self, user_id):
        get_user_sql = "SELECT * FROM users WHERE USER_ID = ?"
        self.cursor.execute(get_user_sql, (user_id,))
        user = self.cursor.fetchone()
        return user

    def delete_user(self, user_id):
        delete_user_sql = "DELETE FROM users WHERE USER_ID = ?"
        self.cursor.execute(delete_user_sql, (user_id,))
        self.conn.commit()


class UserAddress(Database):
    def __init__(self, database_name="data\database.db"):
        super().__init__(database_name)

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS address (
            USER_ID TEXT PRIMARY KEY NOT NULL,
            STREET TEXT NOT NULL,
            CITY TEXT,
            STATE TEXT,
            POSTAL_CODE TEXT NOT NULL,
            COUNTRY TEXT NOT NULL
        );
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def add_record(self, user_id, street, city, state, postal_code, country):
        insert_user_sql = "INSERT INTO users (USER_ID, STREET, CITY, STATE, POSTAL_CODE, COUNTRY) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(
            insert_user_sql, (user_id, street, city, state, postal_code, country)
        )
        self.conn.commit()


class Schedule(Database):
    def __init__(self, database_name="data\database.db"):
        super().__init__(database_name)

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS schedule (
            ID TEXT PRIMARY KEY NOT NULL,
            USER_ID TEXT NOT NULL,
            CLIENT_ID TEXT,
            START_TIME DATETIME,
            END_TIME DATETIME
        );
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def add_record(self, user_id, client_id, start_time, end_time):
        insert_user_sql = "INSERT INTO users (USER_ID, CLIENT_ID, START_TIME, END_TIME) VALUES (?, ?, ?, ?)"
        self.cursor.execute(insert_user_sql, (user_id, client_id, start_time, end_time))
        self.conn.commit()


class Attendance(Database):
    def __init__(self, database_name="data\database.db"):
        super().__init__(database_name)

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS schedule (
            ID TEXT NOT NULL,
            USER_ID TEXT NOT NULL,
            STATUS TEXT,
            CREATED DATETIME
        );
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def add_record(self, id, user_id, status, created):
        insert_user_sql = (
            "INSERT INTO users (ID, USER_ID, STATUS, CREATED) VALUES (?, ?, ?, ?)"
        )
        self.cursor.execute(insert_user_sql, (id, user_id, status, created))
        self.conn.commit()


def main():
    db = UserDatabase()

    add = UserAddress()

    scd = Schedule()

    att = Attendance()

    db.add_record(
        user_id="JohnDoe77",
        name="John Doe",
        role="Admin",
        phone="123-456-7890",
        email="john.doe@example.com",
        password="John@123",
    )

    result = db.run_query(sql_query="SELECT * FROM users")

    db.close()


if __name__ == "__main__":
    main()
