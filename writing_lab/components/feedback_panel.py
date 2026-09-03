"""Post-submission feedback. Design-library mapping: Alert/Callout (verdict),
Progress (rubric bars, diet meters), Card."""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t
from writing_lab.components.common import pill, section_heading
from writing_lab.components.diagnostics import diagnostics_list
from writing_lab.state.lab_state import LabState


def _verdict_banner() -> rx.Component:
    return rx.cond(
        LabState.fb_passed,
        rx.callout(
            "Strong work. XP awarded.",
            icon="circle_check",
            color_scheme="teal",
            variant="soft",
        ),
        rx.callout(
            "Not there yet. Revise using the notes below and resubmit.",
            icon="info",
            color_scheme="amber",
            variant="soft",
        ),
    )


def _rubric_bar(item: rx.Var) -> rx.Component:
    score = item["score"].to(int)
    out_of = item["out_of"].to(int)
    pct = (score * 100 / out_of).to(int)
    return rx.vstack(
        rx.hstack(
            rx.text(item["label"], font_size="12px", font_weight="600", color=t.INK_SOFT),
            rx.spacer(),
            rx.text(score.to_string() + " / " + out_of.to_string(),
                    font_size="12px", color=t.SLATE),
            width="100%",
        ),
        rx.progress(value=pct, color_scheme="purple", height="8px", width="100%"),
        spacing="1",
        width="100%",
    )


def _strength(item: rx.Var) -> rx.Component:
    return rx.hstack(
        rx.icon("check", size=14, color=t.TEAL),
        rx.text(item, font_size="13px", color=t.INK_SOFT, line_height="1.5"),
        spacing="2", align_items="start", width="100%",
    )


def _improvement(item: rx.Var) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("arrow-up-right", size=14, color=t.ORANGE),
            rx.vstack(
                rx.text(item["issue"], font_size="13px", font_weight="600", color=t.INK, line_height="1.4"),
                rx.text(item["suggestion"], font_size="12px", color=t.SLATE, line_height="1.4"),
                spacing="0", align_items="start",
            ),
            spacing="2", align_items="start",
        ),
        style=t.SOFT_CARD, width="100%",
    )


def _diet_meter(label: str, key: str, colour: str) -> rx.Component:
    # diet ratios are shares in [0,1]; scale x100 for a readable meter
    raw = LabState.fb_diet[key].to(float)
    pct = (raw * 100).to(int)
    return rx.vstack(
        rx.hstack(
            rx.text(label, font_size="11px", color=t.SLATE),
            rx.spacer(),
            rx.text(pct.to_string() + "%", font_size="11px", font_weight="700", color=colour),
            width="100%",
        ),
        rx.progress(value=pct, color_scheme="gray", height="6px", width="100%"),
        spacing="1", width="100%",
    )


def _diet_card() -> rx.Component:
    verdict_colour = rx.match(
        LabState.fb_diet["verdict"],
        ("lean", t.GREEN), ("fit-and-trim", t.TEAL), ("needs-toning", t.AMBER),
        ("flabby", t.ORANGE), ("heart-attack", t.RED), t.SLATE,
    )
    return rx.cond(
        LabState.fb_diet,
        rx.box(
            rx.hstack(
                section_heading("Writer's Diet profile"),
                rx.spacer(),
                rx.box(
                    rx.text(LabState.fb_diet["verdict"], font_size="12px", font_weight="700",
                            color=verdict_colour, text_transform="capitalize"),
                    style={**t.PILL, "background": f"{t.MUTED_BG}"},
                ),
                width="100%", align_items="center",
            ),
            rx.grid(
                _diet_meter("Zombie nouns", "nominalisations", t.RED),
                _diet_meter("Prepositions", "prepositions", t.ORANGE),
                _diet_meter("Ad-words", "ad_words", t.AMBER),
                _diet_meter("Waste words", "waste_words", t.SLATE),
                columns="2",
                spacing="4",
                width="100%",
                margin_top="10px",
            ),
            style=t.CARD, width="100%",
        ),
        rx.fragment(),
    )


def feedback_panel() -> rx.Component:
    return rx.cond(
        ~LabState.casual_mode,
        rx.vstack(
            _verdict_banner(),
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.text("Score", font_size="12px", color=t.SLATE),
                        rx.hstack(
                            rx.text(LabState.fb_total.to_string(), font_size="30px", font_weight="800", color=t.INK, line_height="1"),
                            rx.text("/ " + LabState.fb_out_of.to_string(), font_size="14px", color=t.SLATE),
                            spacing="1", align_items="end",
                        ),
                        spacing="1", align_items="start",
                    ),
                    rx.spacer(),
                    pill("+" + LabState.fb_xp.to_string() + " XP", t.AMBER, icon="zap"),
                    rx.cond(LabState.fb_used_llm,
                            pill("AI-graded", t.BLUE, icon="sparkles"),
                            pill("rule-graded", t.SLATE, icon="ruler")),
                    width="100%", align_items="center",
                ),
                rx.cond(
                    LabState.fb_rubric.length() > 0,
                    rx.vstack(rx.foreach(LabState.fb_rubric, _rubric_bar), spacing="3",
                              width="100%", margin_top="14px"),
                    rx.fragment(),
                ),
                style=t.CARD, width="100%",
            ),
            rx.cond(
                LabState.fb_model_revision != "",
                rx.box(
                    section_heading("A stronger version"),
                    rx.text(LabState.fb_model_revision, font_size="14px", font_style="italic", color=t.INK, margin_bottom="8px", line_height="1.5"),
                    rx.cond(
                        LabState.fb_coaching_note != "",
                        rx.text(LabState.fb_coaching_note, font_size="13px", color=t.TEAL, font_weight="600"),
                        rx.fragment()
                    ),
                    style=t.SOFT_CARD, width="100%",
                ),
                rx.fragment()
            ),
            rx.cond(
                LabState.fb_strengths.length() > 0,
                rx.box(
                    section_heading("What worked"),
                    rx.vstack(rx.foreach(LabState.fb_strengths, _strength), spacing="2", width="100%"),
                    style=t.CARD, width="100%",
                ),
                rx.fragment(),
            ),
            rx.cond(
                LabState.fb_improvements.length() > 0,
                rx.vstack(
                    section_heading("Where to sharpen"),
                    rx.foreach(LabState.fb_improvements, _improvement),
                    spacing="2", width="100%",
                ),
                rx.fragment(),
            ),
            _diet_card(),
            rx.cond(
                LabState.fb_diagnostics.length() > 0,
                rx.box(
                    section_heading("Line-level findings"),
                    diagnostics_list(LabState.fb_diagnostics),
                    style=t.CARD, width="100%",
                ),
                rx.fragment(),
            ),
            rx.hstack(
                rx.button("Try again", on_click=LabState.try_again, variant="soft",
                          color_scheme="gray", size="3"),
                rx.button("Next exercise", rx.icon("arrow-right", size=16),
                          on_click=LabState.load_next, color_scheme="purple", size="3"),
                spacing="3", width="100%", justify="end",
            ),
            spacing="4", width="100%", align_items="stretch",
        ),
        rx.vstack(
            _verdict_banner(),
            rx.cond(
                LabState.fb_model_revision != "",
                rx.box(
                    section_heading("A stronger version"),
                    rx.text(LabState.fb_model_revision, font_size="14px", font_style="italic", color=t.INK, margin_bottom="8px", line_height="1.5"),
                    rx.cond(
                        LabState.fb_coaching_note != "",
                        rx.text(LabState.fb_coaching_note, font_size="13px", color=t.TEAL, font_weight="600"),
                        rx.fragment()
                    ),
                    style=t.SOFT_CARD, width="100%",
                ),
                rx.fragment()
            ),
            rx.cond(
                LabState.fb_strengths.length() > 0,
                rx.box(
                    section_heading("What worked"),
                    rx.vstack(rx.foreach(LabState.fb_strengths, _strength), spacing="2", width="100%"),
                    style=t.CARD, width="100%",
                ),
                rx.fragment(),
            ),
            rx.cond(
                LabState.fb_improvements.length() > 0,
                rx.vstack(
                    section_heading("Where to sharpen"),
                    rx.foreach(LabState.fb_improvements, _improvement),
                    spacing="2", width="100%",
                ),
                rx.fragment(),
            ),
            rx.hstack(
                rx.button("Try again", on_click=LabState.try_again, variant="soft",
                          color_scheme="gray", size="3"),
                rx.button("Next exercise", rx.icon("arrow-right", size=16),
                          on_click=LabState.load_next, color_scheme="purple", size="3"),
                spacing="3", width="100%", justify="end",
            ),
            spacing="4", width="100%", align_items="stretch",
        )
    )
