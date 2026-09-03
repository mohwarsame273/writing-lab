"""Mastery bars. XP measures momentum; mastery measures learning. Kept visually
distinct from XP so the learner reads them differently.

Design-library mapping: Progress, Card."""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t
from writing_lab.state.lab_state import LabState


def _mastery_row(item: rx.Var) -> rx.Component:
    m = item["mastery"].to(float)
    pct = (m * 100).to(int)
    colour = rx.cond(
        m >= 0.66, t.TEAL,
        rx.cond(m >= 0.4, t.AMBER, t.ORANGE),
    )
    return rx.vstack(
        rx.hstack(
            rx.text(item["skill"], font_size="13px", font_weight="600", color=t.INK_SOFT,
                    text_transform="capitalize"),
            rx.spacer(),
            rx.text(pct.to_string() + "%", font_size="13px", font_weight="700", color=colour),
            width="100%",
        ),
        rx.box(
            rx.box(width=pct.to_string() + "%", height="100%", background=colour,
                   border_radius="999px", transition="width 400ms ease"),
            width="100%", height="8px", background=t.MUTED_BG, border_radius="999px",
        ),
        spacing="1", width="100%",
    )


def mastery_panel() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("brain", size=18, color=t.PURPLE),
            rx.text("Skill mastery", font_size="15px", font_weight="700", color=t.INK),
            spacing="2", align_items="center", margin_bottom="14px",
        ),
        rx.vstack(rx.foreach(LabState.mastery, _mastery_row), spacing="4", width="100%"),
        style=t.CARD, width="100%",
    )
