"""Navigation components for the Token Visualizer application."""

import reflex as rx
from typing import Optional


def nav_button(
    icon: str,
    label: str,
    is_active: bool = False,
    on_click: Optional[rx.EventHandler] = None
) -> rx.Component:
    """Reusable navigation button component."""
    return rx.button(
        rx.hstack(
            rx.icon(icon, size=16),
            rx.text(label, font_size="0.875rem", font_weight="500"),
            spacing="3",
            align="center",
            justify="start",
            width="100%"
        ),
        
        # Button styling based on active state
        variant="ghost",
        justify="start",
        width="100%",
        padding="0.75rem",
        border_radius="0.375rem",
        background="#F8FAFC" if is_active else "transparent",
        color="#1E40AF" if is_active else "#64748B",
        
        # Hover states
        _hover={
            "background": "#F1F5F9",
            "color": "#334155"
        },
        
        # Click handler
        on_click=on_click
    )


def mode_navigation() -> rx.Component:
    """Navigation component for different application modes."""
    return rx.vstack(
        rx.text(
            "Modes",
            font_size="0.75rem",
            font_weight="600",
            color="#6B7280",
            text_transform="uppercase",
            letter_spacing="0.05em",
            margin_bottom="0.5rem"
        ),
        
        # Mode navigation links
        rx.link(
            nav_button(
                icon="zap",
                label="Interactive Generation",
                is_active=False  # Will be determined by current route
            ),
            href="/interactive",
            text_decoration="none",
            width="100%"
        ),
        
        rx.link(
            nav_button(
                icon="columns",
                label="Prompt Comparison"
            ),
            href="/prompt-comparison",
            text_decoration="none",
            width="100%"
        ),
        
        rx.link(
            nav_button(
                icon="git-branch",
                label="Token Tree"
            ),
            href="/token-tree",
            text_decoration="none",
            width="100%"
        ),
        
        spacing="1",
        align="stretch",
        width="100%"
    )





def mobile_nav_toggle() -> rx.Component:
    """Mobile navigation toggle button."""
    return rx.button(
        rx.text("☰", font_size="1.25rem"),
        variant="ghost",
        size="sm",
        padding="0.5rem",
        border_radius="0.375rem",
        display=["block", "block", "none"],  # Show only on mobile/tablet
        _hover={"background": "#F3F4F6"}
    )


def top_navigation() -> rx.Component:
    """Top navigation bar for tablet/mobile views."""
    return rx.box(
        rx.flex(
            rx.hstack(
                mobile_nav_toggle(),
                rx.text(
                    "Token Visualizer",
                    font_size="1.125rem",
                    font_weight="600",
                    color="#1F2937"
                ),
                spacing="3",
                align="center"
            ),
            
            rx.hstack(
                rx.text("⚡", font_size="1rem"),
                rx.text("Interactive Mode", font_size="0.875rem", color="#6B7280"),
                spacing="2",
                align="center"
            ),
            
            justify="between",
            align="center",
            width="100%"
        ),
        
        # Mobile nav styling
        display=["block", "block", "none"],  # Show only on mobile/tablet
        background="#FFFFFF",
        border_bottom="1px solid #E5E7EB",
        padding="1rem",
        position="sticky",
        top="70px",  # Below main header
        z_index="40"
    )
