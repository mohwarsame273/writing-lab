"""The writing surface.

v1 is a clean, distraction-free text area, on purpose: do not make a custom
editor the first technical challenge. The wrapped React editor is a v2 upgrade.

TODO (completing agent): replace the text area with a wrapped CodeMirror 6
component (rx.NoSSRComponent) to get inline underlines from the diagnostic
ranges. Keep this module's public function `editor()` and the on_change ->
LabState.update_answer wiring identical so the swap is contained.

Design-library mapping: this pairs with Badge (word count, live verdict) and
Alert (live findings)."""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t
from writing_lab.components.common import pill
from writing_lab.components.diagnostics import diagnostics_list
from writing_lab.state.lab_state import LabState


def _live_verdict_pill() -> rx.Component:
    colour = rx.match(
        LabState.live_verdict,
        ("lean", t.GREEN),
        ("fit-and-trim", t.TEAL),
        ("needs-toning", t.AMBER),
        ("flabby", t.ORANGE),
        ("heart-attack", t.RED),
        t.SLATE,
    )
    return rx.cond(
        LabState.live_verdict != "",
        rx.box(
            rx.text(LabState.live_verdict, font_size="12px", font_weight="700", color=colour,
                    text_transform="capitalize"),
            style={**t.PILL, "background": rx.match(
                LabState.live_verdict,
                ("lean", f"{t.GREEN}1A"), ("fit-and-trim", f"{t.TEAL}1A"),
                ("needs-toning", f"{t.AMBER}1A"), ("flabby", f"{t.ORANGE}1A"),
                ("heart-attack", f"{t.RED}1A"), f"{t.SLATE}1A")},
        ),
        rx.fragment(),
    )


from writing_lab.components.codemirror_editor import cm_editor

def editor() -> rx.Component:
    return rx.vstack(
        cm_editor(
            value=LabState.answer,
            on_change=LabState.update_answer.debounce(600),
            diagnostics=LabState.live_diagnostics,
            placeholder="Write your answer here...",
            style=dict(
                min_height="180px",
                font_size="15px",
                line_height="1.7",
                font_family=t.FONT,
                background=t.SURFACE,
                border=f"1px solid {t.BORDER}",
                border_radius="14px",
                padding="16px",
                color=t.INK,
            ),
            min_width="0",
        ),
        rx.hstack(
            pill(LabState.word_count.to_string() + " words", t.SLATE, icon="type"),
            _live_verdict_pill(),
            rx.spacer(),
            rx.text("Live preview updates as you type", font_size="11px", color=t.SLATE),
            width="100%",
            align_items="center",
        ),
        rx.cond(
            ~LabState.casual_mode,
            rx.cond(
                LabState.live_diagnostics.length() > 0,
                rx.box(
                    rx.text("Live findings", font_size="12px", font_weight="700", color=t.INK,
                            margin_bottom="8px"),
                    diagnostics_list(LabState.live_diagnostics),
                    style=t.SOFT_CARD,
                    width="100%",
                ),
                rx.fragment(),
            ),
            rx.fragment()
        ),
        spacing="3",
        width="100%",
        align_items="stretch",
        min_width="0",
    )
