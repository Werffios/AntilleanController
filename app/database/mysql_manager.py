import logging
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import mysql.connector.aio
from mysql.connector import Error

load_dotenv()

class MySQLManager:
    def __init__(self):
        mysql_url = os.getenv("MYSQL_URL", "mysql://root:@localhost:3306/testdb")
        parsed = urlparse(mysql_url)
        query_params = parse_qs(parsed.query)

        self.host = parsed.hostname or "192.168.10.4"
        self.port = parsed.port or 3306
        self.user = parsed.username or "root"
        self.password = parsed.password or "rDEAkeRYphYptoTHLopicOmeL"
        self.database = parsed.path.lstrip('/') or "antillean_app"
        self.autocommit = query_params.get('autocommit', ['true'])[0].lower() == 'true'
        self.connection = None

    async def create_connection(self):
        logging.info(f"Attempting to connect to MySQL database {self.database} at {self.host}:{self.port} with user {self.user}, database={self.database} and password={self.password}")
        try:
            self.connection = await mysql.connector.aio.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=self.autocommit
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos MySQL")
        except Error as e:
            logging.error(f"Unexpected error in connect_db: {str(e)}")
            raise

    async def close_connection(self):
        try:
            if self.connection is not None and self.connection.is_connected():
                await self.connection.close()
                print("Conexión cerrada")
        except Error as e:
            logging.error(f"Unexpected error in close_db: {str(e)}")

    async def execute(self, query, params=None):
        if self.connection is None or not self.connection.is_connected():
            raise Exception("Database connection is not established.")
        cursor = await self.connection.cursor(dictionary=True)
        try:
            await cursor.execute(query, params or ())
            print("Query executed successfully", query, self.autocommit)
            return await cursor.fetchall()
        except Error as e:
            logging.error(f"Error executing query: {e}")
            raise
        finally:
            await cursor.close()