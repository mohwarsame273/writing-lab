try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

import os
from dotenv import load_dotenv
load_dotenv("variables.env")

import reflex as rx

# Reflex Cloud provides DATABASE_URL (or DB_URL if set manually). 
# We prevent silent SQLite fallback in production by checking REFLEX_ENV.
db_url = os.environ.get("DB_URL") or os.environ.get("DATABASE_URL")
if not db_url:
    if os.environ.get("REFLEX_ENV") == "production":
        raise RuntimeError("No DB_URL or DATABASE_URL provided. Refusing to fall back to SQLite in production.")
    db_url = "sqlite:///reflex.db"

config = rx.Config(
    app_name="writing_lab",
    db_url=db_url,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
