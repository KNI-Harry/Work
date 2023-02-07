import sqlite3

conn = sqlite3.connect('login.db')
print("Opened database successfully");

conn.execute('CREATE TABLE login(user_id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT not null, password TEXT not null);')
conn.execute('insert into login(user_id,email,password) VALUES (120,"xyz@mail.com","123xyz")')
conn.execute('insert into login (email,password) VALUES ("abc@mail.com", "123abc")')
conn.commit()
conn.close()