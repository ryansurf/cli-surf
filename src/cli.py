"""
Main module
"""

import argparse
import logging
import sys

from src import api, helper, settings
from src.db import operations

logger = logging.getLogger(__name__)


class SurfReport:
    """
    Orchestrates fetching, persisting, and displaying a surf report.

    Initializes settings and optional database connection on construction,
    then exposes a run() method to execute a full report cycle.
    """

    def __init__(self) -> None:
        gpt_env = settings.GPTSettings()
        self.gpt_prompt = gpt_env.GPT_PROMPT
        self.gpt_info = (gpt_env.API_KEY, gpt_env.GPT_MODEL)
        self.db_handler = self._init_db()

    @staticmethod
    def _init_db() -> operations.SurfReportDatabaseOps | None:
        """Initializes the database handler, or returns None if unavailable."""
        db_env = settings.DatabaseSettings()
        if not db_env.DB_URI:
            return None
        try:
            return operations.SurfReportDatabaseOps()
        except Exception:
            logger.warning(
                "Could not connect to database. Reports will not be saved."
            )
            return None

    def run(
        self,
        lat: float | None = None,
        long: float | None = None,
        args: list[str] | None = None,
    ):
        """
        Fetches surf data for the given coordinates or parsed location,
        optionally persists the report, and renders output.

        Returns the ocean data dict, plus the GPT response when in text mode.
        """
        args = helper.separate_args(args if args is not None else sys.argv)

        location = api.separate_args_and_get_location(args)
        city, loc_lat, loc_long = helper.set_location(location)

        if lat is None or long is None:
            lat, long = loc_lat, loc_long

        arguments = helper.arguments_dictionary(lat, long, city, args)
        ocean_data_dict = api.gather_data(lat, long, arguments)

        self._save_report(ocean_data_dict)
        return self._render_output(ocean_data_dict, arguments)

    def _save_report(self, ocean_data_dict) -> None:
        """Persists the report to the database if a handler is available."""
        if self.db_handler:
            try:
                self.db_handler.insert_report(ocean_data_dict)
            except Exception:
                logger.warning("Failed to save report to database.")

    def _render_output(self, ocean_data_dict, arguments):
        """Renders JSON or human-readable output based on arguments."""
        if not arguments["json_output"]:
            response = helper.print_outputs(
                ocean_data_dict, arguments, self.gpt_prompt, self.gpt_info
            )
            return ocean_data_dict, response
        helper.json_output(ocean_data_dict)
        return ocean_data_dict


def run(lat=None, long=None, args=None):
    """Module-level entry point; delegates to SurfReport for convenience."""
    return SurfReport().run(lat=lat, long=long, args=args)


# FOR CLI TOOL USAGE (no server, invoked via cli)
def _build_args_string(ns):
    tokens = []
    if ns.location:
        tokens.append(f"location={ns.location.replace(' ', '_')}")
    if ns.forecast is not None:
        tokens.append(f"forecast={ns.forecast}")
    if ns.decimal is not None:
        tokens.append(f"decimal={ns.decimal}")
    if ns.color:
        tokens.append(f"color={ns.color}")
    if ns.metric:
        tokens.append("metric")
    if ns.imperial:
        tokens.append("imperial")
    flag_map = {
        "json": "json",
        "gpt": "gpt",
        "hide_wave": "hide_wave",
        "hide_uv": "hide_uv",
        "hide_height": "hide_height",
        "hide_direction": "hide_direction",
        "hide_period": "hide_period",
        "hide_location": "hide_location",
        "hide_date": "hide_date",
        "show_large_wave": "show_large_wave",
        "show_past_uv": "show_past_uv",
        "show_height_history": "show_height_history",
        "show_direction_history": "show_direction_history",
        "show_period_history": "show_period_history",
        "show_air_temp": "show_air_temp",
        "show_wind_speed": "show_wind_speed",
        "show_wind_direction": "show_wind_direction",
        "show_rain_sum": "show_rain_sum",
        "show_precipitation_prob": "show_precipitation_prob",
        "show_cloud_cover": "show_cloud_cover",
        "show_visibility": "show_visibility",
    }
    for attr, token in flag_map.items():
        if getattr(ns, attr, False):
            tokens.append(token)
    return ",".join(tokens)


def cli_main():
    parser = argparse.ArgumentParser(
        prog="surf", description="Get a surf report."
    )
    parser.add_argument("--location", "--loc", metavar="LOCATION")
    parser.add_argument("--forecast", "--fc", type=int, metavar="DAYS")
    parser.add_argument("--decimal", "--dec", type=int, metavar="N")
    parser.add_argument("--color", "-c", metavar="COLOR")
    unit = parser.add_mutually_exclusive_group()
    unit.add_argument("--metric", "-m", action="store_true")
    unit.add_argument("--imperial", "-i", action="store_true")
    parser.add_argument("--json", "-j", action="store_true")
    parser.add_argument("--gpt", "-g", action="store_true")
    parser.add_argument("--hide-wave", action="store_true")
    parser.add_argument("--hide-uv", action="store_true")
    parser.add_argument("--hide-height", action="store_true")
    parser.add_argument("--hide-direction", action="store_true")
    parser.add_argument("--hide-period", action="store_true")
    parser.add_argument("--hide-location", action="store_true")
    parser.add_argument("--hide-date", action="store_true")
    parser.add_argument("--show-large-wave", action="store_true")
    parser.add_argument("--show-past-uv", action="store_true")
    parser.add_argument("--show-height-history", action="store_true")
    parser.add_argument("--show-direction-history", action="store_true")
    parser.add_argument("--show-period-history", action="store_true")
    parser.add_argument("--show-air-temp", action="store_true")
    parser.add_argument("--show-wind-speed", action="store_true")
    parser.add_argument("--show-wind-direction", action="store_true")
    parser.add_argument("--show-rain-sum", action="store_true")
    parser.add_argument("--show-precipitation-prob", action="store_true")
    parser.add_argument("--show-cloud-cover", action="store_true")
    parser.add_argument("--show-visibility", action="store_true")
    ns = parser.parse_args()
    run(args=_build_args_string(ns))


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    cli_main()
