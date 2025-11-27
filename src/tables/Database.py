import sqlite3
import mysql.connector
import os

class Database:
    def __init__(self, database: str = "ApneTV") -> None:
        self.database = database
        
        self.username = None
        self.password = None
        self.ip_address = None
        self.port = None
        
        # Find the above db variable from OS env
        self.set_db_variables()

        self.connection = self.connect_to_db()
    
    def close(self):
        self.connection.close()

    def execute(self, query, params=None, fetchone: bool = False, fetchall: bool = False):
        cur = self.connection.cursor(dictionary=True)

        try:
            cur.execute(query, params or ())
        except mysql.connector.errors.IntegrityError as e: 
            if e.errno == 1062:
                print("Duplicate entry, skipping!")

        if fetchone:
            result = cur.fetchone()
        if fetchall:
            result = cur.fetchall()[0]
        else:
            result = None

        self.connection.commit()
        cur.close()
        return result

   
    # def __del__(self):
    #     self.close_connection(self.connection)


    def set_db_variables(self):
        self.username = os.getenv("remote_mysql_username")
        self.password = os.getenv("remote_mysql_password")
        self.ip_address = os.getenv("remote_mysql_ip_address")
        self.port = int(os.getenv("remote_mysql_port"))

    def createDatabase(self):
        print("Try 1")
        cursor, connection = self.connect_to_db()
        
        return cursor, connection
        # self.close_connection(connection)

    def close_connection(self, connection):
        # Close the database
        connection.close()

    
    def connect_to_db(self):
        config = {
                'user': f'{self.username}',
                'password': f'{self.password}',
	            'host': f'{self.ip_address}',
                'port': f'{self.port}',
	            'database': '', # Access the mysql itself
                }
        try:
            print("Connecting to Server")
            connection = mysql.connector.connect(**config)
            print("Connected")

            # Cursor which connects to database
            cursor = connection.cursor()
            
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")

            cursor.execute(f"USE {self.database}")

            cursor.close()

            print("Successfully connected to Storage")
            
            return connection

        except Exception as e:
            print(e)
            exit()

    
    def connect_to_table(self):
        cursor, connection = self.connect_to_db()

    def create_table(self):
        cursor, connection = self.connect_to_db()
        
        try:
            print("Creating a new table in Storage")
            # Create the tables
            sql_command = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                    date DATE PRIMARY KEY, 
                    mp4_link VARCHAR(1000) 
                    );"""
            
            # execute the statement
            cursor.execute(sql_command)

            print("Successfully created the new table")

        except sqlite3.OperationalError:
            print("Table already existing in Storage, skipping")
        except mysql.connector.errors.ProgrammingError:
            print("Table already existing in Storage, skipping")
        self.close_connection(connection)

    def add_episode(self, date: str, mp4_link: str):
        """Add episode mp4 link for given date"""
        cursor, connection = self.connect_to_db()
        
        print(f"Adding mp4 link for {date}")

        sql_command = f"""INSERT INTO {self.table_name} (date, mp4_link)
        VALUES (%s, %s);
        """
        
        try:
            # execute the statement
            cursor.execute(sql_command, params=(date, mp4_link,))

        except sqlite3.IntegrityError:
            print("Link already inside, skipping!")
        except mysql.connector.errors.IntegrityError as e: 
            if e.errno == 1062:
                print("Link already inside, skipping!")
        else:
            print("Successfully added mp4 link!")

        
        # To save the changes in the files. Never skip this.
        # If we skip this, nothing will be saved in the database.
        connection.commit()

        # Close the database
        self.close_connection(connection)

    def delete_episode(self, date):
        """Delete episode information of given date"""
        cursor, connection = self.connect_to_db()
        
        print(f"Removing mp4 link for {date}")

        # Converting to dict to stop SQL Injection
        sql_command = f"""DELETE FROM {self.table_name}
        WHERE date = (%s);
        """
        
        try:
            # execute the statement
            cursor.execute(sql_command, params=(date,))
            print("Successfully! Removed the mp4 link")

        except sqlite3.IntegrityError:
            print("Mp4 link not found in storage")
        
        # To save the changes in the files. Never skip this.
        # If we skip this, nothing will be saved in the database.
        connection.commit()

        # Close the database
        self.close_connection(connection)


    def get_mp4_link_of(self, date):
        """Get mp4 link of episode for given date"""
        cursor, connection = self.connect_to_db()
        
        sql_command = f"""
        SELECT mp4_link from {self.table_name} WHERE date = (%s);
        """
        cursor.execute(sql_command, (date,))

        # Get all rows matching the query
        mp4_link = cursor.fetchall()

        # Close the connection
        self.close_connection(connection)

        return mp4_link

    def update_mp4_link(self, date, mp4_link):
        """Change mp4 link of episode for given date"""
        cursor, connection = self.connect_to_db()
        
        print(f"Updating mp4 link for {date}")

        # Change episode mp4 link for given episode
        sql_command = f"""UPDATE {self.table_name}
        SET mp4_link = (%s) WHERE date = (%s);
        """
        
        # execute the statement
        cursor.execute(sql_command, params=(mp4_link, date,))

        print("Successfully updated the mp4 link!")
        
        # To save the changes in the files. Never skip this.
        # If we skip this, nothing will be saved in the database.
        connection.commit()

        # Close the database
        self.close_connection(connection)

