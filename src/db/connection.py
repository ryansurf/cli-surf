from pymongo import MongoClient
import logging

from src.settings import DatabaseSettings


class Database:
    # Manages the MongoDB connection
    def __init__(self):
        settings = DatabaseSettings()
        self.db_uri = settings.DB_URI
        self.client = None
        self.db = None

    def connect(self, db_name="surf"):
        if not self.client:
            try:
                self.client = MongoClient(self.db_uri)
                self.db = self.client[db_name]
                logging.info("Database connected successfully")
            except Exception as e:
                logging.warning("Could not connect to MongoDB: ", e)
                raise
        return self.db

    def disconnect(self):
        # Close the connection
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            logging.info("Database connection closed")


db_manager = Database()
