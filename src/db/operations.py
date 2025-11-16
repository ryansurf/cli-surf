from src.db.connection import db_manager
import logging


class SurfReportDatabaseOps:
    # Handles operations to the db
    def __init__(self):
        self.db = db_manager.connect()
        self.collection = self.db["surfReports"]

    def insert_report(self, report_document):
        try:
            rec = self.collection.insert_one(report_document)
            logging.info("Document inserted with ID: ", rec.inserted_id)
            return rec.inserted_id
        except Exception as e:
            logging.error("Error inserting to the db: ", e)
            return None
