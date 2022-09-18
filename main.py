import psycopg2

with psycopg2.connect(database="clients_db", user="postgres", password="K.,bvfz777") as conn:
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)


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
            return conn.commit()


        def add_client(conn, name, surname, email, number=None):
            cur.execute("""
                     INSERT INTO client(name, surname, email) VALUES (%s, %s, %s) RETURNING client_id;
                     """, (name, surname, email))
            client_id = cur.fetchone()[0]
            cur.execute("""
                     INSERT INTO phone(number, client_id) VALUES (%s, %s);
                      """, (number, client_id))
            return conn.commit


        def add_phone(conn, client_id, number):
            cur.execute("""
                          INSERT INTO phone(number, client_id) VALUES (%s, %s);
                              """, (number, client_id))
            return conn.commit


        def change_client(conn, client_id, name, surname, email, number=None):
            cur.execute("""
                   UPDATE client SET name=%s, surname=%s, email=%s  WHERE client_id=%s;
                   """, (name, surname, email, client_id))
            cur.execute("""
                   UPDATE phone SET number=%s WHERE client_id=%s;
                   """, (number, client_id))
            return conn.commit


        def delete_phone(conn, number):  # не удаляем, а обнавляем на None, чтобы работала функция find_client
            cur.execute("""
                UPDATE phone SET number=None WHERE number=%s;
                """, (number,))
            return conn.commit


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
                return print(cur.fetchone())
            else:
                cur.execute("""
                        SELECT  client.name, client.surname, client.email, number FROM client
                        JOIN phone ON client.client_id = phone.client_id
                        WHERE number=%s;
                        """, (number,))
            return print(cur.fetchone())

        create_db(conn)
        add_client(conn, 'Василий', 'Петров', 'pop@mail.ru', 89658542312)
        add_client(conn, 'Дмитрий', 'Пупкин', 'pup@mail.ru')
        add_phone(conn, 2, 89528173015)
        # change_client(conn, 1, 'Вася', 'Белкин', 'pips@gmail.com')
        # delete_phone(conn, 89658542312)
        # delete_client(conn, 1)
        # find_client(conn, email='pop@mail.ru')
conn.close()

