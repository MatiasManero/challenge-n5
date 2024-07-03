import os
from pydantic_settings import BaseSettings
from pydantic import Field

ENV_FILE = os.getenv("ENV_FILE", ".env")


class BaseSettingsModel(BaseSettings):
    """Base class for loading settings."""

    class Config:
        env_file = ENV_FILE


class APISettings(BaseSettingsModel):
    """Settings related with the FastAPI server"""
    host: str = Field(default="0.0.0.0", description="URL")
    port: int = Field(default=8080, description="PORT")

    class Config(BaseSettingsModel.Config):
        env_prefix = "api_"


class DBSettings(BaseSettingsModel):
    """Settings related with the FastAPI server"""
    url: str = Field(default="localhost", description="Database url")
    port: int = Field(default=5432, description="Database port")
    name: str = Field(default="n5db", description="Database name")
    username: str = Field(default="postgres", description="Database username")
    password: str = Field(default="postgres", description="Database password")
    echo: bool = Field(default=False, description="Echo database")

    class Config(BaseSettingsModel.Config):
        env_prefix = "api_db_"


class AuthorizacionSetting(BaseSettingsModel):
    """Setting para la generacion de token"""
    secret_key: str = Field(
        default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
        description="llave secreta del token"
    )
    algoritmo: str = Field(
        default="HS256",
        description="Algoritmo usado para encriptar/desencriptar el token"
    )
    tiempo_expiracion: int = Field(
        default=30,
        description="Tiempo en segundo que indica la vida util del token"
    )

    class Config(BaseSettingsModel.Config):
        env_prefix = "api_auth_"


api_settings = APISettings()
db_settings = DBSettings()
auth_setting = AuthorizacionSetting()
