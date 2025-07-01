"""Token display components for the Token Visualizer application."""

import reflex as rx
from typing import List, Optional, Dict, Any
from ..services.llm_client import TokenProbability


def token_button(
    token: TokenProbability,
    is_selected: bool = False,
    is_highlighted: bool = False,
    on_click: Optional[rx.EventHandler] = None,
    show_probability_text: bool = True,
    show_percentage: bool = True
) -> rx.Component:
    """Individual token button component with probability visualization.
    
    Args:
        token: TokenProbability object containing token text and probability
        is_selected: Whether this token is currently selected
        is_highlighted: Whether this token should be highlighted (e.g., top choice)
        on_click: Event handler for token selection
        show_probability_text: Whether to show probability as text
        show_percentage: Whether to show percentage value
    """
    
    # Get probability percentage (works with both static data and state variables)
    probability_percentage = token.percentage
    
    # Use rx.cond for conditional styling based on probability ranges and state
    bg_color = rx.cond(
        is_selected,
        "#1E40AF",  # Dark blue for selected
        rx.cond(
            is_highlighted,
            "#7C3AED",  # Purple for highlighted
            rx.cond(
                probability_percentage >= 50,
                "#10B981",  # Green for high probability
                rx.cond(
                    probability_percentage >= 25,
                    "#F59E0B",  # Orange for medium probability
                    rx.cond(
                        probability_percentage >= 10,
                        "#6366F1",  # Blue for low-medium probability
                        "#EF4444"  # Red for very low probability
                    )
                )
            )
        )
    )
    
    hover_bg = rx.cond(
        is_selected,
        "#1E3A8A",  # Dark blue hover for selected
        rx.cond(
            is_highlighted,
            "#6D28D9",  # Purple hover for highlighted
            rx.cond(
                probability_percentage >= 50,
                "#059669",  # Green hover for high probability
                rx.cond(
                    probability_percentage >= 25,
                    "#D97706",  # Orange hover for medium probability
                    rx.cond(
                        probability_percentage >= 10,
                        "#4F46E5",  # Blue hover for low-medium probability
                        "#DC2626"  # Red hover for very low probability
                    )
                )
            )
        )
    )
    
    # Build the token content
    token_content = [
        # Token text (main content)
        rx.text(
            f'"{token.token}"',
            font_weight="600",
            font_size="0.875rem",
            color="white",
            margin_bottom=rx.cond(
                show_probability_text | show_percentage,
                "0.125rem",
                "0"
            )
        )
    ]
    
    # Add probability information conditionally
    prob_display = rx.cond(
        show_probability_text | show_percentage,
        rx.cond(
            show_percentage & show_probability_text,
            rx.text(
                f"{probability_percentage:.1f}% | p={token.probability:.3f}",
                font_size="0.75rem",
                color="rgba(255, 255, 255, 0.8)",
                font_weight="400"
            ),
            rx.cond(
                show_percentage,
                rx.text(
                    f"{probability_percentage:.1f}%",
                    font_size="0.75rem",
                    color="rgba(255, 255, 255, 0.8)",
                    font_weight="400"
                ),
                rx.cond(
                    show_probability_text,
                    rx.text(
                        f"p={token.probability:.3f}",
                        font_size="0.75rem",
                        color="rgba(255, 255, 255, 0.8)",
                        font_weight="400"
                    ),
                    rx.box()  # Empty box if neither is shown
                )
            )
        ),
        rx.box()  # Empty box if no probability info
    )
    
    return rx.button(
        rx.vstack(
            *token_content,
            prob_display,
            spacing="0",
            align="center",
            justify="center",
            width="100%"
        ),
        background=bg_color,
        color="white",
        border="2px solid transparent",
        border_color=rx.cond(is_selected, "#374151", "transparent"),
        border_radius="0.5rem",
        padding="0.75rem 1rem",
        min_width="120px",
        min_height="80px",
        _hover={
            "background": hover_bg,
            "transform": "scale(1.02)",
            "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.15)"
        },
        _active={
            "transform": "scale(0.98)"
        },
        transition="all 0.2s ease-in-out",
        cursor="pointer",
        on_click=on_click,
        width="100%"
    )


def token_alternatives_grid(
    alternatives: List[TokenProbability],
    selected_index: Optional[int] = None,
    on_token_select: Optional[rx.EventHandler] = None,
    max_columns: int = 3,
    show_probability_text: bool = True,
    show_percentage: bool = True
) -> rx.Component:
    """Grid display of token alternatives for selection.
    
    Args:
        alternatives: List of TokenProbability objects to display
        selected_index: Index of currently selected token (if any)
        on_token_select: Event handler that receives the token index
        max_columns: Maximum number of columns in the grid
        show_probability_text: Whether to show probability values
        show_percentage: Whether to show percentage values
    """
    
    return rx.box(
        rx.cond(
            alternatives.length() > 0,
            rx.grid(
                # Create buttons for the first few alternatives (simple static approach for now)
                rx.cond(
                    alternatives.length() > 0,
                    token_button(
                        token=alternatives[0],
                        is_selected=rx.cond(selected_index == 0, True, False),
                        is_highlighted=True,  # First token is highlighted
                        on_click=lambda: on_token_select(0) if on_token_select else None,
                        show_probability_text=show_probability_text,
                        show_percentage=show_percentage
                    ),
                    rx.box()
                ),
                rx.cond(
                    alternatives.length() > 1,
                    token_button(
                        token=alternatives[1],
                        is_selected=rx.cond(selected_index == 1, True, False),
                        is_highlighted=False,
                        on_click=lambda: on_token_select(1) if on_token_select else None,
                        show_probability_text=show_probability_text,
                        show_percentage=show_percentage
                    ),
                    rx.box()
                ),
                rx.cond(
                    alternatives.length() > 2,
                    token_button(
                        token=alternatives[2],
                        is_selected=rx.cond(selected_index == 2, True, False),
                        is_highlighted=False,
                        on_click=lambda: on_token_select(2) if on_token_select else None,
                        show_probability_text=show_probability_text,
                        show_percentage=show_percentage
                    ),
                    rx.box()
                ),
                rx.cond(
                    alternatives.length() > 3,
                    token_button(
                        token=alternatives[3],
                        is_selected=rx.cond(selected_index == 3, True, False),
                        is_highlighted=False,
                        on_click=lambda: on_token_select(3) if on_token_select else None,
                        show_probability_text=show_probability_text,
                        show_percentage=show_percentage
                    ),
                    rx.box()
                ),
                columns=str(max_columns),
                spacing="4",
                width="100%"
            ),
            rx.box(
                rx.text(
                    "No token alternatives available",
                    color="#6B7280",
                    font_size="0.875rem",
                    text_align="center"
                ),
                padding="2rem",
                width="100%"
            )
        ),
        width="100%"
    )


def token_selection_header(
    current_text: str = "",
    total_tokens: int = 0,
    show_next_instruction: bool = True
) -> rx.Component:
    """Header component showing current generation state and instructions.
    
    Args:
        current_text: The current generated text
        total_tokens: Number of tokens generated so far
        show_next_instruction: Whether to show "select next token" instruction
    """
    
    return rx.vstack(
        # Current text display
        rx.box(
            rx.heading(
                "Current Text:",
                size="4",
                margin_bottom="0.5rem",
                color="#374151"
            ),
            rx.box(
                rx.text(
                    rx.cond(
                        current_text,
                        current_text,
                        "No text generated yet..."
                    ),
                    font_size="1rem",
                    line_height="1.6",
                    color=rx.cond(
                        current_text,
                        "#111827",
                        "#9CA3AF"
                    ),
                    font_style=rx.cond(
                        current_text,
                        "normal",
                        "italic"
                    ),
                    white_space="pre-wrap"  # Preserve line breaks
                ),
                background="#F9FAFB",
                border="1px solid #E5E7EB",
                border_radius="0.5rem",
                padding="1rem",
                min_height="80px",
                width="100%"
            ),
            width="100%"
        ),
        
        # Statistics and instructions
        rx.hstack(
            rx.text(
                f"Tokens generated: {total_tokens}",
                font_size="0.875rem",
                color="#6B7280",
                font_weight="500"
            ),
            rx.spacer(),
            rx.cond(
                show_next_instruction,
                rx.text(
                    "Select the next token to continue generation",
                    font_size="0.875rem",
                    color="#4F46E5",
                    font_weight="500",
                    font_style="italic"
                ),
                rx.fragment()
            ),
            width="100%",
            align="center"
        ),
        
        spacing="4",
        width="100%"
    )


def token_generation_controls(
    on_generate_next: Optional[rx.EventHandler] = None,
    on_reset: Optional[rx.EventHandler] = None,
    on_undo_last: Optional[rx.EventHandler] = None,
    is_generating: bool = False,
    can_undo: bool = False,
    can_generate: bool = True
) -> rx.Component:
    """Control buttons for token generation flow.
    
    Args:
        on_generate_next: Handler for generating next token alternatives (not used - kept for compatibility)
        on_reset: Handler for resetting the generation
        on_undo_last: Handler for undoing the last token selection
        is_generating: Whether generation is currently in progress
        can_undo: Whether undo is available
        can_generate: Whether generation can proceed (not used - kept for compatibility)
    """
    
    return rx.hstack(
        # Undo Last Token button
        rx.button(
            rx.hstack(
                rx.icon("undo", size=16),
                rx.text("Undo Last", font_weight="500"),
                spacing="2",
                align="center"
            ),
            variant="outline",
            color="#6B7280",
            border_color="#D1D5DB",
            _hover=rx.cond(
                can_undo,
                {"background": "#F3F4F6"},
                {}
            ),
            _disabled={"color": "#9CA3AF", "cursor": "not-allowed"},
            disabled=rx.cond(
                ~can_undo | is_generating,
                True,
                False
            ),
            on_click=on_undo_last,
            padding="0.75rem 1.5rem",
            border_radius="0.5rem"
        ),
        
        # Reset Generation button
        rx.button(
            rx.hstack(
                rx.icon("refresh-cw", size=16),
                rx.text("Reset", font_weight="500"),
                spacing="2",
                align="center"
            ),
            variant="outline",
            color="#EF4444",
            border_color="#EF4444",
            _hover={"background": "#FEF2F2"},
            on_click=on_reset,
            padding="0.75rem 1.5rem",
            border_radius="0.5rem"
        ),
        
        spacing="3",
        wrap="wrap",
        width="100%",
        justify="center"
    )


def token_display_container(
    current_text: str = "",
    total_tokens: int = 0,
    alternatives: List[TokenProbability] = None,
    selected_index: Optional[int] = None,
    is_generating: bool = False,
    can_undo: bool = False,
    can_generate: bool = True,
    on_token_select: Optional[rx.EventHandler] = None,
    on_generate_next: Optional[rx.EventHandler] = None,
    on_reset: Optional[rx.EventHandler] = None,
    on_undo_last: Optional[rx.EventHandler] = None,
    show_probability_text: bool = True,
    show_percentage: bool = True
) -> rx.Component:
    """Complete token display container with header, alternatives, and controls.
    
    This is the main component that combines all token display elements.
    """
    
    # Note: Cannot use `alternatives = alternatives or []` with Reflex state variables
    # because `or` operator is not allowed on Vars. Instead, handle None case in rx.cond.
    
    return rx.vstack(
        # Header with current text and stats
        token_selection_header(
            current_text=current_text,
            total_tokens=total_tokens,
            show_next_instruction=alternatives is not None
        ),
        
        # Token alternatives (only show if we have alternatives)
        rx.cond(
            alternatives,
            rx.vstack(
                rx.heading(
                    "Select Next Token:",
                    size="4",
                    margin_bottom="0.5rem",
                    color="#374151"
                ),
                token_alternatives_grid(
                    alternatives=alternatives,
                    selected_index=selected_index,
                    on_token_select=on_token_select,
                    max_columns=3,
                    show_probability_text=show_probability_text,
                    show_percentage=show_percentage
                ),
                spacing="3",
                width="100%"
            ),
            rx.box()  # Empty box instead of fragment
        ),
        
        # Control buttons
        token_generation_controls(
            on_generate_next=on_generate_next,
            on_reset=on_reset,
            on_undo_last=on_undo_last,
            is_generating=is_generating,
            can_undo=can_undo,
            can_generate=can_generate
        ),
        
        spacing="6",
        width="100%",
        max_width="800px",
        margin="0 auto",
        padding="1rem"
    )
