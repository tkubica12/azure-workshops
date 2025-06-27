"""Token Visualizer - Main application entry point."""

import reflex as rx


def index() -> rx.Component:
    """Main index page with Hello World message."""
    return rx.container(
        rx.vstack(
            rx.heading(
                "🚀 Token Visualizer",
                size="9",  # Valid Reflex heading size (1-9)
                color="blue.600",
                margin_bottom="1rem"
            ),
            rx.text(
                "Educational LLM Token Prediction Visualization Tool",
                size="4",  # Valid Reflex text size
                color="gray.600",
                margin_bottom="2rem"
            ),
            rx.box(
                rx.text(
                    "Hello World! 🌍",
                    size="6",  # Valid Reflex text size
                    weight="bold",
                    color="green.500"
                ),
                padding="2rem",
                border="2px solid",
                border_color="green.200",
                border_radius="lg",
                background="green.50"
            ),
            rx.text(
                "The Token Visualizer application is starting up...",
                color="gray.500",
                margin_top="1rem"
            ),
            spacing="1rem",
            align="center",
            min_height="100vh",
            justify="center"
        ),
        max_width="800px",
        margin="0 auto",
        padding="2rem"
    )


# Create the Reflex app
app = rx.App()

# Add the index page
app.add_page(index, route="/")
