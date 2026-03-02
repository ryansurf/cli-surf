"""
Tests for src/db/connection.py and src/db/operations.py
"""

import logging
from unittest.mock import MagicMock

import pytest

from src.db.connection import Database
from src.db.operations import SurfReportDatabaseOps

# ---------------------------------------------------------------------------
# Database (connection.py)
# ---------------------------------------------------------------------------


def _db_with_mocked_settings(mocker, db_uri="mongodb://localhost"):
    """Return a Database instance with settings and MongoClient mocked."""
    mock_client = MagicMock()
    mock_cls = mocker.patch(
        "src.db.connection.MongoClient", return_value=mock_client
    )
    mocker.patch(
        "src.db.connection.DatabaseSettings",
        return_value=MagicMock(DB_URI=db_uri),
    )
    return Database(), mock_client, mock_cls


def test_connect_creates_mongo_client(mocker):
    """connect() creates a MongoClient and returns the named database."""
    db, mock_client, _ = _db_with_mocked_settings(mocker)
    result = db.connect("surf")
    assert result is mock_client["surf"]


def test_connect_reuses_existing_connection(mocker):
    """connect() does not create a second MongoClient if already connected."""
    db, _, mock_cls = _db_with_mocked_settings(mocker)
    db.connect()
    db.connect()  # second call — should not instantiate another client
    mock_cls.assert_called_once()


def test_connect_logs_warning_and_reraises_on_failure(mocker, caplog):
    """connect() logs a warning and re-raises when MongoClient fails."""
    mocker.patch(
        "src.db.connection.MongoClient",
        side_effect=Exception("connection refused"),
    )
    mocker.patch(
        "src.db.connection.DatabaseSettings",
        return_value=MagicMock(DB_URI="mongodb://localhost"),
    )
    db = Database()
    with caplog.at_level(logging.WARNING, logger="src.db.connection"):
        with pytest.raises(Exception, match="connection refused"):
            db.connect()
    assert "Could not connect to MongoDB" in caplog.text


def test_disconnect_closes_client_and_clears_state(mocker):
    """disconnect() closes the MongoClient and resets client/db to None."""
    db, mock_client, _ = _db_with_mocked_settings(mocker)
    db.connect()
    db.disconnect()
    mock_client.close.assert_called_once()
    assert db.client is None
    assert db.db is None


def test_disconnect_is_noop_when_not_connected(mocker):
    """disconnect() does nothing when no client exists."""
    mocker.patch(
        "src.db.connection.DatabaseSettings",
        return_value=MagicMock(DB_URI=""),
    )
    Database().disconnect()  # must not raise


# ---------------------------------------------------------------------------
# SurfReportDatabaseOps (operations.py)
# ---------------------------------------------------------------------------


def test_init_connects_and_sets_collection(mocker):
    """SurfReportDatabaseOps.__init__ connects and sets self.collection."""
    mock_col = MagicMock()
    mock_db = MagicMock()
    mock_db.__getitem__.return_value = mock_col
    mocker.patch("src.db.operations.db_manager").connect.return_value = mock_db

    ops = SurfReportDatabaseOps()

    assert ops.collection is mock_col


def _make_ops(mocker):
    """Return SurfReportDatabaseOps with bypassed __init__ and mocked col."""
    mocker.patch.object(SurfReportDatabaseOps, "__init__", return_value=None)
    ops = SurfReportDatabaseOps()
    mock_col = MagicMock()
    ops.collection = mock_col
    return ops, mock_col


def test_insert_report_returns_inserted_id(mocker):
    """insert_report returns the inserted document ID on success."""
    ops, mock_col = _make_ops(mocker)
    mock_col.insert_one.return_value = MagicMock(inserted_id="abc123")

    result = ops.insert_report({"Height": 3})

    assert result == "abc123"
    mock_col.insert_one.assert_called_once_with({"Height": 3})


def test_insert_report_logs_error_and_reraises_on_failure(mocker, caplog):
    """insert_report logs an error and re-raises the exception on failure."""
    ops, mock_col = _make_ops(mocker)
    mock_col.insert_one.side_effect = Exception("write failed")

    with caplog.at_level(logging.ERROR, logger="src.db.operations"):
        with pytest.raises(Exception, match="write failed"):
            ops.insert_report({"Height": 3})

    assert "Error inserting to the db" in caplog.text
