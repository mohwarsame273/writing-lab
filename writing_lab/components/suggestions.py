import reflex as rx
from writing_lab import theme as t
from writing_lab.components.common import section_heading

_MOVE_CARDS = [
    {"title": "Context", "prompt": "Establish the background the reader needs to understand this."},
    {"title": "Definition / Claim", "prompt": "Define exactly what you are asserting here."},
    {"title": "Contrast", "prompt": "Identify the dimension along which these options differ."},
    {"title": "Cause / Mechanism", "prompt": "Explain the process by which this might happen."},
    {"title": "Evidence / Warrant", "prompt": "Provide the evidence that supports this, and explain why."},
    {"title": "Problem / Consequence", "prompt": "State what is wrong, by what standard, and who is affected."},
    {"title": "Tension / Counterargument", "prompt": "Present the strongest relevant alternative fairly."},
    {"title": "Condition / Limitation", "prompt": "Clarify the conditions under which this claim holds or fails."},
    {"title": "Gap", "prompt": "Identify what remains uncertain."},
    {"title": "Implication", "prompt": "Explain what follows from this, and what should be done."},
]

def _move_card(card: dict) -> rx.Component:
    return rx.box(
        rx.text(card["title"], font_size="12px", font_weight="700", color=t.PURPLE, margin_bottom="2px"),
        rx.text(card["prompt"], font_size="13px", color=t.INK_SOFT),
        style=t.SOFT_CARD,
        padding="10px 14px",
        min_width="0",
    )

def suggestions_panel() -> rx.Component:
    return rx.box(
        section_heading("Writing Moves", "What does the paragraph need next?"),
        rx.scroll_area(
            rx.flex(
                *[_move_card(c) for c in _MOVE_CARDS],
                direction="column",
                gap="3",
                min_width="0",
            ),
            type="hover", scrollbars="vertical", max_height="300px", margin_top="12px",
        ),
        style=t.CARD, width="100%", min_width="0",
    )