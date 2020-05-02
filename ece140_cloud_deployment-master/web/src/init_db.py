# Import MySQL Connector Driver
import mysql.connector as mysql

# Load the credentials from the secured .env file
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] # must 'localhost' when running this script outside of Docker

# Connect to the database
db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# # CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!! CAUTION!!!
cursor.execute("drop table if exists Users;")

# CREATED USERS TABLE
try:
  cursor.execute("""
    CREATE TABLE Users (
      id integer  AUTO_INCREMENT PRIMARY KEY,
      Username  VARCHAR(50) NOT NULL,
      Password   VARCHAR(50) NOT NULL,
      Status       VARCHAR(50) NOT NULL
    );
  """)
except:
  print("Table already exists. Not recreating it.")

# Insert Records into Users
query = "insert into Users (Username, Password, Status) values (%s, %s, %s)"
values = [
  ('Jesi','jesi@ucsd.edu','Valid'),
  ('Jesus','jesus@ucsd.edu','Pending'),
  ('Zack','zack@ucsd.edu','Pending'),
  ('John','john@ucsd.edu','Pending'),
]
cursor.executemany(query, values)
db.commit()

# Selecting Records
cursor.execute("select * from Users;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]
db.close()
