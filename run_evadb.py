import evadb

cursor = evadb.connect().cursor()

params = {
    "user": "admin",
    "password": "password",
    "host": "localhost",
    "port": "5432",
    "database": "evadb",
}

query = f"CREATE DATABASE postgres_data WITH ENGINE = 'postgres', PARAMETERS = {params};"
cursor.query(query).df()

cursor.query("""
USE postgres_data {
  DROP TABLE IF EXISTS transaction_table
}
""").df()