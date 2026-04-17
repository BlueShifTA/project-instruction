from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Project Template API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"

    # Security: bind to loopback only by default.  In production deployments
    # behind a reverse proxy (nginx, Caddy) the proxy handles external exposure;
    # binding to 0.0.0.0 would unnecessarily expose the API port on all
    # interfaces.  Override with HOST=0.0.0.0 only when the container network
    # layout explicitly requires it (e.g. Docker bridge networking).
    host: str = "127.0.0.1"
    port: int = 8000

    # Security: explicit CORS origins only — no wildcards.  Wildcards are
    # rejected at startup by create_app().  Add your frontend origin here or
    # override via CORS_ORIGINS env var (comma-separated or JSON list).
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Scaling: cap the default thread pool used by run_in_executor.
    # None means Python's default (min(32, cpu_count+4)).  Set a positive int
    # to limit pool size and prevent thread exhaustion under high concurrency.
    # Example: WORKER_THREADS=8 for a 4-core container.
    worker_threads: int | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
