"""Progressive hints. Hints are part of the exercise, not a punishment; each
reveal lowers the XP cap but never blocks completion (see domain.scoring).

Design-library mapping: Accordion / Disclosure."""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t
from writing_lab.components.common import pill
from writing_lab.state.lab_state import LabState

_HINT_LABELS = ["Concept", "Location", "Transformation", "Model answer"]


def _revealed_hint(item: rx.Var, index: rx.Var) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("lightbulb", size=13, color=t.AMBER),
                style=dict(background=f"{t.AMBER}1A", border_radius="8px", padding="6px", display="flex"),
            ),
            rx.text(item, font_size="13px", color=t.INK_SOFT, line_height="1.5"),
            spacing="3",
            align_items="start",
        ),
        style=t.SOFT_CARD,
        width="100%",
    )


def hint_panel() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.text("Hints", font_size="13px", font_weight="700", color=t.INK),
            rx.spacer(),
            rx.cond(
                ~LabState.casual_mode,
                rx.cond(
                ~LabState.casual_mode,
                pill(LabState.xp_cap_label, t.AMBER, icon="gauge"),
                rx.fragment(),
            ),
                rx.fragment(),
            ),
            width="100%",
            align_items="center",
        ),
        rx.foreach(LabState.revealed_hints, _revealed_hint),
        rx.cond(
            LabState.can_reveal_hint,
            rx.button(
                rx.icon("lightbulb", size=15),
                "Reveal a hint",
                on_click=LabState.reveal_hint,
                variant="soft",
                color_scheme="amber",
                size="2",
                width="100%",
            ),
            rx.text("All hints revealed.", font_size="12px", color=t.SLATE),
        ),
        spacing="3",
        width="100%",
        align_items="stretch",
    )
