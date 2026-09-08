import psycopg

connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="devteam",
    user="devteam",
    password="devteam",
)

try:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            "insert into tasks (id,description,status) 
            values(
                '11111111-1111-1111-1111-111111111111',
                'Transaction test',
                'CREATED'
            )
            """
        )
        raise Exception("Something went wrong")
    connection.commit()
except Exception:
    connection.rollback()
    print("Transaction rolled back due to an error.")
finally:
    connection.close()