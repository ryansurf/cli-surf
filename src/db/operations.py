import logging

from src.db.connection import db_manager


class SurfReportDatabaseOps:
    # Handles operations to the db
    def __init__(self):
        self.db = db_manager.connect()
        self.collection = self.db["surfReports"]

    def insert_report(self, report_document):
        try:
            rec = self.collection.insert_one(report_document)
            logging.info(f"Document inserted with ID: {rec.inserted_id}")
            return rec.inserted_id
        except Exception as e:
            logging.error(f"Error inserting to the db: {e}")
            return None
