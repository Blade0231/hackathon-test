import sqlite3


class UserDatabase:
    def __init__(self, database_name="data\\database.db"):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            USER_ID INTEGER PRIMARY KEY,
            NAME TEXT NOT NULL,
            ROLE TEXT,
            PHONE TEXT,
            EMAIL TEXT NOT NULL
        );
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def add_user(self, name, role, phone, email):
        insert_user_sql = (
            "INSERT INTO users (NAME, ROLE, PHONE, EMAIL) VALUES (?, ?, ?, ?)"
        )
        self.cursor.execute(insert_user_sql, (name, role, phone, email))
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

    def run_query(self, sql_query, params=None):
        if params is not None:
            self.cursor.execute(sql_query, params)
        else:
            self.cursor.execute(sql_query)
        self.conn.commit()
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


db = UserDatabase()

db.add_user(
    name="John Doe", role="Admin", phone="123-456-7890", email="john.doe@example.com"
)

df = db.run_query(sql_query="SELECT * FROM users")

db.close()
