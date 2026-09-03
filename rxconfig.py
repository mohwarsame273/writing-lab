try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

import os
from dotenv import load_dotenv
load_dotenv("variables.env")

import reflex as rx

config = rx.Config(
    app_name="writing_lab",
    db_url="sqlite:///reflex.db",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
