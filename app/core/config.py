from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    hf_token: str
    hf_model: str

    jwt_secret: str
    database_url: str
    redis_url: str


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()