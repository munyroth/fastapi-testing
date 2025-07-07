from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USERNAME: str = ""
    DB_PASSWORD: str = ""
    DB_DATABASE: str = ""
    DB_HOST: str = ""
    DB_PORT: str = ""
    JWT_ISSUER: str = ""
    JWT_ALGORITHM: str = ""
    JWT_PRIVATE_KEY_PATH: str = ""
    JWT_PUBLIC_KEY_PATH: str = ""
    REDIS_URL: str = ""

    # These will be loaded manually after initialization
    JWT_PRIVATE_KEY: str = ""
    JWT_PUBLIC_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=('.env', '.env.prod'),
        env_file_encoding='utf-8',
        extra="ignore"
    )

    def load_keys(self):
        self.JWT_PRIVATE_KEY = Path(self.JWT_PRIVATE_KEY_PATH).read_text()
        self.JWT_PUBLIC_KEY = Path(self.JWT_PUBLIC_KEY_PATH).read_text()


settings = Settings()
settings.load_keys()
