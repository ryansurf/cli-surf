import logging

from pymongo import MongoClient

from src.settings import DatabaseSettings

logger = logging.getLogger(__name__)


class Database:
    """Manages the MongoDB connection."""

    def __init__(self):
        settings = DatabaseSettings()
        self.db_uri = settings.DB_URI
        self.client = None
        self.db = None

    def connect(self, db_name="surf"):
        if not self.client:
            try:
                self.client = MongoClient(self.db_uri, serverSelectionTimeoutMS=100)
                self.db = self.client[db_name]
                logger.info("Database connected successfully")
            except Exception as e:
                logger.warning("Could not connect to MongoDB: %s", e)
                raise
        return self.db

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            logger.info("Database connection closed")


db_manager = Database()
