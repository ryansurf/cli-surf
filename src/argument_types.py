# arguments.py
from typing import Literal

from pydantic import BaseModel, Field


class Arguments(BaseModel):
    """
    Define arguments
    """
    lat: float
    long: float
    city: str
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

    alias_map = {
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
        """""
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

    class Config:
        allow_population_by_field_name = True
