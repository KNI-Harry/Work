import sqlite3

conn = sqlite3.connect('Users.db')
print("Opened database successfully");

conn.execute('CREATE TABLE people(Email TEXT, Username TEXT, Password TEXT)')
print("Table created successfully");
conn.close()