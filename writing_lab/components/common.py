"""Small reusable primitives. Maps to Badge, Card and Icon in the design
library. Keep these dumb and presentational."""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t


def pill(label: str, colour: str = t.PURPLE, icon: str | None = None) -> rx.Component:
    """A Badge/Tag/Chip. Coloured, rounded, compact."""
    children = []
    if icon:
        children.append(rx.icon(icon, size=13))
    children.append(rx.text(label, font_size="12px", font_weight="600"))
    return rx.box(
        *children,
        style={
            **t.PILL,
            "color": colour,
            "background": f"{colour}1A",  # ~10% alpha
        },
    )


def stat_card(icon: str, value, label: str, colour: str = t.PURPLE) -> rx.Component:
    """A compact metric Card: big number, small label, tinted icon."""
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon(icon, size=20, color=colour),
                style=dict(
                    background=f"{colour}1A",
                    border_radius="12px",
                    padding="10px",
                    display="flex",
                ),
            ),
            rx.vstack(
                rx.text(value, font_size="22px", font_weight="800", color=t.INK, line_height="1"),
                rx.text(label, font_size="12px", color=t.SLATE),
                spacing="1",
                align_items="start",
            ),
            spacing="3",
            align_items="center",
        ),
        style=t.CARD,
        width="100%",
    )


def section_heading(text: str, sub=None) -> rx.Component:
    """`sub` may be a plain string or a Reflex Var (or None)."""
    if sub is None:
        sub_comp = rx.fragment()
    else:
        sub_comp = rx.cond(
            sub != "",
            rx.text(sub, font_size="13px", color=t.SLATE),
            rx.fragment(),
        )
    return rx.vstack(
        rx.text(text, font_size="15px", font_weight="700", color=t.INK),
        sub_comp,
        spacing="1",
        align_items="start",
        margin_bottom="4px",
    )


def severity_dot(colour: str) -> rx.Component:
    return rx.box(
        width="8px", height="8px", border_radius="999px", background=colour, flex_shrink="0"
    )


def divider() -> rx.Component:
    return rx.box(height="1px", background=t.BORDER, width="100%", margin_y="4px")
