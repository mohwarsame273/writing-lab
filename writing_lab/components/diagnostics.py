"""Diagnostics list. Renders deterministic findings as coloured rows. Shared by
the live editor preview and the post-submission feedback.

TODO (completing agent): the real prize is inline underlining inside the
editor. When you wrap CodeMirror 6, feed it the {start,end,severity} ranges
from domain.diagnostics.analyse() and render decorations instead of this list.
"""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t
from writing_lab.components.common import severity_dot


def _severity_colour(sev: rx.Var) -> rx.Var:
    return rx.match(
        sev,
        ("high", t.RED),
        ("medium", t.AMBER),
        t.SLATE,
    )


def _row(item: rx.Var) -> rx.Component:
    colour = _severity_colour(item["severity"])
    return rx.box(
        rx.hstack(
            severity_dot(colour),
            rx.vstack(
                rx.hstack(
                    rx.text(item["type"], font_size="11px", font_weight="700",
                            color=colour, text_transform="capitalize"),
                    rx.text(item["text"], font_size="11px", color=t.SLATE,
                            font_style="italic", max_width="180px",
                            overflow="hidden", text_overflow="ellipsis", white_space="nowrap"),
                    spacing="2",
                    align_items="center",
                ),
                rx.text(item["message"], font_size="12px", color=t.INK_SOFT, line_height="1.4"),
                spacing="1",
                align_items="start",
            ),
            spacing="3",
            align_items="start",
        ),
        padding="10px 12px",
        border_radius="10px",
        background=t.SURFACE,
        border=f"1px solid {t.BORDER}",
        width="100%",
    )


def diagnostics_list(items: rx.Var, empty_message: str = "No findings yet.") -> rx.Component:
    return rx.cond(
        items.length() > 0,
        rx.vstack(rx.foreach(items, _row), spacing="2", width="100%"),
        rx.text(empty_message, font_size="12px", color=t.SLATE),
    )
