import json
from typing import ClassVar, Literal

from pydantic import BaseModel, Field


class Arguments(BaseModel):
    """
    Define arguments
    """
    lat: float = 0.0
    long: float = 0.0
    city: str = "pleasure_point"
    show_wave: bool = True
    show_large_wave: bool = False
    show_uv: bool = True
    show_height: bool = True
    show_direction: bool = True
    show_period: bool = True
    show_city: bool = True
    show_date: bool = True
    show_air_temp: bool = False
    show_wind_speed: bool = False
    show_wind_direction: bool = False
    json_output: bool = False
    show_rain_sum: bool = False
    show_precipitation_prob: bool = False
    unit: Literal["imperial", "metric"] = "imperial"
    decimal: int = Field(default=1, ge=0)
    forecast_days: int = Field(default=0, ge=0, le=7)
    color: str = "blue"
    gpt: bool = False


class ArgumentMappings(BaseModel):
    """
    Class for argument mappings with multiple aliases.
    """
    city: str = Field(
        default="pleasure_point",
        description="Name of the city you want weather data from",
    )
    show_wave: bool = Field(
        default=True,
        description="Show wave information",
    )
    show_large_wave: bool = Field(
        default=False,
        description="Show large wave information",
    )
    show_uv: bool = Field(
        default=True,
        description="Show UV information",
    )
    show_height: bool = Field(
        default=True,
        description="Show wave height information",
    )
    show_direction: bool = Field(
        default=True,
        description="Show wave direction information",
    )
    show_period: bool = Field(
        default=True,
        description="Show wave period information",
    )
    show_city: bool = Field(
        default=True,
        description="Show city information",
    )
    show_date: bool = Field(
        default=True,
        description="Show date information",
    )
    unit: Literal["imperial", "metric"] = Field(
        default="imperial",
        description="Set unit system",
    )
    json_output: bool = Field(
        default=False,
        description="Enable JSON output",
    )
    gpt: bool = Field(
        default=False,
        description="Enable GPT functionality",
    )
    show_air_temp: bool = Field(
        default=False,
        description="Show air temperature",
    )
    show_wind_speed: bool = Field(
        default=False,
        description="Show wind speed",
    )
    show_wind_direction: bool = Field(
        default=False,
        description="Show wind direction",
    )
    show_rain_sum: bool = Field(
        default=False,
        description="Show rain sum",
    )
    show_precipitation_prob: bool = Field(
        default=False,
        description="Show precipitation probability",
    )

    alias_map: ClassVar[dict[str, list[str]]] = {
        "city": ["loc", "location"],
        "show_wave": ["sw", "hide_wave", "hw"],
        "show_large_wave": ["slw"],
        "show_uv": ["suv", "hide_uv", "huv"],
        "show_height": ["sh", "hide_height", "hh"],
        "show_direction": ["sd", "hide_direction", "hdir"],
        "show_period": ["sp", "hide_period", "hp"],
        "show_city": ["sc", "hide_location", "hl"],
        "show_date": ["sdate", "hide_date", "hdate"],
        "unit": ["m", "metric"],
        "json_output": ["j", "json"],
        "gpt": ["g"],
        "show_air_temp": ["sat"],
        "show_wind_speed": ["sws"],
        "show_wind_direction": ["swd"],
        "show_rain_sum": ["srs"],
        "show_precipitation_prob": ["spp"]
    }

    @classmethod
    def generate_mappings(cls) -> dict[str, str]:
        """
        Flatten the alias map to create a mapping from each alias to the field
        name
        """
        mappings = {}
        for field_name, aliases in cls.alias_map.items():
            for alias in aliases:
                mappings[alias] = field_name
        return mappings

    @classmethod
    def parse_input(cls, data: dict) -> dict:
        alias_to_field_map = cls.generate_mappings()
        remapped_data = {}
        for key, value in data.items():
            field_name = alias_to_field_map.get(key, key)
            remapped_data[field_name] = value

        return remapped_data

    """
    TODO: write method to set location and update the dictionary
    """

    @classmethod
    def set_output_values(cls, args, arguments_dictionary: dict) -> dict:
        """
        Takes a list of command line arguments(args)
        and sets the appropriate values in the
        arguments_dictionary(show_wave = 1, etc).
        Returns the arguments_dictionary dict with the updated CLI args
        """
        # map of arguments to dictionary keys & values
        mappings = {
            "hide_wave": ("show_wave", False),
            "hw": ("show_wave", False),
            "show_large_wave": ("show_large_wave", True),
            "slw": ("show_large_wave", True),
            "hide_uv": ("show_uv", False),
            "huv": ("show_uv", False),
            "hide_height": ("show_height", False),
            "hh": ("show_height", False),
            "hide_direction": ("show_direction", False),
            "hdir": ("show_direction", False),
            "hide_period": ("show_period", False),
            "hp": ("show_period", False),
            "hide_location": ("show_city", False),
            "hl": ("show_city", False),
            "hide_date": ("show_date", False),
            "hdate": ("show_date", False),
            "metric": ("unit", "metric"),
            "m": ("unit", "metric"),
            "json": ("json_output", True),
            "j": ("json_output", True),
            "gpt": ("gpt", True),
            "g": ("gpt", True),
            "show_air_temp": ("show_air_temp", True),
            "sat": ("show_air_temp", True),
            "show_wind_speed": ("show_wind_speed", True),
            "sws": ("show_wind_speed", True),
            "show_wind_direction": ("show_wind_direction", True),
            "swd": ("show_wind_direction", True),
            "show_rain_sum": ("show_rain_sum", True),
            "srs": ("show_rain_sum", True),
            "show_precipitation_prob": ("show_precipitation_prob", True),
            "spp": ("show_precipitation_prob", True),
        }
        # Update arguments_dictionary based on the cli arguments in args
        # Ex: If "hide_uv" in args,
        # "show_uv" will be set to False in arguments_dictionary
        for arg in args:
            if arg in mappings:
                key, value = mappings[arg]
                arguments_dictionary[key] = value

        return arguments_dictionary
