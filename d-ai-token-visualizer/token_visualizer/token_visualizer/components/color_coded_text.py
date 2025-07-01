"""Color-coded text display components for showing tokens with probability-based backgrounds."""

import reflex as rx
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from ..services.llm_client import TokenProbability


def get_probability_color(probability: float) -> str:
    """Get color for probability value using a gradient scale.
    
    Args:
        probability: Probability value between 0.0 and 1.0
        
    Returns:
        CSS color string
    """
    # Convert probability to percentage for easier calculation
    percentage = probability * 100
    
    if percentage >= 80:  # Very high probability (80-100%)
        return "#10B981"  # Green-500
    elif percentage >= 60:  # High probability (60-80%)
        return "#34D399"  # Green-400
    elif percentage >= 40:  # Medium-high probability (40-60%)
        return "#FCD34D"  # Yellow-300
    elif percentage >= 20:  # Medium-low probability (20-40%)
        return "#F59E0B"  # Amber-500
    elif percentage >= 10:  # Low probability (10-20%)
        return "#F97316"  # Orange-500
    else:  # Very low probability (0-10%)
        return "#EF4444"  # Red-500


def get_probability_background_color(probability: float) -> str:
    """Get background color for probability value using a lighter gradient scale.
    
    Args:
        probability: Probability value between 0.0 and 1.0
        
    Returns:
        CSS background color string
    """
    # Convert probability to percentage for easier calculation
    percentage = probability * 100
    
    if percentage >= 80:  # Very high probability (80-100%)
        return "#D1FAE5"  # Green-100
    elif percentage >= 60:  # High probability (60-80%)
        return "#ECFDF5"  # Green-50
    elif percentage >= 40:  # Medium-high probability (40-60%)
        return "#FEF3C7"  # Yellow-100
    elif percentage >= 20:  # Medium-low probability (20-40%)
        return "#FEF3C7"  # Yellow-100
    elif percentage >= 10:  # Low probability (10-20%)
        return "#FED7AA"  # Orange-100
    else:  # Very low probability (0-10%)
        return "#FEE2E2"  # Red-100


def get_text_color(probability: float) -> str:
    """Get text color for probability value to ensure good contrast.
    
    Args:
        probability: Probability value between 0.0 and 1.0
        
    Returns:
        CSS text color string
    """
    # Use darker colors for better readability
    percentage = probability * 100
    
    if percentage >= 60:  # High probability
        return "#065F46"  # Green-800
    elif percentage >= 40:  # Medium probability
        return "#92400E"  # Yellow-800
    elif percentage >= 10:  # Low probability
        return "#C2410C"  # Orange-700
    else:  # Very low probability
        return "#B91C1C"  # Red-700


@dataclass
class TokenWithProbability:
    """Represents a token with its probability information."""
    text: str
    probability: float
    percentage: float
    was_selected: bool = False
    alternatives: List[TokenProbability] = None


def probability_token_span_from_entry(
    entry,  # TokenHistoryEntry - will be Reflex Var when used with rx.foreach
    show_tooltip: bool = True,
    animate_on_hover: bool = True
) -> rx.Component:
    """Create a color-coded span for a token entry directly.
    
    Args:
        entry: TokenHistoryEntry with token information
        show_tooltip: Whether to show tooltip on hover
        animate_on_hover: Whether to animate on hover
        
    Returns:
        Reflex component for the token span
    """
    # Create the base span with color coding using entry properties directly
    token_span = rx.text(
        entry.token,
        display="inline",
        background_color=rx.cond(
            entry.percentage >= 80,
            "#D1FAE5",  # Green-100
            rx.cond(
                entry.percentage >= 60,
                "#ECFDF5",  # Green-50
                rx.cond(
                    entry.percentage >= 40,
                    "#FEF3C7",  # Yellow-100
                    rx.cond(
                        entry.percentage >= 20,
                        "#FEF3C7",  # Yellow-100
                        rx.cond(
                            entry.percentage >= 10,
                            "#FED7AA",  # Orange-100
                            "#FEE2E2"  # Red-100
                        )
                    )
                )
            )
        ),
        color=rx.cond(
            entry.percentage >= 60,
            "#065F46",  # Green-800
            rx.cond(
                entry.percentage >= 40,
                "#92400E",  # Yellow-800
                rx.cond(
                    entry.percentage >= 10,
                    "#C2410C",  # Orange-700
                    "#B91C1C"  # Red-700
                )
            )
        ),
        padding="0.125rem 0.25rem",
        border_radius="0.25rem",
        font_weight="500",  # Selected tokens are always bold
        border=rx.cond(
            entry.percentage >= 80,
            "1px solid #10B981",  # Green-500
            rx.cond(
                entry.percentage >= 60,
                "1px solid #34D399",  # Green-400
                rx.cond(
                    entry.percentage >= 40,
                    "1px solid #FCD34D",  # Yellow-300
                    rx.cond(
                        entry.percentage >= 20,
                        "1px solid #F59E0B",  # Amber-500
                        rx.cond(
                            entry.percentage >= 10,
                            "1px solid #F97316",  # Orange-500
                            "1px solid #EF4444"  # Red-500
                        )
                    )
                )
            )
        ),
        transition="all 0.2s ease-in-out" if animate_on_hover else None,
        _hover={
            "transform": "scale(1.05)",
            "box_shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
            "z_index": "10"
        } if animate_on_hover else None,
        cursor="help" if show_tooltip else "default",
        margin="0.0625rem"  # Small margin between tokens
    )
    
    if not show_tooltip:
        return token_span
    
    # Create simple string tooltip content (Reflex tooltips only accept strings)
    # Use string concatenation that works with Reflex Vars
    tooltip_text = "Token: '" + entry.token + "' | " + entry.percentage.to(str) + "% probability | Selected ✓"
    
    # Wrap in tooltip
    return rx.tooltip(
        token_span,
        content=tooltip_text,
        side="top"
    )


def color_coded_text_display(
    initial_prompt: str,
    token_history: List[Any],  # TokenHistoryEntry from token_state
    show_tooltips: bool = True,
    animate_on_hover: bool = True,
    max_width: str = "100%"
) -> rx.Component:
    """Display text with color-coded tokens based on their selection probabilities.
    
    Args:
        initial_prompt: The original prompt text
        token_history: List of TokenHistoryEntry objects (Reflex Var)
        show_tooltips: Whether to show tooltips on hover
        animate_on_hover: Whether to animate tokens on hover
        max_width: Maximum width of the display
        
    Returns:
        Reflex component for the color-coded text display
    """
    
    def render_token_entry(entry) -> rx.Component:
        """Render a single token entry with color coding."""
        return probability_token_span_from_entry(
            entry,
            show_tooltip=show_tooltips,
            animate_on_hover=animate_on_hover
        )
    
    return rx.box(
        # Initial prompt (not color-coded)
        rx.text(
            initial_prompt,
            display="inline",
            color="#374151",
            font_weight="400"
        ),
        # Color-coded tokens using rx.foreach
        rx.foreach(
            token_history,
            render_token_entry
        ),
        width="100%",
        max_width=max_width,
        line_height="1.8",
        overflow_wrap="break-word",
        word_break="break-word"
    )


def probability_legend() -> rx.Component:
    """Create a legend showing the probability color scale."""
    legend_items = [
        ("Very High (80-100%)", "#D1FAE5", "#065F46"),
        ("High (60-80%)", "#ECFDF5", "#065F46"),
        ("Medium (40-60%)", "#FEF3C7", "#92400E"),
        ("Low (20-40%)", "#FEF3C7", "#92400E"),
        ("Very Low (10-20%)", "#FED7AA", "#C2410C"),
        ("Minimal (0-10%)", "#FEE2E2", "#B91C1C")
    ]
    
    return rx.vstack(
        rx.text(
            "Probability Color Scale",
            font_weight="600",
            color="#374151",
            margin_bottom="0.5rem"
        ),
        rx.hstack(
            *[
                rx.hstack(
                    rx.box(
                        width="1rem",
                        height="1rem",
                        background_color=bg_color,
                        border=f"1px solid {get_probability_color(0.5)}",
                        border_radius="0.25rem"
                    ),
                    rx.text(
                        label,
                        font_size="0.75rem",
                        color=text_color
                    ),
                    spacing="1",
                    align="center"
                )
                for label, bg_color, text_color in legend_items
            ],
            spacing="3",
            flex_wrap="wrap",
            align="center"
        ),
        spacing="2",
        align="start",
        padding="1rem",
        background="#F9FAFB",
        border="1px solid #E5E7EB",
        border_radius="0.5rem",
        margin_top="1rem"
    )
