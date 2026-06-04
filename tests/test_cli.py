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


def test_build_args_string():
    from src.cli import _build_args_string
    class DummyNamespace:
        def __init__(self, **kwargs):
            self.location = kwargs.get("location", None)
            self.forecast = kwargs.get("forecast", None)
            self.decimal = kwargs.get("decimal", None)
            self.color = kwargs.get("color", None)
            self.metric = kwargs.get("metric", False)
            self.imperial = kwargs.get("imperial", False)
            self.json = kwargs.get("json", False)
            self.gpt = kwargs.get("gpt", False)
            self.hide_wave = kwargs.get("hide_wave", False)
            self.hide_uv = kwargs.get("hide_uv", False)
            self.hide_height = kwargs.get("hide_height", False)
            self.hide_direction = kwargs.get("hide_direction", False)
            self.hide_period = kwargs.get("hide_period", False)
            self.hide_location = kwargs.get("hide_location", False)
            self.hide_date = kwargs.get("hide_date", False)
            self.show_large_wave = kwargs.get("show_large_wave", False)
            self.show_past_uv = kwargs.get("show_past_uv", False)
            self.show_height_history = kwargs.get("show_height_history", False)
            self.show_direction_history = kwargs.get("show_direction_history", False)
            self.show_period_history = kwargs.get("show_period_history", False)
            self.show_air_temp = kwargs.get("show_air_temp", False)
            self.show_wind_speed = kwargs.get("show_wind_speed", False)
            self.show_wind_direction = kwargs.get("show_wind_direction", False)
            self.show_rain_sum = kwargs.get("show_rain_sum", False)
            self.show_precipitation_prob = kwargs.get("show_precipitation_prob", False)
            self.show_cloud_cover = kwargs.get("show_cloud_cover", False)
            self.show_visibility = kwargs.get("show_visibility", False)

    ns = DummyNamespace(
        location="San Francisco",
        forecast=3,
        decimal=2,
        color="red",
        metric=True,
        json=True,
        show_large_wave=True
    )
    res = _build_args_string(ns)
    assert "location=San_Francisco" in res
    assert "forecast=3" in res
    assert "decimal=2" in res
    assert "color=red" in res
    assert "metric" in res
    assert "json" in res
    assert "show_large_wave" in res

    all_true_kwargs = {
        "location": "A",
        "forecast": 1,
        "decimal": 0,
        "color": "blue",
        "metric": True,
        "imperial": True,
        "json": True,
        "gpt": True,
        "hide_wave": True,
        "hide_uv": True,
        "hide_height": True,
        "hide_direction": True,
        "hide_period": True,
        "hide_location": True,
        "hide_date": True,
        "show_large_wave": True,
        "show_past_uv": True,
        "show_height_history": True,
        "show_direction_history": True,
        "show_period_history": True,
        "show_air_temp": True,
        "show_wind_speed": True,
        "show_wind_direction": True,
        "show_rain_sum": True,
        "show_precipitation_prob": True,
        "show_cloud_cover": True,
        "show_visibility": True,
    }
    ns_all = DummyNamespace(**all_true_kwargs)
    res_all = _build_args_string(ns_all)
    for flag in all_true_kwargs.keys():
        if flag == "location":
            assert "location=A" in res_all
        elif flag in ("forecast", "decimal", "color"):
            assert f"{flag}=" in res_all
        else:
            assert flag in res_all


def test_cli_main(mocker):
    from src.cli import cli_main
    mocker.patch("sys.argv", [
        "surf",
        "--location", "Santa Cruz",
        "--forecast", "3",
        "--decimal", "1",
        "--color", "blue",
        "--metric",
        "--json",
        "--show-large-wave"
    ])
    mock_run = mocker.patch("src.cli.run")
    cli_main()
    mock_run.assert_called_once()
    _, kwargs = mock_run.call_args
    assert "args" in kwargs
    args_str = kwargs["args"]
    assert "location=Santa_Cruz" in args_str
    assert "forecast=3" in args_str
    assert "decimal=1" in args_str
    assert "color=blue" in args_str
    assert "metric" in args_str
    assert "json" in args_str
    assert "show_large_wave" in args_str

