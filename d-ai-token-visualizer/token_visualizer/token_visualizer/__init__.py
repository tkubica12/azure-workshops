"""Token Visualizer - Educational LLM Token Prediction Visualization Tool."""

import reflex as rx
from .components.layout import app_layout

__version__ = "0.1.0"
__author__ = "Token Visualizer Team"
__description__ = "Interactive visualization of LLM token generation probabilities using Azure OpenAI"


def welcome_content() -> rx.Component:
    """Welcome content for the main page."""
    return rx.vstack(
        # Welcome message
        rx.box(
            rx.vstack(
                rx.heading(
                    "Welcome to Token Visualizer",
                    size="8",
                    color="#1A1A1A",
                    font_weight="600",
                    text_align="center",
                    margin_bottom="1rem"
                ),
                rx.text(
                    "An educational tool to understand how Large Language Models generate text, one token at a time.",
                    font_size="1.125rem",
                    color="#6B7280",
                    text_align="center",
                    line_height="1.6",
                    max_width="600px"
                ),
                spacing="2",
                align="center"
            ),
            padding="3rem 2rem",
            border_radius="0.75rem",
            background="#FAFAFA",
            border="1px solid #E5E7EB",
            margin_bottom="3rem"
        ),
        
        # Status indicator
        rx.center(
            rx.box(
                rx.hstack(
                    rx.text("✓", font_size="1rem", color="#059669"),
                    rx.text(
                        "Phase 2.2 UI Structure Complete",
                        font_size="0.875rem",
                        color="#059669",
                        font_weight="500"
                    ),
                    spacing="2",
                    align="center"
                ),
                padding="12px 16px",
                border_radius="8px",
                background="#F0FDF4",
                border="1px solid #D1FAE5"
            ),
            margin_bottom="3rem"
        ),
        
        # Features grid
        rx.grid(
            rx.box(
                rx.vstack(
                    rx.text("🎯", font_size="2rem", margin_bottom="8px"),
                    rx.heading("Modern Layout", size="4", margin_bottom="8px", color="#1A1A1A"),
                    rx.text("Clean three-column responsive design", color="#6B7280", text_align="center"),
                    align="center"
                ),
                padding="2rem",
                border_radius="0.75rem",
                background="#FFFFFF",
                border="1px solid #E5E7EB"
            ),
            
            rx.box(
                rx.vstack(
                    rx.text("📱", font_size="2rem", margin_bottom="8px"),
                    rx.heading("Responsive", size="4", margin_bottom="8px", color="#1A1A1A"),
                    rx.text("Adapts to desktop, tablet, and mobile", color="#6B7280", text_align="center"),
                    align="center"
                ),
                padding="2rem",
                border_radius="0.75rem",
                background="#FFFFFF",
                border="1px solid #E5E7EB"
            ),
            
            rx.box(
                rx.vstack(
                    rx.text("🎨", font_size="2rem", margin_bottom="8px"),
                    rx.heading("Modern Design", size="4", margin_bottom="8px", color="#1A1A1A"),
                    rx.text("ChatGPT-inspired minimalist aesthetic", color="#6B7280", text_align="center"),
                    align="center"
                ),
                padding="2rem",
                border_radius="0.75rem",
                background="#FFFFFF",
                border="1px solid #E5E7EB"
            ),
            
            columns="3",
            gap="4",
            width="100%"
        ),
        
        spacing="2rem",
        align="stretch",
        width="100%",
        max_width="1200px",
        margin="0 auto"
    )


def index() -> rx.Component:
    """Main index page with modern layout."""
    return app_layout(
        welcome_content()
    )


# Create the Reflex app
app = rx.App()

# Add the index page
app.add_page(index, route="/")
