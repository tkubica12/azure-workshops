"""Probability bar components for visualizing token probabilities."""

import reflex as rx
from typing import List, Optional, Dict, Any
from ..services.azure_openai import TokenProbability


def probability_bar(
    token: TokenProbability,
    is_selected: bool = False,
    is_highlighted: bool = False,
    max_width: str = "100%",
    height: str = "2.5rem",
    show_token_text: bool = True,
    show_percentage: bool = True,
    show_probability_value: bool = False,
    animate: bool = True
) -> rx.Component:
    """Single horizontal probability bar component.
    
    Args:
        token: TokenProbability object containing token text and probability
        is_selected: Whether this token is currently selected
        is_highlighted: Whether this token should be highlighted
        max_width: Maximum width of the bar container
        height: Height of the bar
        show_token_text: Whether to show token text on the bar
        show_percentage: Whether to show percentage value
        show_probability_value: Whether to show raw probability value
        animate: Whether to animate the bar fill
    """
    
    # Get probability percentage for width calculation
    probability_percentage = token.percentage
    bar_width = f"{probability_percentage}%"
    
    # Color coding based on probability ranges
    bar_color = rx.cond(
        is_selected,
        "#1E40AF",  # Dark blue for selected
        rx.cond(
            is_highlighted,
            "#7C3AED",  # Purple for highlighted
            rx.cond(
                probability_percentage >= 70,
                "#10B981",  # Green for very high probability
                rx.cond(
                    probability_percentage >= 40,
                    "#F59E0B",  # Orange for medium-high probability
                    rx.cond(
                        probability_percentage >= 15,
                        "#6366F1",  # Blue for medium probability
                        rx.cond(
                            probability_percentage >= 5,
                            "#EC4899",  # Pink for low probability
                            "#EF4444"  # Red for very low probability
                        )
                    )
                )
            )
        )
    )
    
    # Background color for the bar track
    track_color = rx.cond(
        is_selected,
        "#E5E7EB",  # Light gray for selected token track
        "#F3F4F6"  # Very light gray for normal track
    )
    
    # Text color based on bar size and selection
    text_color = rx.cond(
        is_selected,
        "white",
        rx.cond(
            probability_percentage >= 30,
            "white",  # White text on colored background
            "#374151"  # Dark text for small bars
        )
    )
    
    # Build probability display text
    prob_text_content = rx.cond(
        show_percentage & show_probability_value,
        f"{probability_percentage:.1f}% (p={token.probability:.3f})",
        rx.cond(
            show_percentage,
            f"{probability_percentage:.1f}%",
            rx.cond(
                show_probability_value,
                f"p={token.probability:.3f}",
                ""
            )
        )
    )
    
    return rx.box(
        # Background track
        rx.box(
            # Filled bar
            rx.box(
                # Content overlay
                rx.hstack(
                    # Token text (left side)
                    rx.cond(
                        show_token_text,
                        rx.text(
                            f'"{token.token}"',
                            font_weight="600",
                            font_size="0.875rem",
                            color=text_color,
                            margin_left="0.75rem",
                            white_space="pre"
                        ),
                        rx.box()
                    ),
                    
                    # Spacer
                    rx.spacer(),
                    
                    # Probability text (right side)
                    rx.cond(
                        show_percentage | show_probability_value,
                        rx.text(
                            prob_text_content,
                            font_size="0.75rem",
                            font_weight="500",
                            color=text_color,
                            margin_right="0.75rem"
                        ),
                        rx.box()
                    ),
                    
                    align="center",
                    height="100%",
                    width="100%"
                ),
                
                # Bar styling
                background=bar_color,
                width=bar_width,
                height="100%",
                border_radius="0.375rem",
                position="relative",
                transition=rx.cond(
                    animate,
                    "width 0.5s ease-in-out, background-color 0.3s ease",
                    "none"
                )
            ),
            
            # Track styling
            background=track_color,
            width="100%",
            height=height,
            border_radius="0.375rem",
            border=rx.cond(
                is_selected,
                "2px solid #1E40AF",
                "1px solid #E5E7EB"
            ),
            position="relative",
            overflow="hidden"
        ),
        
        width=max_width,
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
            spacing="1"
        )
    )


def compact_probability_bar(
    token: TokenProbability,
    is_selected: bool = False,
    width: str = "100%",
    height: str = "1.5rem"
) -> rx.Component:
    """Compact version of probability bar for dense layouts.
    
    Args:
        token: TokenProbability object
        is_selected: Whether this token is selected
        width: Width of the bar
        height: Height of the bar
    """
    
    probability_percentage = token.percentage
    bar_width = f"{probability_percentage}%"
    
    # Simplified color scheme for compact view
    bar_color = rx.cond(
        is_selected,
        "#1E40AF",
        rx.cond(
            probability_percentage >= 50,
            "#10B981",
            rx.cond(
                probability_percentage >= 25,
                "#F59E0B",
                "#6366F1"
            )
        )
    )
    
    return rx.box(
        rx.box(
            rx.hstack(
                rx.text(
                    token.token,
                    font_size="0.75rem",
                    font_weight="500",
                    color="white",
                    margin_left="0.5rem"
                ),
                rx.spacer(),
                rx.text(
                    f"{probability_percentage:.0f}%",
                    font_size="0.625rem",
                    color="white",
                    margin_right="0.5rem"
                ),
                align="center",
                height="100%",
                width="100%"
            ),
            background=bar_color,
            width=bar_width,
            height="100%",
            border_radius="0.25rem",
            transition="width 0.3s ease-in-out"
        ),
        background="#F3F4F6",
        width=width,
        height=height,
        border_radius="0.25rem",
        border="1px solid #E5E7EB",
        overflow="hidden",
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
