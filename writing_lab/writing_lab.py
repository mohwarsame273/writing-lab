"""Writing Lab — app entry point.

A gamified, DataCamp-style writing-practice app. Academic and literary tracks,
short graded drills, a free-writing diagnostic mirror, XP, streaks and skill
mastery.

Architecture in one line: a framework-independent core (domain/, retrieval/,
services/) does all the thinking; this Reflex package (writing_lab/) is a
disposable UI shell. See ARCHITECTURE.md.
"""
from __future__ import annotations

try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

import reflex as rx

from writing_lab import theme as t
from writing_lab.pages.dashboard import dashboard
from writing_lab.pages.practice import practice
from writing_lab.pages.free_write import free_write
from writing_lab.state.lab_state import LabState

app = rx.App(
    theme=rx.theme(**t.theme_props()),
    style=t.APP_STYLE,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap",
    ],
)

# Load the first exercise when the practice page is opened.
app.add_page(dashboard, route="/", title="Writing Lab")
app.add_page(practice, route="/practice", title="Practice · Writing Lab", on_load=LabState.load_next)
app.add_page(free_write, route="/free-write", title="Free write · Writing Lab")
