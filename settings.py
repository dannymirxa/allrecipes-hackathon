
from dataclasses import dataclass

@dataclass
class app_env_settings_docker:
    POSTGRES_USER: str = "myuser"
    POSTGRES_PASSWORD: str = "mypassword"
    POSTGRES_HOST: str = "food-postgres"
    POSTGRES_PORT: str = 5432
    POSTGRES_DB: str = "food"

@dataclass
class app_env_settings_local:
    POSTGRES_USER: str = "myuser"
    POSTGRES_PASSWORD: str = "mypassword"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = 5435
    POSTGRES_DB: str = "food"