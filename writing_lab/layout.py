"""Shared page shell."""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t
from writing_lab.components.top_bar import top_bar


def shell(*content: rx.Component, max_width: str = "1080px") -> rx.Component:
    return rx.box(
        top_bar(),
        rx.box(
            rx.vstack(*content, spacing="6", width="100%", align_items="stretch"),
            max_width=max_width,
            margin="0 auto",
            padding=rx.breakpoints(initial="20px 16px", md="32px 28px"),
            width="100%",
        ),
        background=t.BG,
        min_height="100vh",
        width="100%",
    )
