import sqlite3

conn = sqlite3.connect('Rin.db')
cursor = conn.cursor()

cursor.execute("""
				CREATE TABLE users
				(user_id int PRIMARY KEY);
				""")

cursor.execute("""
				CREATE TABLE users_list(
				link text UNIQUE,
				last_episode text,
				user_id int UNIQUE, 
				FOREIGN KEY(user_id) REFERENCES users); 
				""")
cursor.execute("""
				INSERT INTO users
				VALUES(431862523197915146)
				""")
cursor.execute("""
				INSERT INTO users_list
				VALUES('http://fanserials.pro/black-lightning/',
						'1 сезон 10 серия',
						431862523197915146)
				""")
cursor.execute("""
				INSERT INTO users
				VALUES(417269196850987029)
				""")
cursor.execute("""
				INSERT INTO users_list
				VALUES('http://fanserials.pro/black-lightning/',
						'1 сезон 10 серия',
						417269196850987029)
				""")

conn.commit()
