"""The Academic <-> Literary toggle. More than a colour swap: switching it
reloads the exercise bank and re-weights grading (see LabState.set_mode)."""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t
from writing_lab.state.lab_state import LabState


def _segment(label: str, icon: str, active: rx.Var, on_click) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=15),
            rx.text(label, font_size="13px", font_weight="600"),
            spacing="2",
            align_items="center",
        ),
        on_click=on_click,
        cursor="pointer",
        padding="7px 14px",
        border_radius="10px",
        color=rx.cond(active, "white", t.SLATE),
        background=rx.cond(active, t.PURPLE, "transparent"),
        transition="all 140ms ease",
        style={"_hover": {"color": rx.cond(active, "white", t.INK)}},
    )


def mode_toggle() -> rx.Component:
    return rx.box(
        rx.hstack(
            _segment("Academic", "graduation-cap", LabState.mode_is_academic,
                     lambda: LabState.set_mode("academic")),
            _segment("Literary", "feather", ~LabState.mode_is_academic,
                     lambda: LabState.set_mode("literary")),
            spacing="1",
        ),
        style=dict(
            background=t.MUTED_BG,
            border=f"1px solid {t.BORDER}",
            border_radius="12px",
            padding="4px",
        ),
    )
