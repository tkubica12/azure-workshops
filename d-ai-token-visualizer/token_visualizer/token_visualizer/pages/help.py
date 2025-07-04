"""Help page explaining the three core modes of Token Visualizer."""

import reflex as rx
from ..components.layout import app_layout


def mode_explanation_card(
    title: str,
    description: str,
    icon: str,
    features: list,
    route: str
) -> rx.Component:
    """Create a card explaining one of the three modes."""
    return rx.box(
        rx.flex(
            # Content area that grows to fill available space
            rx.vstack(
                # Mode header
                rx.hstack(
                    rx.icon(icon, size=24, color="#2563EB"),
                    rx.heading(
                        title,
                        size="5",
                        color="#1A1A1A",
                        font_weight="600"
                    ),
                    spacing="3",
                    align="center",
                    margin_bottom="1rem"
                ),
                
                # Description
                rx.text(
                    description,
                    color="#6B7280",
                    line_height="1.6",
                    margin_bottom="1.5rem"
                ),
                
                # Features list
                rx.vstack(
                    *[
                        rx.hstack(
                            rx.icon("check", size=16, color="#10B981"),
                            rx.text(feature, font_size="0.9rem", color="#374151"),
                            spacing="2",
                            align="center"
                        )
                        for feature in features
                    ],
                    spacing="2",
                    align="start",
                    width="100%",
                    margin_bottom="2rem"  # Add space below the feature list
                ),
                
                spacing="0",
                align="start",
                width="100%",
                flex="1"  # This makes the content area grow
            ),
            
            # Try it button anchored to bottom
            rx.link(
                rx.button(
                    f"Try {title}",
                    variant="solid",
                    size="3",
                    width="100%",
                    background="#2563EB",
                    color="white",
                    _hover={"background": "#1D4ED8"}
                ),
                href=route,
                text_decoration="none",
                width="100%"
            ),
            
            direction="column",
            width="100%",
            min_height="100%"
        ),
        padding="2rem",
        border_radius="0.75rem",
        background="#FFFFFF",
        border="1px solid #E5E7EB",
        _hover={
            "border_color": "#D1D5DB",
            "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
        },
        transition="all 0.2s ease",
        height="100%"  # Ensure the card takes full height
    )


def help_content() -> rx.Component:
    """Help page content explaining the three core modes."""
    return rx.vstack(
        # Page header
        rx.box(
            rx.vstack(
                rx.heading(
                    "Token Visualizer",
                    size="8",
                    color="#1A1A1A",
                    font_weight="700",
                    text_align="center",
                    margin_bottom="1rem"
                ),
                rx.text(
                    "An educational tool to understand how Large Language Models generate text, one token at a time.",
                    font_size="1.25rem",
                    color="#6B7280",
                    text_align="center",
                    line_height="1.6",
                    max_width="700px"
                ),
                spacing="2",
                align="center"
            ),
            padding="3rem 2rem",
            border_radius="0.75rem",
            background="#F8FAFC",
            border="1px solid #E5E7EB",
            margin_bottom="3rem"
        ),
        
        # Introduction
        rx.box(
            rx.vstack(
                rx.heading(
                    "Choose Your Learning Mode",
                    size="6",
                    color="#1A1A1A",
                    font_weight="600",
                    text_align="center",
                    margin_bottom="1rem"
                ),
                rx.text(
                    "Token Visualizer offers three different ways to explore how Large Language Models predict and generate text. Each mode is designed to help you understand different aspects of LLM behavior.",
                    color="#6B7280",
                    text_align="center",
                    line_height="1.6",
                    max_width="600px"
                ),
                spacing="2",
                align="center"
            ),
            margin_bottom="3rem"
        ),
        
        # Three modes grid
        rx.grid(
            # Mode 1: Interactive Generation
            mode_explanation_card(
                title="Interactive Generation",
                description="Experience step-by-step token generation where you choose each next token from the most probable options. Perfect for understanding how context affects predictions.",
                icon="zap",
                features=[
                    "Enter any prompt to start",
                    "See top 5 most likely next tokens",
                    "Color-coded probability visualization",
                    "Build text token by token",
                    "Control generation with temperature settings"
                ],
                route="/interactive"
            ),
            
            # Mode 2: Prompt Comparison
            mode_explanation_card(
                title="Prompt Comparison",
                description="Compare how different prompts affect next-token probabilities side by side. Ideal for understanding prompt engineering and context sensitivity.",
                icon="columns",
                features=[
                    "Compare up to 3 prompts simultaneously",
                    "See how small changes affect predictions",
                    "Fixed temperature for consistent comparison",
                    "Color-coded probability display",
                    "Side-by-side visualization"
                ],
                route="/prompt-comparison"
            ),
            
            # Mode 3: Token Tree
            mode_explanation_card(
                title="Token Tree",
                description="Explore branching paths of token generation in an interactive tree structure. Perfect for visualizing how different choices lead to different outcomes.",
                icon="git-branch",
                features=[
                    "Interactive tree visualization",
                    "Explore multiple generation paths",
                    "Click any node to branch from there",
                    "Configurable tree depth",
                    "Visual probability weighting"
                ],
                route="/token-tree"
            ),
            
            columns="3",
            gap="2rem",
            width="100%",
            align_items="stretch"  # Ensure equal height cards
        ),
        
        spacing="0",
        align="center",
        width="100%",
        max_width="1200px",
        margin="0 auto"
    )


def help_page() -> rx.Component:
    """Help page explaining the three core modes."""
    return app_layout(
        help_content()
    )
