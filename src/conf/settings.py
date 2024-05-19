
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    KAFKA_REQUEST_TOPIC: str
    KAFKA_RESPONSE_TOPIC: str

    model_config = SettingsConfigDict(
        env_file='conf/.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='allow' 
    )

settings = Settings.model_validate({})
