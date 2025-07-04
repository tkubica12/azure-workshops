"""Main layout components for the Token Visualizer application."""

import reflex as rx
from typing import List
from ..state.ui_state import NavigationState
from .navigation import mode_navigation


def header() -> rx.Component:
    """Main application header with title and navigation."""
    return rx.box(
        rx.flex(
            # Left: Logo and title
            rx.hstack(
                rx.icon(
                    "brain-circuit",
                    size=32,
                    color="#2563EB",
                    margin_right="12px"
                ),
                rx.vstack(
                    rx.heading(
                        "Token Visualizer",
                        size="6",
                        color="#1A1A1A",
                        font_weight="600",
                        line_height="1.2"
                    ),
                    rx.text(
                        "Educational LLM Token Prediction Tool",
                        font_size="0.875rem",
                        color="#6B7280",
                        line_height="1.1"
                    ),
                    spacing="0",
                    align="start"
                ),
                align="center",
                spacing="0"
            ),
            
            # Right: Help button
            rx.link(
                rx.button(
                    rx.hstack(
                        rx.icon("circle-help", size=16),
                        rx.text("Help", font_size="0.875rem", font_weight="500"),
                        spacing="2",
                        align="center"
                    ),
                    variant="ghost",
                    size="3",
                    padding="0.75rem 1rem",
                    border_radius="0.375rem",
                    color="#64748B",
                    _hover={
                        "background": "#F1F5F9",
                        "color": "#334155"
                    }
                ),
                href="/help",
                text_decoration="none"
            ),
            
            justify="between",
            align="center",
            width="100%"
        ),
        
        # Header styling
        background="#FFFFFF",
        border_bottom="1px solid #E5E7EB",
        padding="32px 32px 16px 32px",
        position="sticky",
        top="0",
        z_index="50",
        backdrop_filter="blur(8px)",
        background_color="rgba(255, 255, 255, 0.95)"
    )


def sidebar() -> rx.Component:
    """Left sidebar for navigation and controls."""
    return rx.box(
        rx.vstack(
            # Mode Navigation
            mode_navigation(),
            
            spacing="4",
            align="stretch",
            height="100%"
        ),
        
        # Sidebar styling
        width="240px",
        min_width="240px",
        height="calc(100vh - 70px)",  # Full height minus header
        background="#FAFAFA",
        border_right="1px solid #E5E7EB",
        padding="1.5rem",
        position="sticky",
        top="70px"  # Height of header
    )


def main_content(children: List[rx.Component]) -> rx.Component:
    """Main content area that wraps page content."""
    return rx.box(
        rx.vstack(
            *children,
            spacing="5",
            align="stretch",
            width="100%",
            padding="32px"
        ),
        
        # Main content styling
        flex="1",
        min_height="calc(100vh - 70px)",
        background="#FFFFFF",
        overflow_y="auto"
    )


def app_layout(*children: rx.Component) -> rx.Component:
    """Main application layout with header, sidebar, and content (no right panel)."""
    return rx.box(
        # Header
        header(),
        
        # Main layout with sidebar and content
        rx.flex(
            # Left sidebar
            sidebar(),
            
            # Main content area
            main_content(list(children)),
            
            # Layout styling
            direction="row",
            width="100%",
            min_height="calc(100vh - 70px)"
        ),
        
        # Root styling
        min_height="100vh",
        background="#FFFFFF",
        font_family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    )
