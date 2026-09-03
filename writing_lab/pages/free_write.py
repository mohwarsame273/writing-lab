"""Free writing. The emotional core: sit down, write, and get an honest mirror
of your habits without a score hanging over you."""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t
from writing_lab.components.common import pill, section_heading
from writing_lab.components.diagnostics import diagnostics_list
from writing_lab.layout import shell
from writing_lab.state.lab_state import LabState


def _intro() -> rx.Component:
    return rx.box(
        rx.vstack(
            pill("No score, just a mirror", t.TEAL, icon="eye"),
            rx.heading("Free writing", size="7", color=t.INK, weight="bold"),
            rx.text(
                "Write for a few minutes without stopping to edit. When you are ready, "
                "get a profile of your habits: zombie nouns, preposition stacks, repeated "
                "openings and sentence rhythm.",
                font_size="14px", color=t.SLATE, max_width="620px", line_height="1.6",
            ),
            spacing="3", align_items="start",
        ),
        width="100%",
    )


def _writing_surface() -> rx.Component:
    return rx.box(
        rx.text_area(
            value=LabState.fw_text,
            on_change=LabState.update_free_write,
            placeholder="Start writing. Describe the room you are in, or pick up a thread you have been avoiding...",
            style=dict(
                min_height="320px", font_size="16px", line_height="1.8", font_family=t.FONT,
                background=t.SURFACE, border=f"1px solid {t.BORDER}", border_radius="16px",
                padding="22px", color=t.INK,
            ),
            width="100%", resize="vertical",
        ),
        rx.hstack(
            pill(LabState.fw_word_count.to_string() + " words", t.SLATE, icon="type"),
            rx.spacer(),
            rx.button(
                "Analyse my writing", rx.icon("scan-line", size=16),
                on_click=LabState.analyse_free_write, color_scheme="purple", size="3",
                disabled=LabState.fw_word_count < 20,
            ),
            width="100%", align_items="center", margin_top="12px",
        ),
        rx.cond(
            LabState.fw_word_count < 20,
            rx.text("Write at least 20 words for a meaningful profile.",
                    font_size="12px", color=t.SLATE, margin_top="6px"),
            rx.fragment(),
        ),
        width="100%",
    )


def _profile_metric(label: str, key: str, colour: str) -> rx.Component:
    pct = (LabState.fw_diet[key].to(float) * 100).to(int)
    return rx.vstack(
        rx.hstack(
            rx.text(label, font_size="12px", color=t.SLATE),
            rx.spacer(),
            rx.text(pct.to_string() + "%", font_size="12px", font_weight="700", color=colour),
            width="100%",
        ),
        rx.progress(value=pct, color_scheme="gray", height="7px", width="100%"),
        spacing="1", width="100%",
    )


def _opening(item: rx.Var) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text(item["word"], font_size="13px", font_weight="600", color=t.INK,
                    text_transform="capitalize"),
            rx.spacer(),
            pill(item["count"].to_string() + "x", t.ORANGE),
            width="100%", align_items="center",
        ),
        style=t.SOFT_CARD, width="100%",
    )


def _ai_note() -> rx.Component:
    return rx.cond(
        LabState.fw_ai_note != "",
        rx.box(
            section_heading("Coaching note", "Voice, rhythm, and your strongest line."),
            rx.text(LabState.fw_ai_note, font_size="14px", font_style="italic",
                    color=t.INK, line_height="1.6"),
            style={**t.SOFT_CARD, "border_left": f"3px solid {t.TEAL}"},
            width="100%",
        ),
        rx.fragment(),
    )


def _profile() -> rx.Component:
    verdict_colour = rx.match(
        LabState.fw_diet["verdict"],
        ("lean", t.GREEN), ("fit-and-trim", t.TEAL), ("needs-toning", t.AMBER),
        ("flabby", t.ORANGE), ("heart-attack", t.RED), t.SLATE,
    )
    return rx.vstack(
        _ai_note(),
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.text("Your Writer's Diet", font_size="12px", color=t.SLATE),
                    rx.text(LabState.fw_diet["verdict"], font_size="26px", font_weight="800",
                            color=verdict_colour, text_transform="capitalize", line_height="1"),
                    spacing="1", align_items="start",
                ),
                rx.spacer(),
                rx.vstack(
                    pill(LabState.fw_diet["word_count"].to_string() + " words", t.SLATE),
                    pill("avg " + LabState.fw_diet["mean_sentence_len"].to_string() + " w/sentence", t.BLUE),
                    spacing="2", align_items="end",
                ),
                width="100%", align_items="center",
            ),
            rx.grid(
                _profile_metric("Zombie nouns", "nominalisations", t.RED),
                _profile_metric("Prepositions", "prepositions", t.ORANGE),
                _profile_metric("Ad-words", "ad_words", t.AMBER),
                _profile_metric("Waste words", "waste_words", t.SLATE),
                columns="2", spacing="5", width="100%", margin_top="16px",
            ),
            style=t.CARD, width="100%",
        ),
        rx.cond(
            LabState.fw_openings.length() > 0,
            rx.box(
                section_heading("Repeated sentence openings",
                                "Words you start sentences with more than once."),
                rx.grid(rx.foreach(LabState.fw_openings, _opening),
                        columns=rx.breakpoints(initial="1", md="2"), spacing="3", width="100%"),
                style=t.CARD, width="100%",
            ),
            rx.fragment(),
        ),
        rx.box(
            section_heading("Line-level findings"),
            diagnostics_list(LabState.fw_diagnostics, "A clean pass. Nothing flagged."),
            style=t.CARD, width="100%",
        ),
        rx.hstack(
            rx.button("Write more", on_click=LabState.reset_free_write, variant="soft",
                      color_scheme="gray", size="3"),
            rx.spacer(),
            rx.cond(
                ~LabState.casual_mode,
                pill("+20 XP for showing up", t.AMBER, icon="zap"),
                rx.fragment(),
            ),
            width="100%", align_items="center",
        ),
        spacing="4", width="100%", align_items="stretch",
    )


def free_write() -> rx.Component:
    return shell(
        _intro(),
        rx.cond(LabState.fw_analysed, _profile(), _writing_surface()),
        max_width="920px",
    )