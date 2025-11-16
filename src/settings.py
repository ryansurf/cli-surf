from pathlib import Path
from typing import Literal, Union

from pydantic import EmailStr, Field, IPvAnyAddress
from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    """
    Base class for defining common settings.
    model_config (SettingsConfigDict)Configuration dictionary
    for specifying the settings file and encoding.
    """

    model_config = SettingsConfigDict(
        env_file=f"{Path(__file__).parent.parent}/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class ServerSettings(CommonSettings):
    """
    Class for defining server env settings.
    """

    PORT: int = Field(default=8000)
    IP_ADDRESS: Union[IPvAnyAddress | Literal["localhost"]] = Field(
        default="localhost"
    )
    DEBUG: bool = Field(default=True)


class EmailSettings(ServerSettings):
    """
    Class for defining email env settings.
    """

    SMTP_SERVER: str = Field(default="smtp.gmail.com")  # default gmail server
    SMTP_PORT: int = Field(default=587)  # default 587
    EMAIL: EmailStr  # required
    EMAIL_PW: str  # required
    EMAIL_RECEIVER: EmailStr  # required
    COMMAND: str = Field(
        default_factory=lambda cls: f"{cls.IP_ADDRESS}:{cls.PORT}"
    )
    SUBJECT: str = Field(default="Surf Report")


class GPTSettings(CommonSettings):
    """
    Class for defining server env settings.
    """

    GPT_PROMPT: str = Field(
        default="""
        With this surf data, give me a short estimate on how the surf
        might be at the specified location with the given data.
        Recommend another nearby spot to surf at if you think it may be better.
    """
    )

    API_KEY: str = Field(default="")
    GPT_MODEL: str = Field(default="gpt-3.5-turbo")


class DatabaseSettings(CommonSettings):
    """
    Class for defining database env settings
    """

    DB_URI: str
