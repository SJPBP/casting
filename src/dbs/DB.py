from abc import ABC, abstractmethod
import os
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

class DB(ABC):
    def __init__(self) -> None:
        self.set_credentials()

        # This connected means there is db created on server
        self.connected = False

        # Create database if not exists already
        self.create_db()
    
    def set_credentials(self):
        try:
            self.username = os.getenv("mysql_username")
            self.password = os.getenv("mysql_password")
            self.ip_address = os.getenv("mysql_ip_address")
            self.db_name = os.getenv("mysql_db_name")
        except Exception as e:
            print("Failed Obtaining Database Credentials!")
            print(e)
            exit(-1)
    
    @contextmanager
    def connect_to_server(self):
        # This connected means there is db created on server
        config = {
                    'user': f'{self.username}',
                    'password': f'{self.password}',
                    'host': f'{self.ip_address}',
                    }
        if self.connected:
            # Created db with following {db_name} name
            config['database'] = f'{self.db_name}'
            
        else:
            # There is no db created on server
            config['database'] = ''

        connection = None

        try:
            connection = mysql.connector.connect(**config)
            if connection.is_connected():

                yield connection
        
        except Exception as e:
            print(e)

        except mysql.connector.errors.DatabaseError as e:
            if e.errno == 2003:
                print("Can't connect to MySQL server")

        finally:
            if connection is not None:
                connection.close()
            
    
    
    def create_db(self):
        try:
            with self.connect_to_server() as connection:

                print("Connecting to Database on Server...", end="")

                # Cursor which connects to database
                cursor = connection.cursor()
                
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")

                cursor.execute(f"USE {self.db_name}")
                
                # Created the db on server
                self.connected = True
                
                print("Succeed!")
                
        except Exception as e:
            print("Failed!")
            print(e)
    
    def execute(self, command, parameters = None):
        try:
            with self.connect_to_server() as connection:
                cursor = connection.cursor()
            
                if parameters is None:
                    cursor.execute(command)
                else:
                    cursor.execute(command, params=parameters)

                print("Succeed!")

        except Error as e:
            print("Failed!")
            print(e)


    
    @abstractmethod
    def create_table(self):
        pass
        

    # @abstractmethod
    # def validate_key(self, key: str):
    #     pass
    #
    # @abstractmethod
    # def validate_value(self, key: str, value: str):
    #     pass
