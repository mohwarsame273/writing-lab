"""The core practice screen: a two-pane, DataCamp-style layout.

Left rail frames the current drill, lets you focus a single topic to drill and
memorise, and shows progress (in Full mode). Right pane is the exercise, editor,
hints and feedback.
"""
from __future__ import annotations

import reflex as rx

from writing_lab import theme as t
from writing_lab.components.common import pill, section_heading
from writing_lab.components.editor import editor
from writing_lab.components.feedback_panel import feedback_panel
from writing_lab.components.hint_panel import hint_panel
from writing_lab.layout import shell
from writing_lab.state.lab_state import LabState


# --------------------------------------------------------------- topic picker
def _topic_chip(label, active, on_click) -> rx.Component:
    """A single clickable topic chip. `label` and `active` may be Vars."""
    return rx.box(
        rx.text(label, font_size="12px", font_weight="600",
                text_transform="capitalize", white_space="nowrap"),
        on_click=on_click,
        cursor="pointer",
        padding="6px 12px",
        border_radius="999px",
        color=rx.cond(active, "white", t.INK_SOFT),
        background=rx.cond(active, t.PURPLE, t.MUTED_BG),
        border=rx.cond(active, f"1px solid {t.PURPLE}", f"1px solid {t.BORDER}"),
        transition="all 120ms ease",
        style={"_hover": {"border_color": t.PURPLE}},
    )


def _skill_chip(item: rx.Var) -> rx.Component:
    label = item.replace("-", " ")
    return _topic_chip(
        label,
        LabState.selected_skill == item,
        lambda: LabState.set_focus_skill(item),
    )


def _topic_picker() -> rx.Component:
    return rx.box(
        section_heading("Focus a topic", "Drill one area until it sticks."),
        rx.scroll_area(
            rx.flex(
                _topic_chip("All topics", LabState.selected_skill == "", LabState.clear_focus),
                rx.foreach(LabState.available_skills, _skill_chip),
                wrap="wrap", gap="8px",
            ),
            type="hover", scrollbars="vertical", max_height="150px",
        ),
        width="100%",
    )


# --------------------------------------------------------------- left rail
def _kind_title() -> rx.Var:
    return rx.match(
        LabState.ex_kind,
        ("rewrite", "Targeted rewrite"),
        ("sentence_completion", "Sentence completion"),
        ("diagnostic_selection", "Diagnostic choice"),
        ("constrained_composition", "Constrained composition"),
        ("transitions", "Transition drill"),
        ("paragraph_revision", "Paragraph revision"),
        ("free_write", "Free writing"),
        "Exercise",
    )


def _bank_progress() -> rx.Component:
    # meaningful only in Full mode, where completions accrue
    return rx.cond(
        ~LabState.casual_mode,
        rx.vstack(
            rx.hstack(
                rx.text("Bank progress", font_size="12px", color=t.SLATE),
                rx.spacer(),
                rx.text(LabState.progress_pct.to_string() + "%", font_size="12px",
                        font_weight="700", color=t.PURPLE),
                width="100%",
            ),
            rx.progress(value=LabState.progress_pct, color_scheme="purple", height="8px", width="100%"),
            spacing="2", width="100%",
        ),
        rx.fragment(),
    )


def _generate_button() -> rx.Component:
    return rx.button(
        rx.cond(LabState.is_generating_drill, rx.spinner(size="2"), rx.icon("sparkles", size=14)),
        rx.cond(LabState.is_generating_drill, "Generating...", "Generate a fresh drill"),
        on_click=LabState.generate_fresh_drill,
        disabled=LabState.is_generating_drill,
        variant="soft", color_scheme="purple", size="2", width="100%",
    )


def _left_rail() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                pill(LabState.ex_skill, t.PURPLE, icon="tag"),
                rx.cond(
                    LabState.mode_is_academic,
                    pill("Academic", t.BLUE, icon="graduation-cap"),
                    pill("Literary", t.ORANGE, icon="feather"),
                ),
                spacing="2", wrap="wrap",
            ),
            rx.text(_kind_title(), font_size="18px", font_weight="800", color=t.INK, margin_top="6px"),
            rx.divider(),
            _topic_picker(),
            rx.divider(),
            section_heading("Objective", LabState.ex_target),
            _bank_progress(),
            _generate_button(),
            spacing="4", align_items="stretch",
        ),
        style=t.CARD,
        width="100%",
        height="fit-content",
        position=rx.breakpoints(initial="static", md="sticky"),
        top="90px",
    )


# --------------------------------------------------------------- right pane
def _prompt_card() -> rx.Component:
    return rx.box(
        rx.text(LabState.ex_prompt, font_size="15px", font_weight="600", color=t.INK, line_height="1.6", overflow_wrap="anywhere"),
        rx.cond(
            LabState.ex_seed != "",
            rx.box(
                rx.text(LabState.ex_seed, font_size="15px", color=t.INK_SOFT, font_style="italic",
                        line_height="1.6", overflow_wrap="anywhere"),
                style=dict(background=t.PURPLE_SOFT, border_left=f"3px solid {t.PURPLE}",
                           border_radius="10px", padding="12px 16px", margin_top="12px"),
                min_width="0",
            ),
            rx.fragment(),
        ),
        style=t.CARD, width="100%", min_width="0",
    )


def _option_row(item: rx.Var, index: rx.Var) -> rx.Component:
    selected = LabState.selected_option == index
    return rx.box(
        rx.hstack(
            rx.box(
                rx.cond(selected, rx.icon("check", size=14, color="white"), rx.fragment()),
                style=dict(
                    width="22px", height="22px", border_radius="7px", flex_shrink="0",
                    display="flex", align_items="center", justify_content="center",
                    border=rx.cond(selected, f"1px solid {t.PURPLE}", f"1px solid {t.BORDER}"),
                    background=rx.cond(selected, t.PURPLE, t.SURFACE),
                ),
            ),
            rx.text(item, font_size="14px", color=t.INK_SOFT, line_height="1.5"),
            spacing="3", align_items="center",
        ),
        on_click=lambda: LabState.select_option(index),
        cursor="pointer",
        padding="14px 16px",
        border_radius="12px",
        background=rx.cond(selected, t.PURPLE_SOFT, t.SURFACE),
        border=rx.cond(selected, f"1px solid {t.PURPLE}", f"1px solid {t.BORDER}"),
        transition="all 120ms ease",
        width="100%",
    )


def _work_area() -> rx.Component:
    return rx.cond(
        LabState.is_selection,
        rx.vstack(rx.foreach(LabState.ex_options, _option_row), spacing="3", width="100%"),
        editor(),
    )


def _submit_bar() -> rx.Component:
    return rx.hstack(
        rx.cond(
            LabState.is_grading,
            rx.button(rx.spinner(size="2"), "Grading...", disabled=True, size="3",
                      color_scheme="purple", width="100%"),
            rx.button(
                "Submit for grading", rx.icon("send", size=16),
                on_click=LabState.submit, size="3", color_scheme="purple", width="100%",
                disabled=rx.cond(
                    LabState.is_selection,
                    LabState.selected_option == -1,
                    LabState.word_count < 1,
                ),
            ),
        ),
        width="100%",
    )


def _selection_hint() -> rx.Component:
    return rx.cond(LabState.ex_hints.length() > 0, hint_panel(), rx.fragment())


def _right_pane() -> rx.Component:
    return rx.vstack(
        _prompt_card(),
        rx.cond(
            LabState.graded,
            feedback_panel(),
            rx.vstack(
                _work_area(),
                rx.cond(~LabState.is_selection, hint_panel(), _selection_hint()),
                _submit_bar(),
                spacing="4", width="100%", align_items="stretch", min_width="0",
            ),
        ),
        spacing="5", width="100%", align_items="stretch", min_width="0",
    )


def practice() -> rx.Component:
    return shell(
        rx.grid(
            _left_rail(),
            _right_pane(),
            columns=rx.breakpoints(initial="1", md="340px 1fr"),
            spacing="6",
            width="100%",
            align_items="start",
        ),
        max_width="1160px",
    )