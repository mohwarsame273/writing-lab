"""Dashboard / home. Momentum at a glance (Full mode) and one clear way back
into practice. In Casual mode it stays deliberately quiet."""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t
from writing_lab.components.common import stat_card, pill
from writing_lab.components.mastery import mastery_panel
from writing_lab.layout import shell
from writing_lab.state.lab_state import LabState


def _hero() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                pill("Welcome back", "white", icon="sparkles"),
                rx.heading("Get back to writing.", size="8", color="white", weight="bold"),
                rx.text(
                    "Short, practical drills and free-writing sessions. Switch between "
                    "academic and literary craft, and focus a single topic when you want "
                    "to drill it into memory.",
                    color="rgba(255,255,255,0.85)", font_size="15px", max_width="460px",
                ),
                rx.hstack(
                    rx.link(
                        rx.button("Start practising", rx.icon("arrow-right", size=16),
                                  on_click=LabState.load_next, size="3",
                                  style={"background": "white", "color": t.PURPLE, "font_weight": "700"}),
                        href="/practice",
                    ),
                    rx.link(
                        rx.button("Free write", rx.icon("pen-tool", size=16), size="3",
                                  variant="outline",
                                  style={"color": "white", "border_color": "rgba(255,255,255,0.5)"}),
                        href="/free-write",
                    ),
                    spacing="3", margin_top="8px",
                ),
                spacing="3", align_items="start",
            ),
            rx.spacer(),
            rx.box(
                rx.icon("feather", size=120, color="rgba(255,255,255,0.18)"),
                display=rx.breakpoints(initial="none", md="block"),
            ),
            width="100%", align_items="center",
        ),
        style=dict(
            background=f"linear-gradient(135deg, {t.PURPLE} 0%, #8A4CB0 60%, {t.BLUE} 130%)",
            border_radius="22px",
            padding="34px",
            box_shadow="0 12px 40px rgba(110,54,138,0.28)",
        ),
        width="100%",
    )


def _stats_row() -> rx.Component:
    return rx.cond(
        ~LabState.casual_mode,
        rx.grid(
            stat_card("zap", LabState.xp, "Total XP", t.AMBER),
            stat_card("flame", LabState.streak, "Day streak", t.ORANGE),
            stat_card("circle_check", LabState.completed_ids.length(), "Exercises done", t.TEAL),
            stat_card("target", LabState.progress_pct.to_string() + "%", "Bank progress", t.PURPLE),
            columns=rx.breakpoints(initial="2", md="4"),
            spacing="4", width="100%",
        ),
        rx.fragment(),
    )


def _step(n: str, title: str, body: str) -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.text(n, font_size="13px", font_weight="800", color="white"),
            style=dict(background=t.PURPLE, border_radius="999px", width="26px", height="26px",
                       display="flex", align_items="center", justify_content="center", flex_shrink="0"),
        ),
        rx.vstack(
            rx.text(title, font_size="13px", font_weight="700", color=t.INK),
            rx.text(body, font_size="12px", color=t.SLATE, line_height="1.5"),
            spacing="0", align_items="start",
        ),
        spacing="3", align_items="start", width="100%",
    )


def _how_it_works() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("list-checks", size=18, color=t.PURPLE),
            rx.text("How it works", font_size="15px", font_weight="700", color=t.INK),
            spacing="2", align_items="center", margin_bottom="12px",
        ),
        rx.vstack(
            _step("1", "Pick a mode", "Academic sharpens clarity and argument. Literary sharpens voice and image."),
            _step("2", "Focus a topic (optional)", "Choose one area, say transitions or reporting results, and drill it until it sticks."),
            _step("3", "Practise in short drills", "Rewrite, complete a sentence, choose the best option, or compose under a constraint. Reveal hints if stuck."),
            _step("4", "Get a real check", "Deterministic diagnostics plus retrieved principles, with an optional AI read on meaning and force when a key is set."),
            spacing="3", width="100%",
        ),
        style=t.CARD, width="100%",
    )


def _casual_hint() -> rx.Component:
    return rx.cond(
        LabState.casual_mode,
        rx.box(
            rx.hstack(
                rx.icon("info", size=15, color=t.SLATE),
                rx.text("You are in Casual mode: no scores or streaks, just practice. "
                        "Flip the switch in the top bar to Full for XP and progress tracking.",
                        font_size="12px", color=t.SLATE, line_height="1.5"),
                spacing="2", align_items="start",
            ),
            style=t.SOFT_CARD, width="100%",
        ),
        rx.fragment(),
    )


def dashboard() -> rx.Component:
    return shell(
        _hero(),
        _stats_row(),
        rx.cond(
            ~LabState.casual_mode,
            rx.grid(
                mastery_panel(),
                _how_it_works(),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="5", width="100%",
            ),
            rx.vstack(
                _how_it_works(),
                _casual_hint(),
                spacing="5", width="100%", align_items="stretch",
            ),
        ),
    )