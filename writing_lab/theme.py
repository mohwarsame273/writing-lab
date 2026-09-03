"""Design tokens for Writing Lab.

Palette blends a BPP-style purple primary with an energetic accent set so the
product reads like a polished, modern learning app (DataCamp-adjacent) rather
than a corporate dashboard. Everything visual funnels through here so the shell
stays consistent and easy to re-skin.

The component vocabulary below is drawn from the uploaded UI design library
(component.gallery): Accordion, Alert/Callout, Avatar, Badge, Breadcrumbs,
Card, Progress, Tabs, Tooltip. Each maps to a component module under
components/.
"""
from __future__ import annotations

# --- brand + accent palette -------------------------------------------------
PURPLE = "#6E368A"       # primary / brand
PURPLE_SOFT = "#F3ECF7"  # tinted surfaces
INK = "#2D2D3D"          # near-black text (never pure black)
INK_SOFT = "#3C3C3B"
SLATE = "#7A7A7A"        # captions / secondary
BLUE = "#3763AD"         # technical / code
CYAN = "#89CFE1"
AMBER = "#F9B149"        # XP / rewards
ORANGE = "#E75B11"       # streak / urgency
RED = "#E94843"          # critical / high severity
TEAL = "#64BDB6"         # success / solutions
GREEN = "#2FA37C"

BG = "#FBFAFC"           # app background
SURFACE = "#FFFFFF"      # card surface
BORDER = "#E9E6EF"       # hairline borders
MUTED_BG = "#F5F3F8"

# severity -> colour, used by the diagnostics list
SEVERITY_COLOUR = {"low": SLATE, "medium": AMBER, "high": RED}

# diet verdict -> colour, used by the free-write profile
VERDICT_COLOUR = {
    "lean": GREEN,
    "fit-and-trim": TEAL,
    "needs-toning": AMBER,
    "flabby": ORANGE,
    "heart-attack": RED,
}

FONT = "Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# --- reusable style fragments ----------------------------------------------
CARD = dict(
    background=SURFACE,
    border=f"1px solid {BORDER}",
    border_radius="16px",
    padding="20px",
    box_shadow="0 1px 2px rgba(45,45,61,0.04), 0 8px 24px rgba(45,45,61,0.06)",
)

SOFT_CARD = dict(
    background=MUTED_BG,
    border=f"1px solid {BORDER}",
    border_radius="14px",
    padding="16px",
)

PILL = dict(
    display="inline-flex",
    align_items="center",
    gap="6px",
    padding="4px 10px",
    border_radius="999px",
    font_size="12px",
    font_weight="600",
)

# app-level style passed to rx.App(style=...)
APP_STYLE = {
    "font_family": FONT,
    "background": BG,
    "color": INK,
    "::selection": {"background": PURPLE_SOFT},
}


def theme_props() -> dict:
    """Props for rx.theme(); radix theme underneath the custom tokens."""
    return dict(
        appearance="light",
        accent_color="purple",
        gray_color="slate",
        radius="large",
        scaling="100%",
    )
