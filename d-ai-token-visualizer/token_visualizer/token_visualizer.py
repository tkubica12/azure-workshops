"""Token Visualizer - Main application entry point."""

import reflex as rx
from .components.layout import app_layout
from .pages.config_test import config_test_page
from .pages.state_test import state_test_page
from .pages.token_display_test import token_display_test_page
from .pages.probability_bar_test import probability_bar_test_page


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
        
        # Getting started section
        rx.vstack(
            rx.heading(
                "Getting Started",
                size="6",
                color="#1A1A1A",
                font_weight="600",
                margin_bottom="2rem"
            ),
            
            rx.grid(
                # Step 1
                rx.box(
                    rx.vstack(
                        rx.box(
                            rx.text("1", font_size="1.5rem", font_weight="600", color="#1A1A1A"),
                            width="3rem",
                            height="3rem",
                            border_radius="50%",
                            background="#F3F4F6",
                            border="2px solid #E5E7EB",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            margin_bottom="1rem"
                        ),
                        rx.heading(
                            "Enter a Prompt",
                            size="4",
                            color="#1A1A1A",
                            font_weight="600",
                            margin_bottom="0.5rem"
                        ),
                        rx.text(
                            "Start by typing any text prompt. The AI will analyze it and show you the most likely next tokens.",
                            color="#6B7280",
                            text_align="center",
                            line_height="1.5"
                        ),
                        align="center",
                        spacing="2"
                    ),
                    padding="2rem",
                    border_radius="0.75rem",
                    background="#FFFFFF",
                    border="1px solid #E5E7EB"
                ),
                
                # Step 2
                rx.box(
                    rx.vstack(
                        rx.box(
                            rx.text("2", font_size="1.5rem", font_weight="600", color="#1A1A1A"),
                            width="3rem",
                            height="3rem",
                            border_radius="50%",
                            background="#F3F4F6",
                            border="2px solid #E5E7EB",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            margin_bottom="1rem"
                        ),
                        rx.heading(
                            "Select Tokens",
                            size="4",
                            color="#1A1A1A",
                            font_weight="600",
                            margin_bottom="0.5rem"
                        ),
                        rx.text(
                            "Choose from the 5 most likely next tokens. Each token shows its probability of being selected.",
                            color="#6B7280",
                            text_align="center",
                            line_height="1.5"
                        ),
                        align="center",
                        spacing="2"
                    ),
                    padding="2rem",
                    border_radius="0.75rem",
                    background="#FFFFFF",
                    border="1px solid #E5E7EB"
                ),
                
                # Step 3
                rx.box(
                    rx.vstack(
                        rx.box(
                            rx.text("3", font_size="1.5rem", font_weight="600", color="#1A1A1A"),
                            width="3rem",
                            height="3rem",
                            border_radius="50%",
                            background="#F3F4F6",
                            border="2px solid #E5E7EB",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                            margin_bottom="1rem"
                        ),
                        rx.heading(
                            "Learn & Explore",
                            size="4",
                            color="#1A1A1A",
                            font_weight="600",
                            margin_bottom="0.5rem"
                        ),
                        rx.text(
                            "Watch how your choices affect the next set of predictions. Explore different modes and visualizations.",
                            color="#6B7280",
                            text_align="center",
                            line_height="1.5"
                        ),
                        align="center",
                        spacing="2"
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
            
            spacing="4",
            align="stretch",
            width="100%"
        ),
        
        # Call to action
        rx.center(
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon("zap", size=18, color="#FFFFFF"),
                        rx.text("Start Interactive Mode", font_size="1rem", font_weight="500"),
                        spacing="2",
                        align="center"
                    ),
                    size="4",
                    color_scheme="gray",
                    variant="outline",
                    padding="1rem 2rem",
                    border_radius="0.5rem",
                    _hover={
                        "background": "#F9FAFB"
                    }
                ),
                rx.link(
                    rx.button(
                        rx.hstack(
                            rx.icon("eye", size=18, color="#FFFFFF"),
                            rx.text("Test Token Display", font_size="1rem", font_weight="500"),
                            spacing="2",
                            align="center"
                        ),
                        size="4",
                        color_scheme="green",
                        variant="solid",
                        padding="1rem 2rem",
                        border_radius="0.5rem",
                        _hover={
                            "background": "#059669"
                        }
                    ),
                    href="/token-display-test"
                ),
                rx.link(
                    rx.button(
                        rx.hstack(
                            rx.icon("settings", size=18, color="#FFFFFF"),
                            rx.text("Test Configuration", font_size="1rem", font_weight="500"),
                            spacing="2",
                            align="center"
                        ),
                        size="4",
                        color_scheme="blue",
                        variant="solid",
                        padding="1rem 2rem",
                        border_radius="0.5rem",
                        _hover={
                            "background": "#1D4ED8"
                        }
                    ),
                    href="/config-test"
                ),
                spacing="4",
                align="center",
                margin_top="3rem"
            ),
            width="100%"
        ),
        
        spacing="5",
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

# Add the configuration test page
app.add_page(config_test_page, route="/config-test")

# Add the state management test page
app.add_page(state_test_page, route="/state-test")

# Add the token display test page
app.add_page(token_display_test_page, route="/token-display-test")

# Add the probability bar test page
app.add_page(probability_bar_test_page, route="/probability-bar-test")
