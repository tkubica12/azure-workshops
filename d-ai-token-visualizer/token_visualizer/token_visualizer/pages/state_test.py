"""State management test page for debugging and verification."""

import reflex as rx
from typing import Dict, Any

from ..state import (
    CounterTestState, 
    TokenState, 
    SettingsState, 
    NavigationState,
    UIState
)
from ..components.layout import app_layout


def counter_test_section() -> rx.Component:
    """Counter test section to verify basic state management."""
    return rx.box(
        rx.vstack(
            rx.heading("Counter Test", size="5", color="#1A1A1A", margin_bottom="4"),
            
            # Counter display
            rx.center(
                rx.text(
                    CounterTestState.count,
                    font_size="3rem",
                    font_weight="bold",
                    color="#3B82F6"
                ),
                margin_bottom="4"
            ),
            
            # Counter controls
            rx.hstack(
                rx.button(
                    "- Decrement",
                    on_click=CounterTestState.decrement,
                    color_scheme="red",
                    size="3"
                ),
                rx.button(
                    "+ Increment", 
                    on_click=CounterTestState.increment,
                    color_scheme="blue",
                    size="3"
                ),
                rx.button(
                    "Reset",
                    on_click=CounterTestState.reset_counter,
                    color_scheme="gray",
                    size="3"
                ),
                spacing="3",
                justify="center"
            ),
            
            # Counter history
            rx.box(
                rx.text("History:", font_weight="bold", margin_bottom="2"),
                rx.text(
                    rx.cond(
                        CounterTestState.history,
                        f"Last 10 values: {CounterTestState.history[-10:]}",
                        "No history yet"
                    ),
                    font_size="0.875rem",
                    color="#6B7280"
                ),
                margin_top="4",
                padding="3",
                background="#F9FAFB",
                border_radius="8px",
                border="1px solid #E5E7EB"
            ),
            
            spacing="4",
            align="center"
        ),
        padding="6",
        border_radius="12px",
        background="#FFFFFF",
        border="1px solid #E5E7EB",
        margin_bottom="6"
    )


def token_state_section() -> rx.Component:
    """Token state test section."""
    return rx.box(
        rx.vstack(
            rx.heading("Token State Test", size="5", color="#1A1A1A", margin_bottom="4"),
            
            # Current prompt input
            rx.vstack(
                rx.text("Test Prompt:", font_weight="bold"),
                rx.input(
                    placeholder="Enter a test prompt...",
                    value=TokenState.current_prompt,
                    on_change=TokenState.set_current_prompt,
                    width="100%",
                    size="3"
                ),
                rx.button(
                    "Start New Session",
                    on_click=TokenState.start_test_session,
                    color_scheme="green",
                    size="3",
                    width="100%"
                ),
                spacing="2",
                width="100%"
            ),
            
            # Session info
            rx.box(
                rx.text("Session Info:", font_weight="bold", margin_bottom="2"),
                rx.vstack(
                    rx.text(f"Current Session ID: {TokenState.current_session_id}"),
                    rx.text(f"Generated Tokens: {TokenState.generated_tokens}"),
                    rx.text(f"Token Count: {TokenState.generated_tokens.length()}"),
                    rx.text(f"Total Sessions: {TokenState.sessions.length()}"),
                    spacing="1",
                    font_size="0.875rem",
                    color="#6B7280"
                ),
                padding="3",
                background="#F9FAFB", 
                border_radius="8px",
                border="1px solid #E5E7EB",
                margin_top="4"
            ),
            
            # Token controls
            rx.hstack(
                rx.button(
                    "Add Test Token",
                    on_click=TokenState.add_test_token,
                    color_scheme="blue",
                    size="3"
                ),
                rx.button(
                    "Remove Last Token",
                    on_click=TokenState.remove_last_token,
                    color_scheme="red",
                    size="3"
                ),
                rx.button(
                    "Reset Session",
                    on_click=TokenState.reset_current_session,
                    color_scheme="gray",
                    size="3"
                ),
                spacing="2",
                justify="center",
                margin_top="4"
            ),
            
            spacing="4",
            align="stretch"
        ),
        padding="6",
        border_radius="12px",
        background="#FFFFFF",
        border="1px solid #E5E7EB",
        margin_bottom="6"
    )


def settings_state_section() -> rx.Component:
    """Settings state test section."""
    return rx.box(
        rx.vstack(
            rx.heading("Settings State Test", size="5", color="#1A1A1A", margin_bottom="4"),
            
            # Current settings display
            rx.grid(
                rx.box(
                    rx.vstack(
                        rx.text("Visualization", font_weight="bold"),
                        rx.text(f"Mode: {SettingsState.current_mode}", font_size="0.875rem"),
                        rx.text(f"Color Scheme: {SettingsState.color_scheme}", font_size="0.875rem"),
                        spacing="1"
                    ),
                    padding="3",
                    background="#F0F9FF",
                    border_radius="8px",
                    border="1px solid #BAE6FD"
                ),
                
                rx.box(
                    rx.vstack(
                        rx.text("Generation", font_weight="bold"),
                        rx.text(f"Max Tokens: {SettingsState.max_tokens_per_generation}", font_size="0.875rem"),
                        rx.text(f"Top K: {SettingsState.top_k_alternatives}", font_size="0.875rem"),
                        rx.text(f"Temperature: {SettingsState.temperature}", font_size="0.875rem"),
                        spacing="1"
                    ),
                    padding="3",
                    background="#F0FDF4",
                    border_radius="8px",
                    border="1px solid #BBF7D0"
                ),
                
                rx.box(
                    rx.vstack(
                        rx.text("UI Preferences", font_weight="bold"),
                        rx.text(f"Show %: {SettingsState.show_probabilities_as_percentages}", font_size="0.875rem"),
                        rx.text(f"Debug: {SettingsState.enable_debug_mode}", font_size="0.875rem"),
                        spacing="1"
                    ),
                    padding="3",
                    background="#FEF7FF",
                    border_radius="8px",
                    border="1px solid #E879F9"
                ),
                
                columns="3",
                gap="3",
                width="100%"
            ),
            
            # Settings controls
            rx.hstack(
                rx.button(
                    "Toggle Debug",
                    on_click=SettingsState.toggle_debug_mode,
                    color_scheme="purple",
                    size="3"
                ),
                rx.button(
                    "Reset Settings",
                    on_click=SettingsState.reset_to_defaults,
                    color_scheme="gray",
                    size="3"
                ),
                spacing="3",
                justify="center",
                margin_top="4"
            ),
            
            spacing="4",
            align="stretch"
        ),
        padding="6",
        border_radius="12px",
        background="#FFFFFF",
        border="1px solid #E5E7EB",
        margin_bottom="6"
    )


def debug_info_section() -> rx.Component:
    """Debug information section."""
    return rx.box(
        rx.vstack(
            rx.heading("Debug Information", size="5", color="#1A1A1A", margin_bottom="4"),
            
            rx.accordion.root(
                rx.accordion.item(
                    header="Counter State Debug",
                    content=rx.box(
                        rx.text("Counter Debug Info:", font_weight="bold", margin_bottom="2"),
                        rx.code_block(
                            str(CounterTestState.get_counter_info()),
                            language="json",
                            font_size="0.75rem"
                        ),
                        padding="2"
                    ),
                    value="counter"
                ),
                
                rx.accordion.item(
                    header="Token State Debug", 
                    content=rx.box(
                        rx.text("Token Debug Info:", font_weight="bold", margin_bottom="2"),
                        rx.code_block(
                            str(TokenState.get_debug_info()),
                            language="json",
                            font_size="0.75rem"
                        ),
                        padding="2"
                    ),
                    value="token"
                ),
                
                rx.accordion.item(
                    header="Settings Summary",
                    content=rx.box(
                        rx.text("Settings Summary:", font_weight="bold", margin_bottom="2"),
                        rx.code_block(
                            str(SettingsState.get_settings_summary()),
                            language="json",
                            font_size="0.75rem"
                        ),
                        padding="2"
                    ),
                    value="settings"
                ),
                
                collapsible=True,
                width="100%"
            ),
            
            spacing="4",
            align="stretch"
        ),
        padding="6",
        border_radius="12px",
        background="#FFFFFF",
        border="1px solid #E5E7EB"
    )


def state_test_content() -> rx.Component:
    """Main content for the state test page."""
    return rx.vstack(
        # Page header
        rx.box(
            rx.vstack(
                rx.heading(
                    "State Management Test",
                    size="8",
                    color="#1A1A1A",
                    font_weight="600",
                    text_align="center"
                ),
                rx.text(
                    "Test and debug application state management functionality",
                    font_size="1.125rem",
                    color="#6B7280",
                    text_align="center",
                    line_height="1.6"
                ),
                spacing="2",
                align="center"
            ),
            padding="3rem 2rem",
            border_radius="0.75rem",
            background="#FAFAFA",
            border="1px solid #E5E7EB",
            margin_bottom="6"
        ),
        
        # Test sections
        counter_test_section(),
        token_state_section(),
        settings_state_section(),
        debug_info_section(),
        
        spacing="6",
        align="stretch",
        width="100%",
        max_width="1200px",
        margin="0 auto"
    )


def state_test_page() -> rx.Component:
    """State management test page."""
    return app_layout(
        state_test_content()
    )
