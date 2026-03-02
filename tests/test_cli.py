"""
Tests for cli.py
"""

import logging
from unittest.mock import Mock

from src.cli import SurfReport, run
from src.helper import DEFAULT_ARGUMENTS

_LAT = 10.0
_LONG = 20.0

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_settings(
    mocker, *, db_uri="", gpt_prompt="prompt", api_key="", model="gpt-3.5"
):
    """Patch both settings classes used by SurfReport.__init__."""
    mocker.patch(
        "src.cli.settings.GPTSettings",
        return_value=Mock(
            GPT_PROMPT=gpt_prompt, API_KEY=api_key, GPT_MODEL=model
        ),
    )
    mocker.patch(
        "src.cli.settings.DatabaseSettings",
        return_value=Mock(DB_URI=db_uri),
    )


def _make_arguments(**overrides):
    """Return a full arguments dict suitable for run() calls."""
    args = {
        **DEFAULT_ARGUMENTS,
        "lat": 36.97,
        "long": -122.03,
        "city": "Santa Cruz",
        "decimal": 1,
        "forecast_days": 0,
        "color": "blue",
    }
    args.update(overrides)
    return args


def _mock_run_pipeline(mocker, arguments, ocean_data):
    """Patch all I/O helpers called inside SurfReport.run()."""
    mocker.patch("src.cli.helper.separate_args", return_value=[])
    mocker.patch(
        "src.cli.api.separate_args_and_get_location",
        return_value={"city": "Santa Cruz", "lat": 36.97, "long": -122.03},
    )
    mocker.patch(
        "src.cli.helper.set_location",
        return_value=("Santa Cruz", 36.97, -122.03),
    )
    mocker.patch("src.cli.helper.arguments_dictionary", return_value=arguments)
    mocker.patch("src.cli.api.gather_data", return_value=ocean_data)


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------


def test_init_stores_gpt_settings(mocker):
    """SurfReport reads GPT prompt and model from settings on construction."""
    _mock_settings(mocker, gpt_prompt="surf report", api_key="", model="gpt-4")
    report = SurfReport()
    assert report.gpt_prompt == "surf report"
    assert report.gpt_info == ("", "gpt-4")


def test_init_db_none_when_uri_empty(mocker):
    """db_handler is None when DB_URI is not configured."""
    _mock_settings(mocker, db_uri="")
    assert SurfReport().db_handler is None


def test_init_db_connected_when_uri_set(mocker):
    """db_handler is the SurfReportDatabaseOps instance when DB_URI is set."""
    _mock_settings(mocker, db_uri="mongodb://localhost")
    mock_handler = Mock()
    mocker.patch(
        "src.cli.operations.SurfReportDatabaseOps", return_value=mock_handler
    )
    assert SurfReport().db_handler is mock_handler


def test_init_db_logs_warning_and_returns_none_on_failure(mocker, caplog):
    """db_handler is None and a warning is logged when DB connection fails."""
    _mock_settings(mocker, db_uri="mongodb://localhost")
    mocker.patch(
        "src.cli.operations.SurfReportDatabaseOps",
        side_effect=Exception("timeout"),
    )
    with caplog.at_level(logging.WARNING, logger="src.cli"):
        report = SurfReport()
    assert report.db_handler is None
    assert "Could not connect to database" in caplog.text


# ---------------------------------------------------------------------------
# run() – text mode
# ---------------------------------------------------------------------------


def test_run_text_mode_returns_dict_and_gpt_response(mocker):
    """run() in text mode returns (ocean_data_dict, gpt_response)."""
    ocean_data = {"Height": 3.0, "Lat": 36.97, "Long": -122.03}
    arguments = _make_arguments()
    _mock_settings(mocker)
    _mock_run_pipeline(mocker, arguments, ocean_data)
    mock_print = mocker.patch(
        "src.cli.helper.print_outputs", return_value="surf is fun"
    )

    result = SurfReport().run()

    assert result == (ocean_data, "surf is fun")
    mock_print.assert_called_once()


def test_run_json_mode_returns_dict_only(mocker):
    """run() in JSON mode returns only the ocean data dict."""
    ocean_data = {"Height": 3.0, "Lat": 36.97, "Long": -122.03}
    arguments = _make_arguments(json_output=True)
    _mock_settings(mocker)
    _mock_run_pipeline(mocker, arguments, ocean_data)
    mock_json = mocker.patch("src.cli.helper.json_output")

    result = SurfReport().run()

    assert result is ocean_data
    mock_json.assert_called_once_with(ocean_data)


def test_run_uses_explicit_lat_long_over_resolved(mocker):
    """Caller-supplied lat/long overrides the location resolved from args."""
    ocean_data = {"Height": 3.0, "Lat": _LAT, "Long": _LONG}
    arguments = _make_arguments(lat=_LAT, long=_LONG)
    _mock_settings(mocker)
    _mock_run_pipeline(mocker, arguments, ocean_data)
    mock_gather = mocker.patch(
        "src.cli.api.gather_data", return_value=ocean_data
    )
    mocker.patch("src.cli.helper.print_outputs", return_value=None)

    SurfReport().run(lat=_LAT, long=_LONG)

    call_lat, call_long = mock_gather.call_args[0][:2]
    assert call_lat == _LAT
    assert call_long == _LONG


# ---------------------------------------------------------------------------
# _save_report
# ---------------------------------------------------------------------------


def test_save_report_calls_insert_when_handler_set(mocker):
    """_save_report delegates to the db_handler when one is configured."""
    _mock_settings(mocker, db_uri="mongodb://localhost")
    mock_handler = Mock()
    mocker.patch(
        "src.cli.operations.SurfReportDatabaseOps", return_value=mock_handler
    )
    data = {"Height": 3}
    SurfReport()._save_report(data)
    mock_handler.insert_report.assert_called_once_with(data)


def test_save_report_is_noop_without_handler(mocker):
    """_save_report does nothing when db_handler is None."""
    _mock_settings(mocker)
    SurfReport()._save_report({"Height": 3})  # must not raise


# ---------------------------------------------------------------------------
# Module-level run() shim
# ---------------------------------------------------------------------------


def test_module_run_delegates_to_surf_report(mocker):
    """The module-level run() creates a SurfReport and forwards all args."""
    mock_instance = Mock()
    mock_instance.run.return_value = {"ocean": "data"}
    mock_class = mocker.patch("src.cli.SurfReport", return_value=mock_instance)

    result = run(lat=1.0, long=2.0, args=["placeholder", "json"])

    mock_class.assert_called_once()
    mock_instance.run.assert_called_once_with(
        lat=1.0, long=2.0, args=["placeholder", "json"]
    )
    assert result == {"ocean": "data"}
