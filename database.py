import sqlite3
from sqlite3 import Error

database = r"bdd.db"

def create_connection():
  c = None
  try:
    c = sqlite3.connect(database)
    print(sqlite3.version)
    return c
  except Error as e:
    print(e)

def create_table(conn, create_table_sql):
  try:
    c = conn.cursor()
    c.execute(create_table_sql)
  except Error as e:
    print(e)
  finally:
    if c:
      c.close()

def dict_factory(cursor, row):
  d = {}
  for i, col in enumerate(cursor.description):
    d[col[0]] = row[i]
  return d

def execute(sql, isSelect=True):
  conn = sqlite3.connect(database)
  conn.row_factory = dict_factory
  cur = conn.cursor()
  if isSelect:
    return cur.execute(sql).fetchall()
  else:
    result = cur.execute(sql)
    conn.commit()
    return result

def start_db():
  conn = create_connection()
  if conn is not None:
    user_table =  """ CREATE TABLE IF NOT EXISTS user (
                      id integer PRIMARY KEY AUTOINCREMENT,
                      name varchar(20),
                      password varchar(20), 
                      email varchar(50)
                      ); 
                  """
    create_table(conn, user_table)
  else:
    print("Error : Cannot create the database connection.")

start_db()