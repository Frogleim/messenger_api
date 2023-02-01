import psycopg2
from pydantic import BaseModel
import bcrypt


class User(BaseModel):
    username: str
    password: str


def db_connect():
    conn = psycopg2.connect(host="localhost",
                            database="postgres",
                            user="postgres",
                            password="123456"
                            )

    return conn


def check_username(username):
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM messenger_users WHERE username = '{username}'"),
        result = cursor.fetchone()
        if result is None:
            return False
        else:
            return True


def save_users(username, password):
    connection = db_connect()
    curs = connection.cursor()
    curs.execute("INSERT INTO messenger_users (username, password)"
                 " VALUES (%s, %s)",

                 (username, password))
    connection.commit()
    connection.close()
    print('Saved Successfully')


def retrieve_user(username: str, password: str):
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messenger_users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if not user:
            return None
        return User(username=user[0], password=user[1])


def edit_user(id, e_mail, avatar50, avatar100, avatar400):
    connection = db_connect()
    curs = connection.cursor()
    curs.execute("UPDATE messenger_users SET email=%s, avatar_50x50=%s, avatar_100x100=%s, "
                 "avatar_400x400=%s WHERE id=%s",
                 (e_mail, avatar50, avatar100, avatar400, id))
    connection.commit()
    connection.close()
    print('Saved Successfully')


if __name__ == "__main__":
    create_table()
