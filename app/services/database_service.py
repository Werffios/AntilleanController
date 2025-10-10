import logging
from app.database.mysql_manager import MySQLManager


class DatabaseService:
    def __init__(self):
        self.db_manager = MySQLManager()

    async def connect(self):
        await self.db_manager.create_connection()

    async def disconnect(self):
        await self.db_manager.close_connection()

    async def execute(self, query: str, params: tuple = None):
        try:
            result = await self.db_manager.execute(query, params)
            return result
        except Exception as e:
            logging.error(f"Error executing query: {str(e)}")
            raise

