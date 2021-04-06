import mysql.connector

db_conn = mysql.connector.connect(host="localhost", user="events", password="password", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE send
          (id INT NOT NULL AUTO_INCREMENT,
           mail_ID VARCHAR(100), 
           address VARCHAR(250) NOT NULL,
           date_created VARCHAR(250) NOT NULL,
           CONSTRAINT send_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE recievemail
          (id INT NOT NULL AUTO_INCREMENT,
          mail_ID VARCHAR(100), 
           address VARCHAR(250) NOT NULL,
           date_created VARCHAR(250) NOT NULL,
           CONSTRAINT recievemail_pk PRIMARY KEY (id))
          ''')

db_conn.commit()
db_conn.close()
