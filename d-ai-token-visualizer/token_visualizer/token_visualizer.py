"""Token Visualizer - Main application entry point."""

import reflex as rx


def index() -> rx.Component:
    """Main index page with Hello World message."""
    return rx.container(
        rx.vstack(
            rx.heading(
                "🚀 Token Visualizer",
                size="9",  # Valid Reflex heading size (1-9)
                color_scheme="blue",
                margin_bottom="4"
            ),
            rx.text(
                "Educational LLM Token Prediction Visualization Tool",
                size="4",  # Valid Reflex text size
                color_scheme="gray",
                margin_bottom="6"
            ),
            rx.box(
                rx.text(
                    "Hello World! 🌍",
                    size="6",  # Valid Reflex text size
                    weight="bold",
                    color_scheme="green"
                ),
                padding="4",
                border_width="2",
                border_color="green",
                border_radius="4",
                background_color="green"
            ),
            rx.text(
                "The Token Visualizer application is starting up...",
                color_scheme="gray",
                margin_top="4"
            ),
            spacing="4",
            align="center",
            min_height="100vh",
            justify="center"
        ),
        max_width="800px",
        margin_x="auto",
        padding="6"
    )


# Create the Reflex app
app = rx.App()

# Add the index page
app.add_page(index, route="/")
