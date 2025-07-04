"""Token Visualizer - Main application entry point."""

import reflex as rx
from .pages.interactive_mode import interactive_mode_page
from .pages.prompt_comparison import prompt_comparison_page
from .pages.token_tree import token_tree_page
from .pages.help import help_page


def index() -> rx.Component:
    """Main index page - shows help content."""
    return help_page()


# Create the Reflex app
app = rx.App()

# Add the index page (help)
app.add_page(index, route="/")

# Add the help page as a separate route too
app.add_page(help_page, route="/help")

# Add the interactive mode page
app.add_page(interactive_mode_page, route="/interactive")

# Add the prompt comparison page
app.add_page(prompt_comparison_page, route="/prompt-comparison")

# Add the token tree page
app.add_page(token_tree_page, route="/token-tree")
