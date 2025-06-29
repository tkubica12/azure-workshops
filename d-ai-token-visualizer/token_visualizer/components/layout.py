"""Main layout components for the Token Visualizer application."""

import reflex as rx
from typing import List
from ..state.ui_state import NavigationState


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
            
            # Right: Future navigation will go here
            rx.box(
                width="0px"  # Placeholder for future navigation
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
            # Navigation placeholder
            rx.text(
                "Navigation",
                font_size="0.75rem",
                font_weight="600",
                color="#6B7280",
                text_transform="uppercase",
                letter_spacing="0.05em",
                margin_bottom="16px"
            ),
            
            # Mode buttons (placeholder)
            rx.vstack(
                rx.button(
                    rx.hstack(
                        rx.icon("zap", size=16, color=rx.cond(NavigationState.current_mode == "interactive", "#FFFFFF", "#6B7280")),
                        rx.text("Interactive Mode", font_size="0.875rem"),
                        spacing="2",
                        align="center"
                    ),
                    variant="ghost",
                    color_scheme="gray",
                    justify="start",
                    width="100%",
                    padding="0.75rem",
                    border_radius="0.5rem",
                    background=rx.cond(NavigationState.current_mode == "interactive", "#2563EB", "#F3F4F6"),
                    color=rx.cond(NavigationState.current_mode == "interactive", "#FFFFFF", "#374151"),
                    _hover={"background": rx.cond(NavigationState.current_mode == "interactive", "#1D4ED8", "#E5E7EB")},
                    border="1px solid #E5E7EB",
                    on_click=NavigationState.set_mode("interactive")
                ),
                
                rx.button(
                    rx.hstack(
                        rx.icon("activity", size=16, color=rx.cond(NavigationState.current_mode == "live_probability", "#FFFFFF", "#6B7280")),
                        rx.text("Live Probability", font_size="0.875rem"),
                        spacing="2",
                        align="center"
                    ),
                    variant="ghost",
                    color_scheme="gray",
                    justify="start",
                    width="100%",
                    padding="0.75rem",
                    border_radius="0.5rem",
                    background=rx.cond(NavigationState.current_mode == "live_probability", "#2563EB", "transparent"),
                    color=rx.cond(NavigationState.current_mode == "live_probability", "#FFFFFF", "#374151"),
                    _hover={"background": rx.cond(NavigationState.current_mode == "live_probability", "#1D4ED8", "#F3F4F6")},
                    border="1px solid transparent",
                    on_click=NavigationState.set_mode("live_probability")
                ),
                
                rx.button(
                    rx.hstack(
                        rx.icon("palette", size=16, color=rx.cond(NavigationState.current_mode == "color_visualization", "#FFFFFF", "#6B7280")),
                        rx.text("Color Visualization", font_size="0.875rem"),
                        spacing="2",
                        align="center"
                    ),
                    variant="ghost",
                    color_scheme="gray",
                    justify="start",
                    width="100%",
                    padding="0.75rem",
                    border_radius="0.5rem",
                    background=rx.cond(NavigationState.current_mode == "color_visualization", "#2563EB", "transparent"),
                    color=rx.cond(NavigationState.current_mode == "color_visualization", "#FFFFFF", "#374151"),
                    _hover={"background": rx.cond(NavigationState.current_mode == "color_visualization", "#1D4ED8", "#F3F4F6")},
                    border="1px solid transparent",
                    on_click=NavigationState.set_mode("color_visualization")
                ),
                
                spacing="2",
                align="stretch",
                width="100%"
            ),
            
            # Spacer
            rx.spacer(),
            
            # Settings placeholder
            rx.button(
                rx.hstack(
                    rx.icon("settings", size=16, color="#6B7280"),
                    rx.text("Settings", font_size="0.875rem"),
                    spacing="2",
                    align="center"
                ),
                variant="ghost",
                color_scheme="gray",
                justify="start",
                width="100%",
                padding="0.75rem",
                border_radius="0.5rem",
                _hover={"background": "#F3F4F6"}
            ),
            
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


def info_panel() -> rx.Component:
    """Right info panel for statistics and help."""
    return rx.box(
        rx.vstack(
            # Statistics section
            rx.text(
                "Session Stats",
                font_size="0.875rem",
                font_weight="600",
                color="#374151",
                margin_bottom="16px"
            ),
            
            rx.vstack(
                rx.box(
                    rx.vstack(
                        rx.text("Tokens Generated", font_size="0.75rem", color="#6B7280"),
                        rx.text("0", font_size="1.5rem", font_weight="700", color="#1F2937"),
                        spacing="1",
                        align="center"
                    ),
                    padding="1rem",
                    border_radius="0.5rem",
                    background="#F9FAFB",
                    border="1px solid #E5E7EB"
                ),
                
                rx.box(
                    rx.vstack(
                        rx.text("Avg Probability", font_size="0.75rem", color="#6B7280"),
                        rx.text("-%", font_size="1.5rem", font_weight="700", color="#1F2937"),
                        spacing="1",
                        align="center"
                    ),
                    padding="1rem",
                    border_radius="0.5rem",
                    background="#F9FAFB",
                    border="1px solid #E5E7EB"
                ),
                
                spacing="3",
                align="stretch",
                width="100%"
            ),
            
            # Spacer
            rx.spacer(),
            
            # Help section
            rx.text(
                "How to Use",
                font_size="0.875rem",
                font_weight="600",
                color="#374151",
                margin_bottom="16px",
                margin_top="32px"
            ),
            
            rx.vstack(
                rx.text(
                    "1. Enter a prompt to start",
                    font_size="0.8rem",
                    color="#6B7280",
                    line_height="1.4"
                ),
                rx.text(
                    "2. Select tokens interactively",
                    font_size="0.8rem",
                    color="#6B7280",
                    line_height="1.4"
                ),
                rx.text(
                    "3. Watch probabilities change",
                    font_size="0.8rem",
                    color="#6B7280",
                    line_height="1.4"
                ),
                spacing="2",
                align="start",
                width="100%"
            ),
            
            spacing="4",
            align="stretch",
            height="100%"
        ),
        
        # Info panel styling
        width="240px",
        min_width="240px",
        height="calc(100vh - 70px)",  # Full height minus header
        background="#FAFAFA",
        border_left="1px solid #E5E7EB",
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
    """Main application layout with header, sidebar, content, and info panel."""
    return rx.box(
        # Header
        header(),
        
        # Main layout with sidebar, content, and info panel
        rx.flex(
            # Left sidebar
            sidebar(),
            
            # Main content area
            main_content(list(children)),
            
            # Right info panel
            info_panel(),
            
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
