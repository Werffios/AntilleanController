import logging
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

class MongoManager:
    def __init__(self):
        self.mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017/testdb")
        parsed = urlparse(self.mongo_url)
        self.database_name = parsed.path.lstrip('/') or "testdb"
        self.client = None
        self.db = None

    async def create_connection(self):
        try:
            self.client = AsyncIOMotorClient(self.mongo_url)
            self.db = self.client[self.database_name]
            await self.client.admin.command('ping')
            print("Conexión exitosa a la base de datos MongoDB")
        except Exception as e:
            logging.error(f"Unexpected error in connect_mongo: {str(e)}")

    async def close_connection(self):
        try:
            if self.client is not None:
                self.client.close()
                print("Conexión cerrada")
        except Exception as e:
            logging.error(f"Unexpected error in close_mongo: {str(e)}")

    async def get_collection(self, collection_name):
        if self.db is None:
            raise Exception("Database connection is not established.")
        return self.db[collection_name]