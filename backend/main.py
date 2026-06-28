"""Uvicorn entrypoint for the Svigl backend."""

import uvicorn

from app.config import get_settings
from app.create_app import create_app

app = create_app()


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
