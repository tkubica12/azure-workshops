"""Probability bar components for visualizing token probabilities."""

import reflex as rx
from typing import List, Optional, Dict, Any
from ..services.llm_client import TokenProbability
from .color_coded_text import get_probability_color, get_probability_background_color, get_text_color


def token_pill(
    token: TokenProbability,
    is_selected: bool = False,
    show_percentage: bool = True,
    show_probability_value: bool = False
) -> rx.Component:
    """Create a color-coded pill for token display using the same colors as generated text.
    
    Args:
        token: TokenProbability object
        is_selected: Whether this token is selected
        show_percentage: Whether to show percentage
        show_probability_value: Whether to show raw probability
    """
    
    # Get probability percentage
    probability_percentage = token.percentage
    
    # Use the same color logic as in color_coded_text.py
    background_color = rx.cond(
        is_selected,
        "#1E40AF",  # Blue for selected
        rx.cond(
            probability_percentage >= 80,
            "#D1FAE5",  # Green-100
            rx.cond(
                probability_percentage >= 60,
                "#ECFDF5",  # Green-50
                rx.cond(
                    probability_percentage >= 40,
                    "#FEF3C7",  # Yellow-100
                    rx.cond(
                        probability_percentage >= 20,
                        "#FEF3C7",  # Yellow-100
                        rx.cond(
                            probability_percentage >= 10,
                            "#FED7AA",  # Orange-100
                            "#FEE2E2"  # Red-100
                        )
                    )
                )
            )
        )
    )
    
    # Text color for good contrast
    text_color = rx.cond(
        is_selected,
        "white",  # White text for selected (blue background)
        rx.cond(
            probability_percentage >= 60,
            "#065F46",  # Green-800
            rx.cond(
                probability_percentage >= 40,
                "#92400E",  # Yellow-800
                rx.cond(
                    probability_percentage >= 10,
                    "#C2410C",  # Orange-700
                    "#B91C1C"  # Red-700
                )
            )
        )
    )
    
    # Border color matching the text tokens
    border_color = rx.cond(
        is_selected,
        "#1E40AF",  # Blue border for selected
        rx.cond(
            probability_percentage >= 80,
            "#10B981",  # Green-500
            rx.cond(
                probability_percentage >= 60,
                "#34D399",  # Green-400
                rx.cond(
                    probability_percentage >= 40,
                    "#FCD34D",  # Yellow-300
                    rx.cond(
                        probability_percentage >= 20,
                        "#F59E0B",  # Amber-500
                        rx.cond(
                            probability_percentage >= 10,
                            "#F97316",  # Orange-500
                            "#EF4444"  # Red-500
                        )
                    )
                )
            )
        )
    )
    
    # Build display text
    display_text = rx.cond(
        show_percentage & show_probability_value,
        f'"{token.token}" {probability_percentage:.1f}% (p={token.probability:.3f})',
        rx.cond(
            show_percentage,
            f'"{token.token}" {probability_percentage:.1f}%',
            rx.cond(
                show_probability_value,
                f'"{token.token}" p={token.probability:.3f}',
                f'"{token.token}"'
            )
        )
    )
    
    return rx.box(
        rx.text(
            display_text,
            color=text_color,
            font_weight="500",
            font_size="0.875rem",
            white_space="nowrap",
            text_align="center"
        ),
        background=background_color,
        border=f"1px solid {border_color}",
        border_radius="0.375rem",
        padding="0.5rem 0.75rem",
        display="inline-block",
        width="100%",  # Use full width of allocated space instead of fixed min-width
        text_align="center"
    )


def probability_bar(
    token: TokenProbability,
    is_selected: bool = False,
    is_highlighted: bool = False,
    max_width: str = "100%",
    height: str = "1.5rem",
    show_token_text: bool = True,
    show_percentage: bool = True,
    show_probability_value: bool = False,
    animate: bool = True
) -> rx.Component:
    """Redesigned probability bar with progress bar and token pill on the same line.
    
    Args:
        token: TokenProbability object containing token text and probability
        is_selected: Whether this token is currently selected
        is_highlighted: Whether this token should be highlighted
        max_width: Maximum width of the bar container
        height: Height of the progress bar
        show_token_text: Whether to show token text in the pill
        show_percentage: Whether to show percentage value
        show_probability_value: Whether to show raw probability value
        animate: Whether to animate the bar fill
    """
    
    # Get probability percentage for width calculation
    probability_percentage = token.percentage
    bar_width = f"{probability_percentage}%"
    
    # Color-coded progress bar colors (same as token pill colors)
    bar_color = rx.cond(
        is_selected,
        "#1E40AF",  # Blue for selected
        rx.cond(
            probability_percentage >= 80,
            "#10B981",  # Green-500
            rx.cond(
                probability_percentage >= 60,
                "#34D399",  # Green-400
                rx.cond(
                    probability_percentage >= 40,
                    "#FCD34D",  # Yellow-300
                    rx.cond(
                        probability_percentage >= 20,
                        "#F59E0B",  # Amber-500
                        rx.cond(
                            probability_percentage >= 10,
                            "#F97316",  # Orange-500
                            "#EF4444"  # Red-500
                        )
                    )
                )
            )
        )
    )
    
    # Light track color
    track_color = "#F3F4F6"  # Gray-100
    
    return rx.hstack(
        # Progress bar takes 60% of available width
        rx.box(
            rx.box(
                width=bar_width,
                height="100%",
                background=bar_color,
                border_radius="0.25rem",
                transition=rx.cond(
                    animate,
                    "width 0.5s ease-in-out",
                    "none"
                )
            ),
            background=track_color,
            width="60%",  # Dynamic 60% of container width
            height=height,
            border_radius="0.25rem",
            border="1px solid #E5E7EB",
            overflow="hidden",
            flex_shrink="0"
        ),
        
        # Token pill takes remaining 40% of available width
        rx.box(
            token_pill(
                token=token,
                is_selected=is_selected,
                show_percentage=show_percentage,
                show_probability_value=show_probability_value
            ),
            width="40%",  # Dynamic 40% of container width
            display="flex",
            justify_content="flex-start",
            align_items="center",
            padding_left="1rem"
        ),
        
        spacing="0",  # No spacing since we're using percentage widths
        align="center",
        width="100%",  # Use full width
        margin_bottom="0.5rem"
    )


def probability_bars_list(
    tokens: List[TokenProbability],
    selected_index: Optional[int] = None,
    highlighted_indices: Optional[List[int]] = None,
    max_width: str = "100%",
    bar_height: str = "2.5rem",
    show_token_text: bool = True,
    show_percentage: bool = True,
    show_probability_value: bool = False,
    animate: bool = True,
    sort_by_probability: bool = True
) -> rx.Component:
    """List of probability bars for multiple tokens.
    
    Args:
        tokens: List of TokenProbability objects
        selected_index: Index of the selected token
        highlighted_indices: List of indices to highlight
        max_width: Maximum width of the bars container
        bar_height: Height of each bar
        show_token_text: Whether to show token text on bars
        show_percentage: Whether to show percentage values
        show_probability_value: Whether to show raw probability values
        animate: Whether to animate the bars
        sort_by_probability: Whether to sort bars by probability (descending)
    """
    
    return rx.cond(
        tokens.length() == 0,
        rx.box(
            rx.text(
                "No token probabilities to display",
                color="#6B7280",
                font_style="italic"
            ),
            padding="1rem"
        ),
        rx.vstack(
            rx.foreach(
                tokens,
                lambda token, index: probability_bar(
                    token=token,
                    is_selected=selected_index == index,
                    is_highlighted=False,  # Simplified for now - no highlighting in list view
                    max_width="100%",
                    height=bar_height,
                    show_token_text=show_token_text,
                    show_percentage=show_percentage,
                    show_probability_value=show_probability_value,
                    animate=animate
                )
            ),
            width=max_width,
            spacing="2"
        )
    )


def compact_probability_bar(
    token: TokenProbability,
    is_selected: bool = False,
    width: str = "100%",
    height: str = "1rem"
) -> rx.Component:
    """Compact version with progress bar and token pill on the same line for dense layouts.
    
    Args:
        token: TokenProbability object
        is_selected: Whether this token is selected
        width: Width of the container
        height: Height of the progress bar
    """
    
    probability_percentage = token.percentage
    bar_width = f"{probability_percentage}%"
    
    # Color-coded progress bar colors (same as main function)
    bar_color = rx.cond(
        is_selected,
        "#1E40AF",  # Blue for selected
        rx.cond(
            probability_percentage >= 80,
            "#10B981",  # Green-500
            rx.cond(
                probability_percentage >= 60,
                "#34D399",  # Green-400
                rx.cond(
                    probability_percentage >= 40,
                    "#FCD34D",  # Yellow-300
                    rx.cond(
                        probability_percentage >= 20,
                        "#F59E0B",  # Amber-500
                        rx.cond(
                            probability_percentage >= 10,
                            "#F97316",  # Orange-500
                            "#EF4444"  # Red-500
                        )
                    )
                )
            )
        )
    )
    
    return rx.hstack(
        # Compact progress bar takes 60% of available width
        rx.box(
            rx.box(
                width=bar_width,
                height="100%",
                background=bar_color,
                border_radius="0.125rem",
                transition="width 0.3s ease-in-out"
            ),
            background="#F3F4F6",
            width="60%",  # Dynamic 60% of container width
            height=height,
            border_radius="0.125rem",
            border="1px solid #E5E7EB",
            overflow="hidden",
            flex_shrink="0"
        ),
        
        # Compact token pill takes remaining 40%
        rx.box(
            token_pill(
                token=token,
                is_selected=is_selected,
                show_percentage=True,
                show_probability_value=False
            ),
            width="40%",  # Dynamic 40% of container width
            display="flex",
            justify_content="flex-start",
            align_items="center",
            padding_left="0.75rem"
        ),
        
        spacing="0",  # No spacing since we're using percentage widths
        align="center",
        width="100%",  # Use full width
        margin_bottom="0.25rem"
    )


def interactive_probability_bars(
    tokens: List[TokenProbability],
    selected_index: Optional[int] = None,
    on_token_select: Optional[rx.EventHandler] = None,
    show_rank_numbers: bool = True,
    show_token_text: bool = True,
    show_percentage: bool = True,
    animate: bool = True
) -> rx.Component:
    """Interactive probability bars that can be clicked to select tokens.
    
    Args:
        tokens: List of TokenProbability objects
        selected_index: Index of the currently selected token
        on_token_select: Event handler for token selection
        show_rank_numbers: Whether to show rank numbers
        show_token_text: Whether to show token text
        show_percentage: Whether to show percentage values
        animate: Whether to animate the bars
    """
    
    return rx.cond(
        tokens.length() == 0,
        rx.box(
            rx.text(
                "No tokens available for selection",
                color="#6B7280",
                font_style="italic"
            ),
            padding="1rem"
        ),
        rx.vstack(
            rx.text(
                "Select a token by clicking on its probability bar:",
                font_size="0.875rem",
                color="#6B7280",
                margin_bottom="0.5rem"
            ),
            rx.foreach(
                tokens,
                lambda token, index: rx.button(
                    rx.hstack(
                        # Rank number
                        rx.cond(
                            show_rank_numbers,
                            rx.text(
                                f"{index + 1}.",
                                font_size="0.75rem",
                                color="#6B7280",
                                font_weight="600",
                                width="1.5rem",
                                flex_shrink="0"
                            ),
                            rx.box()
                        ),
                        
                        # Probability bar
                        probability_bar(
                            token=token,
                            is_selected=selected_index == index,
                            is_highlighted=index == 0,  # Highlight top choice
                            max_width="100%",
                            height="2.25rem",
                            show_token_text=show_token_text,
                            show_percentage=show_percentage,
                            animate=animate
                        ),
                        
                        spacing="2",
                        align="center",
                        width="100%"
                    ),
                    
                    variant="ghost",
                    padding="0.5rem",
                    border_radius="0.5rem",
                    width="100%",
                    background=rx.cond(
                        selected_index == index,
                        "#F0F9FF",  # Light blue background for selected
                        "transparent"
                    ),
                    border=rx.cond(
                        selected_index == index,
                        "2px solid #1E40AF",
                        "2px solid transparent"
                    ),
                    _hover={
                        "background": rx.cond(
                            selected_index == index,
                            "#F0F9FF",
                            "#F8FAFC"
                        )
                    },
                    on_click=lambda index=index: on_token_select(index)
                )
            ),
            spacing="2",
            width="100%"
        )
    )
