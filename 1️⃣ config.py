from pydantic_settings import BaseSettings
from typing import Literal
import structlog
import logging
from pathlib import Path

class Settings(BaseSettings):
    ENVIRONMENT: Literal["development", "production"] = "development"
    DEBUG: bool = True

    BROKER_TYPE: Literal["mock", "kite"] = "mock"
    KITE_API_KEY: str = ""
    KITE_API_SECRET: str = ""
    KITE_ACCESS_TOKEN: str = ""

    INITIAL_CAPITAL: float = 1_000_000.0
    MAX_POSITION_SIZE: float = 500_000.0
    MAX_TOTAL_EXPOSURE: float = 2_000_000.0

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()

# Logging
Path("logs").mkdir(exist_ok=True)

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()
