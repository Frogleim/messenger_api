import psycopg2


def db_connect():
    conn = psycopg2.connect(host="localhost",
                            database="postgres",
                            user="postgres",
                            password="123456"
                            )

    return conn


def create_table():
    connection = db_connect()

    cursor = connection.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS messenger_users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255),
        password VARCHAR(255),
        email VARCHAR(255),
        avatar_50x50 TEXT,
        avatar_100x100 TEXT,
        avatar_400x400 TEXT
        
    );
    """

    cursor.execute(create_table_sql)
    connection.commit()
    connection.close()


def save_users(username, password):
    connection = db_connect()
    curs = connection.cursor()
    curs.execute("INSERT INTO messenger_users (username, password)"
                 " VALUES (%s, %s)",

                 (username, password))
    connection.commit()
    connection.close()
    print('Saved Successfully')


def check_username(username):
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM messenger_users WHERE username = '{username}'"),
        result = cursor.fetchone()
        if result is None:
            return False
        else:
            return True


def check_password(password):

    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM messenger_users WHERE password = '{password}'"),
        result = cursor.fetchone()
        if result is None:
            return False
        else:
            return True


def edit_user(e_mail, avatar50, avatar100, avatar400):
    connection = db_connect()
    curs = connection.cursor()
    curs.execute("INSERT INTO messenger_users (e_mail, avatar_50, avatar_100, avatar_100)"
                 " VALUES (%s, %s)",

                 (e_mail, avatar50, avatar100, avatar400))
    connection.commit()
    connection.close()
    print('Saved Successfully')


if __name__ == "__main__":
    create_table()
