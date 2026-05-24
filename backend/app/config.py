from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Providers
    TWELVE_DATA_API_KEY: str = ""
    ALPHA_VANTAGE_API_KEY: str = ""
    FINNHUB_API_KEY: str = ""
    POLYGON_API_KEY: str = ""
    TRADING_ECONOMICS_KEY: str = ""
    NEWS_API_KEY: str = ""

    # DB / cache
    DATABASE_URL: str = "postgresql+asyncpg://forex:forex@postgres:5432/forex"
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    # Auth
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALLOW_ANONYMOUS_AUTH: bool = False
    APP_ENV: str = "local"

    # HTTP / CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Notifications
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    DISCORD_WEBHOOK_URL: str = ""

    # Universe
    PAIRS: list[str] = [
        "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD",
        "USD/CAD", "USD/CHF", "NZD/USD", "XAU/USD",
    ]
    TIMEFRAMES: list[str] = ["1min", "5min", "15min", "30min", "1h", "4h", "1day"]

    # Signal discipline
    MIN_SIGNAL_CONFIDENCE: float = 60.0
    SIGNAL_COOLDOWN_MINUTES: int = 30
    ALLOW_SYNTHETIC_SIGNALS: bool = False
    DEFAULT_SLIPPAGE_PIPS: float = 0.5
    COMMISSION_PER_TRADE: float = 0.0
    XAU_PIP_SIZE: float = 0.1
    DEFAULT_SPREAD_PIPS: dict[str, float] = {
        "EUR/USD": 1.0,
        "GBP/USD": 1.3,
        "USD/JPY": 1.2,
        "XAU/USD": 3.0,
    }


settings = Settings()
