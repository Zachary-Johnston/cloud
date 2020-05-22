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


# CREATED NEWS TABLE
try:
  cursor.execute("""
    CREATE TABLE News (
      id integer  AUTO_INCREMENT PRIMARY KEY,
      Title  VARCHAR(50) NOT NULL,
      Date   VARCHAR(50) NOT NULL,
      Update       VARCHAR(50) NOT NULL
    );
  """)
except:
  print("Table already exists. Not recreating it.")

# Insert Records into News
query = "insert into Users (Title, Date, Update) values (%s, %s, %s)"
values = [
  ('Prototype Completed','May 15, 2020','All hardware is functional. Your coffee comes out ice cold! Working on software integration.'),
  ('Taste Quality Improvements','May 20, 2020','Ridding the machine of any influence on taste from the cooling unit. Taste will be 100% safe and neutral!'),
]
cursor.executemany(query, values)
db.commit()




try:
 cursor.execute("""
   CREATE TABLE cofset (
     id integer  AUTO_INCREMENT PRIMARY KEY,
     coffeeid VARCHAR(50) NOT NULL,
     temperature VARCHAR(50) NOT NULL,
     time    VARCHAR(50) NOT NULL
   );
 """)
except:
 print("Table already exists. Not recreating it.")
 
# Insert Records into cofset
query = "insert into cofset (coffeeid, temperature, time) values (%s, %s, %s)"
values = [
 ('someid', 'sometemp', 'sometime'),
]
cursor.executemany(query, values)
db.commit()




# Selecting Records
cursor.execute("select * from Users;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]

cursor.execute("select * from cofset;")
print('---------- DATABASE INITIALIZED ----------')
[print(x) for x in cursor]

db.close()
