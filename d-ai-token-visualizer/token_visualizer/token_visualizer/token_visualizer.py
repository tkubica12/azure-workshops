"""Token Visualizer - Main application entry point."""

import reflex as rx
from .pages.interactive_mode import interactive_mode_page
from .pages.prompt_comparison import prompt_comparison_page
from .pages.token_tree import token_tree_page
from .pages.help import help_page


def index() -> rx.Component:
    """Main index page - shows help content."""
    return help_page()


app = rx.App()

app.add_page(index, route="/")
app.add_page(help_page, route="/help")
app.add_page(interactive_mode_page, route="/interactive")
app.add_page(prompt_comparison_page, route="/prompt-comparison")
app.add_page(token_tree_page, route="/token-tree")
