import logging

from src.db.connection import db_manager

logger = logging.getLogger(__name__)


class SurfReportDatabaseOps:
    """Handles surf report operations against the database."""

    def __init__(self):
        self.db = db_manager.connect()
        self.collection = self.db["surfReports"]

    def insert_report(self, report_document):
        try:
            rec = self.collection.insert_one(report_document)
            logger.info("Document inserted with ID: %s", rec.inserted_id)
            return rec.inserted_id
        except Exception as e:
            logger.error("Error inserting to the db: %s", e)
            raise
