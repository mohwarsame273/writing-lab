"""Mastery bars. XP measures momentum; mastery measures learning. Kept visually
distinct from XP so the learner reads them differently.

Design-library mapping: Progress, Card."""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t
from writing_lab.state.lab_state import LabState


def _mastery_row(item: rx.Var) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text(item["skill"].to(str).replace("-", " "), font_size="13px", font_weight="600", color=t.INK_SOFT, text_transform="capitalize"),
            rx.spacer(),
            rx.cond(
                item["attempts"].to(int) > 0,
                rx.text(item["attempts"].to(str) + " observations • Last seen " + item["date"].to(str), font_size="11px", color=t.SLATE),
                rx.fragment(),
            ),
            width="100%",
        ),
        rx.hstack(
            rx.box(
                rx.icon("circle_check", size=14, color=rx.cond(item["state"].to(str) != "Not yet sampled", t.TEAL, t.MUTED_BG)),
                rx.text("Practised", font_size="11px", color=rx.cond(item["state"].to(str) != "Not yet sampled", t.TEAL, t.SLATE)),
                display="flex", align_items="center", gap="4px"
            ),
            rx.box(
                rx.icon("circle_check", size=14, color=rx.cond((item["state"].to(str) == "Demonstrated in independent practice") | (item["state"].to(str) == "Demonstrated again after a delay"), t.TEAL, t.MUTED_BG)),
                rx.text("Independent", font_size="11px", color=rx.cond((item["state"].to(str) == "Demonstrated in independent practice") | (item["state"].to(str) == "Demonstrated again after a delay"), t.TEAL, t.SLATE)),
                display="flex", align_items="center", gap="4px"
            ),
            rx.box(
                rx.icon("circle_check", size=14, color=rx.cond(item["state"].to(str) == "Demonstrated again after a delay", t.TEAL, t.MUTED_BG)),
                rx.text("Delayed", font_size="11px", color=rx.cond(item["state"].to(str) == "Demonstrated again after a delay", t.TEAL, t.SLATE)),
                display="flex", align_items="center", gap="4px"
            ),
            rx.box(
                rx.icon("lock", size=14, color=t.SLATE),
                rx.text("Verified", font_size="11px", color=t.SLATE),
                display="flex", align_items="center", gap="4px", opacity="0.6"
            ),
            width="100%", spacing="3"
        ),
        spacing="2", width="100%", margin_bottom="12px",
    )

def mastery_panel() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("brain", size=18, color=t.PURPLE),
            rx.text("Evidence of learning", font_size="15px", font_weight="700", color=t.INK),
            spacing="2", align_items="center", margin_bottom="14px",
        ),
        rx.vstack(rx.foreach(LabState.mastery_display_list.to(list[dict]), _mastery_row), spacing="4", width="100%"),
        style=t.CARD, width="100%",
    )
