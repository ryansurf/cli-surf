"""
Main module
"""

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


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    run()
