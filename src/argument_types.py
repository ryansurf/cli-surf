# arguments.py
from typing import Dict, Literal

from pydantic import BaseModel, Field


class Arguments(BaseModel):
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
    show_wave: bool = Field(
        default=True,
        description="Show wave information",
        aliases=["sw", "hide_wave", "hw"]
    )
    show_large_wave: bool = Field(
        default=False,
        description="Show large wave information",
        aliases=["slw"]
    )
    show_uv: bool = Field(
        default=True,
        description="Show UV information",
        aliases=["suv", "hide_uv", "huv"]
    )
    show_height: bool = Field(
        default=True,
        description="Show wave height information",
        aliases=["sh", "hide_height", "hh"]
    )
    show_direction: bool = Field(
        default=True,
        description="Show wave direction information",
        aliases=["sd", "hide_direction", "hdir"]
    )
    show_period: bool = Field(
        default=True,
        description="Show wave period information",
        aliases=["sp", "hide_period", "hp"]
    )
    show_city: bool = Field(
        default=True,
        description="Show city information",
        aliases=["sc", "hide_location", "hl"]
    )
    show_date: bool = Field(
        default=True,
        description="Show date information",
        aliases=["sdate", "hide_date", "hdate"]
    )
    unit: Literal["imperial", "metric"] = Field(
        default="imperial",
        description="Set unit system",
        aliases=["m", "metric"]
    )
    json_output: bool = Field(
        default=False,
        description="Enable JSON output",
        aliases=["j", "json"]
    )
    gpt: bool = Field(
        default=False,
        description="Enable GPT functionality",
        aliases=["g"]
    )
    show_air_temp: bool = Field(
        default=False,
        description="Show air temperature",
        aliases=["sat"]
    )
    show_wind_speed: bool = Field(
        default=False,
        description="Show wind speed",
        aliases=["sws"]
        )
    show_wind_direction: bool = Field(
        default=False,
        description="Show wind direction",
        aliases=["swd"]
    )
    show_rain_sum: bool = Field(
        default=False,
        description="Show rain sum",
        aliases=["srs"]
    )
    show_precipitation_prob: bool = Field(
        default=False,
        description="Show precipitation probability",
        aliases=["spp"]
    )

    @classmethod
    def generate_mappings(cls) -> Dict[str, str]:
        mappings = {}
        for field_name, field in cls.model_fields.items():
            mappings[field_name] = field_name
            for alias in field.alias_priority or []:
                mappings[alias] = field_name
        return mappings

    class Config:
        allow_population_by_field_name = True
