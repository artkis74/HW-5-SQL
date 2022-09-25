import psycopg2


def create_db(conn):
    cur.execute("""
                   CREATE TABLE IF NOT EXISTS client(
                       client_id SERIAL PRIMARY KEY,
                       name VARCHAR(40),
                       surname VARCHAR(40),
                       email VARCHAR(60) UNIQUE
                   );
                   """)
    cur.execute("""
                   CREATE TABLE IF NOT EXISTS phone(
                       phone_id SERIAL PRIMARY KEY,
                       number BIGINT UNIQUE,
                       client_id INTEGER  REFERENCES client(client_id)
                   );
                   """)


def add_client(conn, name, surname, email, number=None):
    cur.execute("""
                    INSERT INTO client(name, surname, email) VALUES (%s, %s, %s) RETURNING client_id;
                    """, (name, surname, email))
    client_id = cur.fetchone()[0]
    cur.execute("""
                    INSERT INTO phone(number, client_id) VALUES (%s, %s);
                     """, (number, client_id))


def add_phone(conn, client_id, number):
    cur.execute("""
                         INSERT INTO phone(number, client_id) VALUES (%s, %s);
                             """, (number, client_id))

def change_client(conn, client_id, name=None, surname=None, email=None, number=None):
    if name is not None:
        cur.execute("""
                      UPDATE client SET name=%s WHERE client_id=%s;
                      """, (name, client_id))
    if surname is not None:
        cur.execute("""
                      UPDATE client SET surname=%s WHERE client_id=%s;
                      """, (surname, client_id))
    if email is not None:
        cur.execute("""
                      UPDATE client SET email=%s WHERE client_id=%s;
                        """, (email, client_id))
    if number is not None:
        cur.execute("""
                      UPDATE phone SET number=%s WHERE client_id=%s;
                      """, (number, client_id))


def delete_phone(conn, number):  # не удаляем, а обнавляем на None, чтобы работала функция find_client
    cur.execute("""
               UPDATE phone SET number=None WHERE number=%s;
               """, (number,))


def delete_client(conn, client_id):
    cur.execute("""
                  DELETE FROM phone WHERE client_id=%s;
                       """, (client_id,))
    cur.execute("""
                  DELETE FROM client WHERE client_id=%s;
                  """, (client_id,))


def find_client(conn, name=None, surname=None, email=None, number=None):
    if email is not None:
        cur.execute("""
                   SELECT  client.name, client.surname, client.email, number FROM client
                   JOIN phone ON client.client_id = phone.client_id
                   WHERE email=%s;
                   """, (email,))
        print(cur.fetchone())
    if number is not None:
        cur.execute("""
                    SELECT  client.name, client.surname, client.email, number FROM client
                    JOIN phone ON client.client_id = phone.client_id
                    WHERE number=%s;
                    """, (number,))
        print(cur.fetchone())
    if name and surname is not None:
        cur.execute("""
                            SELECT  client.name, client.surname, client.email, number FROM client
                            JOIN phone ON client.client_id = phone.client_id
                            WHERE name=%s AND surname=%s;
                            """, (name,surname))
        print(cur.fetchone())
    elif name is not None:
        cur.execute("""
                    SELECT  client.name, client.surname, client.email, number FROM client
                    JOIN phone ON client.client_id = phone.client_id
                    WHERE name=%s;
                    """, (name,))
        print(cur.fetchone())
    elif surname is not None:
        cur.execute("""
                    SELECT  client.name, client.surname, client.email, number FROM client
                    JOIN phone ON client.client_id = phone.client_id
                    WHERE surname=%s;
                    """, (surname,))
        print(cur.fetchone())


with psycopg2.connect(database="clients_db", user="postgres", password="YOUR_PASSWORD") as conn:
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)
        create_db(conn)
        add_client(conn, 'Василий', 'Петров', 'pop@mail.ru', 89658542312)
        add_client(conn, 'Дмитрий', 'Пупкин', 'pup@mail.ru')
        add_phone(conn, 2, 89528173015)
        # change_client(conn, 1, 'Вася', 'Белкин', 'pips@gmail.com')
        # delete_phone(conn, 89658542312)
        # delete_client(conn, 1)
        find_client(conn, surname='Белкин', name='Вася')
conn.close()

