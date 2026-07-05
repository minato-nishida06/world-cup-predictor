import psycopg2

conn = psycopg2.connect(
    host="db",
    port=5432,
    dbname="world_cup",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()
cur.execute("SELECT version();")
print(cur.fetchone())

cur.close()
conn.close()
