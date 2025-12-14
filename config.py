from pathlib import Path
import json
from pydantic.v1 import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str
    model_config = SettingsConfigDict(env_file=".env")
settings = Settings()
class BusinessRules(BaseModel):
    max_accounts_per_user: int
    allow_account_creation: bool
class Settings(BaseModel):
    database_url: str
    business_rules: BusinessRules
def load_settings() -> Settings:
    config_path = Path("config.json")
    if not config_path.exists():
        raise FileNotFoundError("config.json not found!")
    with open(config_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    return Settings(**config_data)
