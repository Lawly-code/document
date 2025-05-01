from dataclasses import dataclass, field

from pydantic_settings import BaseSettings, SettingsConfigDict


class CiphersSettings(BaseSettings):
    salt: str

    model_config = SettingsConfigDict(
        env_prefix="cipher_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class JWTSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    max_user_sessions: int

    model_config = SettingsConfigDict(
        env_prefix="jwt_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@dataclass
class Settings:
    cipher_settings: CiphersSettings = field(default_factory=CiphersSettings)
    jwt_settings: JWTSettings = field(default_factory=JWTSettings)


settings = Settings()
