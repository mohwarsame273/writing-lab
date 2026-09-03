"""Application header. Design-library components in play: Avatar, Badge,
Breadcrumbs (implicit via nav links), Tabs (mode toggle)."""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t
from writing_lab.components.mode_toggle import mode_toggle
from writing_lab.state.lab_state import LabState


def _brand() -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.icon("pen-line", size=18, color="white"),
            style=dict(background=t.PURPLE, border_radius="10px", padding="8px", display="flex"),
        ),
        rx.vstack(
            rx.text("Writing Lab", font_size="16px", font_weight="800", color=t.INK, line_height="1"),
            rx.text("practice, graded", font_size="11px", color=t.SLATE, line_height="1"),
            spacing="0",
            align_items="start",
        ),
        spacing="3",
        align_items="center",
    )


def _nav_link(label: str, href: str, icon: str) -> rx.Component:
    return rx.link(
        rx.hstack(rx.icon(icon, size=15), rx.text(label, font_size="13px", font_weight="600"),
                  spacing="2", align_items="center"),
        href=href,
        color=t.SLATE,
        style={"_hover": {"color": t.PURPLE}},
        text_decoration="none",
    )


def _metric(icon: str, value: rx.Var, colour: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=15, color=colour),
            rx.text(value, font_size="13px", font_weight="700", color=t.INK),
            spacing="2", align_items="center",
        ),
        style={**t.PILL, "background": f"{colour}14", "padding": "6px 12px"},
    )


def top_bar() -> rx.Component:
    return rx.box(
        rx.hstack(
            _brand(),
            rx.hstack(
                _nav_link("Dashboard", "/", "layout-dashboard"),
                _nav_link("Practice", "/practice", "target"),
                _nav_link("Free write", "/free-write", "pen-tool"),
                spacing="5",
                display=rx.breakpoints(initial="none", md="flex"),
            ),
            rx.spacer(),
            rx.hstack(
                rx.text("Casual", font_size="13px", font_weight="600", color=t.SLATE),
                rx.switch(checked=LabState.casual_mode, on_change=LabState.toggle_casual_mode, color_scheme="purple"),
                spacing="2",
                align_items="center",
            ),
            mode_toggle(),
            rx.cond(
                ~LabState.casual_mode,
                rx.hstack(
                    _metric("flame", LabState.streak, t.ORANGE),
                    _metric("zap", LabState.xp, t.AMBER),
                    spacing="4"
                ),
                rx.fragment()
            ),
            rx.avatar(fallback="MW", size="2", color_scheme="purple"),
            spacing="4",
            align_items="center",
            width="100%",
        ),
        style=dict(
            background="rgba(255,255,255,0.85)",
            backdrop_filter="blur(8px)",
            border_bottom=f"1px solid {t.BORDER}",
            padding="12px 28px",
            position="sticky",
            top="0",
            z_index="50",
        ),
        width="100%",
    )
